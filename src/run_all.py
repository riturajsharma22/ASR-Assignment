"""
End-to-end runner: transcribe → metrics → failure analysis.

Usage:
    python -m src.run_all [--force] [--skip-transcribe] [--metrics-only] [--skip-metrics]
"""

import argparse
import json
import sys

import pandas as pd

from .config import AUDIO_DIR, GROUND_TRUTH_CSV, RESULTS_DIR, TRANSCRIPTIONS_JSON
from .transcribe import (
    ASRModel,
    DeepgramModel,
    WhisperModel,
    SarvamModel,
    run_transcriptions,
)
from .metrics import run_metrics, build_locality_table
from .failure_analysis import generate_failures_report


_MODEL_CLASSES = [DeepgramModel, WhisperModel, SarvamModel]


def build_models() -> list[ASRModel]:
    """Initialise all models. Skips any that fail to load (missing keys, missing deps)."""
    models: list[ASRModel] = []
    print("Initialising models...")
    for cls in _MODEL_CLASSES:
        try:
            models.append(cls())
            print(f"  [OK]   {cls.name}")
        except Exception as exc:
            print(f"  [SKIP] {cls.name}: {exc}")
    return models


def _print_locality_table(cache: dict) -> None:
    """Print per-file simplified-Latin transcripts and strict-match results."""
    if not GROUND_TRUTH_CSV.exists():
        return
    gt = pd.read_csv(GROUND_TRUTH_CSV)
    present_models = sorted({k.split("__", 1)[1] for k in cache})
    display = [m for m in ["deepgram", "sarvam", "whisper"] if m in present_models]
    tbl = build_locality_table(gt, cache, display_models=display)
    print("\n=== Per-file locality match (Devanagari -> simplified Latin) ===")
    print(tbl.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the ASR shootout pipeline end-to-end."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-transcribe all files, ignoring the cache.",
    )
    parser.add_argument(
        "--skip-transcribe",
        action="store_true",
        help="Skip transcription; use the existing results/transcriptions.json.",
    )
    parser.add_argument(
        "--metrics-only",
        action="store_true",
        help="Skip transcription; recompute metrics and failure analysis from cached results.",
    )
    parser.add_argument(
        "--skip-metrics",
        action="store_true",
        help="Transcribe only; do not compute metrics or generate failure analysis.",
    )
    args = parser.parse_args()

    skip_transcribe = args.skip_transcribe or args.metrics_only

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Step 1 — Transcription
    # ------------------------------------------------------------------
    if not skip_transcribe:
        audio_files = sorted(AUDIO_DIR.glob("*.mp3"))
        if not audio_files:
            print(f"No MP3 files found in {AUDIO_DIR}. Add your recordings and retry.")
            sys.exit(1)
        print(f"\nFound {len(audio_files)} audio file(s) in {AUDIO_DIR}")

        models = build_models()
        if not models:
            print("\nNo models loaded — check API keys and dependencies.")
            sys.exit(1)

        run_transcriptions(audio_files, models, force=args.force)
        print("\nTranscription complete.")
    else:
        if not TRANSCRIPTIONS_JSON.exists():
            print(
                f"--metrics-only / --skip-transcribe was set but "
                f"{TRANSCRIPTIONS_JSON} does not exist. "
                "Run without that flag first."
            )
            sys.exit(1)
        print(f"Skipping transcription; using {TRANSCRIPTIONS_JSON}")

    # ------------------------------------------------------------------
    # Step 2 — Metrics
    # ------------------------------------------------------------------
    if args.skip_metrics:
        print("Skipping metrics computation (--skip-metrics).")
        return

    if not GROUND_TRUTH_CSV.exists():
        print(
            f"\nGround truth CSV not found at {GROUND_TRUTH_CSV}. "
            "Fill in data/ground_truth.csv before running metrics."
        )
        sys.exit(1)

    print("\nComputing metrics...")
    metrics_df, summary_df = run_metrics()

    print("\n=== Model Summary ===")
    print(summary_df.to_string(index=False))

    # ------------------------------------------------------------------
    # Step 3 — Failure analysis
    # ------------------------------------------------------------------
    print("\nGenerating failure analysis...")
    generate_failures_report()

    # ------------------------------------------------------------------
    # Step 4 — Per-file locality verification table
    # ------------------------------------------------------------------
    with open(TRANSCRIPTIONS_JSON, "r", encoding="utf-8") as fh:
        cache = json.load(fh)
    _print_locality_table(cache)

    print(f"\nAll outputs written to {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
