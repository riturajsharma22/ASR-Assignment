"""
Generates results/failures.md.

For every (file, model) pair where strict locality match failed, writes a
markdown section containing:
  - file name and recording condition
  - ground truth transcript and canonical locality
  - side-by-side table of all models' transcripts for that file
  - edit distance from each model's output to the canonical locality
"""

import json
from pathlib import Path

import pandas as pd

from .config import GROUND_TRUTH_CSV, TRANSCRIPTIONS_JSON, FAILURES_MD
from .metrics import strict_locality_match, min_edit_distance_to_locality


def _cache_key(file_name: str, model_name: str) -> str:
    return f"{file_name}__{model_name}"


def generate_failures_report(ground_truth_path: Path = GROUND_TRUTH_CSV) -> None:
    if not TRANSCRIPTIONS_JSON.exists():
        raise FileNotFoundError(
            f"Transcriptions cache not found at {TRANSCRIPTIONS_JSON}. "
            "Run transcription step first."
        )

    ground_truth = pd.read_csv(ground_truth_path)

    with open(TRANSCRIPTIONS_JSON, "r", encoding="utf-8") as fh:
        cache = json.load(fh)

    all_models = sorted({key.split("__", 1)[1] for key in cache})

    lines: list[str] = ["# Failure Analysis\n\n"]
    lines.append(
        "Sections appear for every *(file, model)* pair where strict locality "
        "match failed. The side-by-side table covers **all** models for context.\n\n"
    )
    lines.append("---\n\n")

    failure_count = 0

    for _, gt in ground_truth.iterrows():
        file_name = str(gt["file_name"])
        canonical = str(gt["locality_canonical"])
        ref_transcript = str(gt["full_transcript"])
        condition = str(gt.get("condition", "unknown"))

        for model_name in all_models:
            entry = cache.get(_cache_key(file_name, model_name), {})
            transcript = entry.get("transcript", "") or ""
            error = entry.get("error") or ""

            if error:
                continue  # transcription errors are out-of-scope here

            no_output = not transcript
            if not no_output and strict_locality_match(transcript, canonical):
                continue  # strict match passed — not a failure

            failure_count += 1
            failure_mode = "NO OUTPUT" if no_output else "WRONG OUTPUT"

            lines.append(
                f"## `{file_name}` — model: `{model_name}` "
                f"— condition: {condition} — [{failure_mode}]\n\n"
            )
            if no_output:
                lines.append(
                    "**Failure mode: NO OUTPUT** — model returned an empty transcript.\n\n"
                )
            else:
                lines.append(f"**Ground Truth:** {ref_transcript}\n\n")
                lines.append(f"**Canonical Locality:** `{canonical}`\n\n")

            # Side-by-side table (always shown for context across all models)
            lines.append("| Model | Transcript | Edit Distance |\n")
            lines.append("|-------|-----------|:---:|\n")

            for m in all_models:
                e = cache.get(_cache_key(file_name, m), {})
                t = e.get("transcript", "") or ""
                err = e.get("error") or ""
                if err:
                    lines.append(f"| `{m}` | *ERROR: {err[:100]}* | — |\n")
                elif not t:
                    lines.append(f"| `{m}` | *NO OUTPUT* | — |\n")
                else:
                    dist = min_edit_distance_to_locality(t, canonical)
                    display_t = t.replace("|", "\\|")
                    lines.append(f"| `{m}` | {display_t} | {dist} |\n")

            lines.append("\n---\n\n")

    if failure_count == 0:
        lines.append("*No strict locality match failures found.*\n")

    FAILURES_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(FAILURES_MD, "w", encoding="utf-8") as fh:
        fh.writelines(lines)

    print(f"Failure analysis written to {FAILURES_MD} ({failure_count} failure(s))")
