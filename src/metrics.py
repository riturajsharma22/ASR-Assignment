"""
Metrics computation: WER, CER, locality entity accuracy, latency stats.

Locality matching strategy
--------------------------
Model output is Devanagari; canonical locality names are Latin ("Koramangala").
We transliterate the transcript Devanagari → IAST → strip diacritics → ASCII-
approximate Latin, then substring/Levenshtein match against the canonical.

WER/CER strategy
----------------
Both reference (ground truth) and hypothesis (model output) are Devanagari,
so we normalise in-script (strip ।, punctuation, collapse whitespace) and
compute WER/CER directly — no transliteration, which would add noise.

Outputs
-------
results/metrics.csv              long format  (file, model, condition, language_mix, metric, value)
results/summary.csv              wide format  (model × metric aggregates)
results/sliced_condition.csv     locality accuracy broken down by condition
results/sliced_language_mix.csv  locality accuracy broken down by language_mix
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# Auto-install indic-transliteration if missing
try:
    from indic_transliteration import sanscript as _sanscript
    from indic_transliteration.sanscript import transliterate as _xlit
except ImportError:
    print("[metrics] indic-transliteration not found — installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "indic-transliteration"])
    from indic_transliteration import sanscript as _sanscript
    from indic_transliteration.sanscript import transliterate as _xlit

import Levenshtein
import pandas as pd
from jiwer import wer, cer

from .config import (
    GROUND_TRUTH_CSV,
    TRANSCRIPTIONS_JSON,
    METRICS_CSV,
    SUMMARY_CSV,
    RESULTS_DIR,
)

# ---------------------------------------------------------------------------
# IAST diacritic → ASCII (applied after Devanagari → IAST transliteration)
# ---------------------------------------------------------------------------

_IAST_STRIP = str.maketrans({
    # Long vowels
    'ā': 'a', 'ī': 'i', 'ū': 'u',
    # Retroflex consonants
    'ṭ': 't', 'ḍ': 'd', 'ṇ': 'n',
    # Sibilants / fricatives
    'ś': 's', 'ṣ': 's',
    # Other
    'ḥ': 'h', 'ṃ': 'm', 'ṁ': 'm',
    'ñ': 'n', 'ṅ': 'n', 'ṛ': 'r', 'ḷ': 'l', 'ḻ': 'l',
    # Uppercase variants (safe guard)
    'Ā': 'a', 'Ī': 'i', 'Ū': 'u',
    'Ṭ': 't', 'Ḍ': 'd', 'Ṇ': 'n',
    'Ś': 's', 'Ṣ': 's',
    'Ḥ': 'h', 'Ṃ': 'm', 'Ṁ': 'm',
})


def _to_simplified_latin(text: str) -> str:
    """
    Devanagari → IAST → strip diacritics → lowercase ASCII approximation.
    Latin characters in mixed-script input pass through unchanged.
    e.g. "कोरमंगला" → IAST "korāmaṃgalā" → strip → "koramamgala"
         (matches canonical "koramangala" at window distance 1, not exact)
         "Whitefield के पास" → "whitefield ke pasa" (Latin preserved)
    """
    if not text:
        return ""
    try:
        iast = _xlit(text, _sanscript.DEVANAGARI, _sanscript.IAST)
    except Exception:
        iast = text
    return iast.translate(_IAST_STRIP).lower()


# ---------------------------------------------------------------------------
# Text normalisation
# ---------------------------------------------------------------------------

def normalize(text: str) -> str:
    """
    Lowercase, strip punctuation (incl. Devanagari ।॥), collapse whitespace.
    \w is Unicode-aware: keeps Devanagari, Latin letters, digits; removes punctuation.
    Used for WER/CER on raw Devanagari and for post-transliteration locality matching.
    """
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# Locality matching (transliteration-based, window Levenshtein)
# ---------------------------------------------------------------------------

def _is_pure_ascii(text: str) -> bool:
    return all(ord(c) < 128 for c in text)


def _normalised_canonical(canonical: str) -> str:
    """
    Normalise a canonical locality name for matching.
    Pure-ASCII canonicals (all Bangalore names here) are just lowercased —
    no transliteration needed, which would only add noise.
    Non-ASCII canonicals are transliterated first.
    """
    if _is_pure_ascii(canonical):
        return normalize(canonical)
    return normalize(_to_simplified_latin(canonical))


def _best_window_distance(simplified_transcript: str, norm_canonical: str) -> int:
    """
    Slide a character window of len(norm_canonical) across simplified_transcript
    and return the minimum Levenshtein distance to norm_canonical.
    """
    n = len(norm_canonical)
    if not norm_canonical:
        return 0
    if not simplified_transcript:
        return n
    min_dist = Levenshtein.distance(simplified_transcript, norm_canonical)
    for i in range(len(simplified_transcript)):
        window = simplified_transcript[i : i + n]
        if len(window) < max(1, n // 2):
            break
        dist = Levenshtein.distance(window, norm_canonical)
        if dist < min_dist:
            min_dist = dist
        if min_dist == 0:
            break
    return min_dist


def strict_locality_match(transcript: str, canonical: str) -> bool:
    """
    Window Levenshtein ≤ 1 between simplified transcript and normalised canonical.
    Tolerates one transliteration noise character (e.g. 'koramamgala' → 'koramangala').
    """
    simplified = normalize(_to_simplified_latin(transcript))
    norm_c = _normalised_canonical(canonical)
    return _best_window_distance(simplified, norm_c) <= 1


def min_edit_distance_to_locality(transcript: str, canonical: str) -> int:
    """Best window Levenshtein distance (simplified-Latin transcript vs normalised canonical)."""
    simplified = normalize(_to_simplified_latin(transcript))
    norm_c = _normalised_canonical(canonical)
    return _best_window_distance(simplified, norm_c)


def fuzzy_locality_match(transcript: str, canonical: str) -> bool:
    """Window Levenshtein ≤ 3."""
    return min_edit_distance_to_locality(transcript, canonical) <= 3


# ---------------------------------------------------------------------------
# Per-(file, model) metrics
# ---------------------------------------------------------------------------

def _cache_key(file_name: str, model_name: str) -> str:
    return f"{file_name}__{model_name}"


def compute_metrics(ground_truth: pd.DataFrame, cache: dict) -> pd.DataFrame:
    rows: list[dict] = []

    for _, gt in ground_truth.iterrows():
        file_name = str(gt["file_name"])
        canonical = str(gt["locality_canonical"])
        ref_transcript = str(gt["full_transcript"])
        condition = str(gt.get("condition", ""))
        language_mix = str(gt.get("language_mix", ""))

        model_names = sorted({
            key.split("__", 1)[1]
            for key in cache
            if key.startswith(file_name + "__")
        })

        for model_name in model_names:
            entry = cache.get(_cache_key(file_name, model_name), {})
            transcript = entry.get("transcript", "") or ""
            latency_ms = float(entry.get("latency_ms") or 0.0)
            audio_duration_ms = float(entry.get("audio_duration_ms") or 0.0)
            error = entry.get("error") or ""

            base = {
                "file": file_name,
                "model": model_name,
                "condition": condition,
                "language_mix": language_mix,
            }

            if error or not transcript:
                for metric in ("wer", "cer", "locality_strict", "locality_fuzzy",
                               "edit_distance", "latency_ms", "rtf"):
                    rows.append({**base, "metric": metric, "value": float("nan")})
                continue

            # WER/CER: normalise in-script (Devanagari) — no transliteration
            norm_ref = normalize(ref_transcript)
            norm_hyp = normalize(transcript)

            try:
                wer_val = wer(norm_ref, norm_hyp) if norm_ref and norm_hyp else float("nan")
            except Exception:
                wer_val = float("nan")

            try:
                cer_val = cer(norm_ref, norm_hyp) if norm_ref and norm_hyp else float("nan")
            except Exception:
                cer_val = float("nan")

            # Locality: transliterate transcript → simplified Latin, match vs canonical
            strict = float(strict_locality_match(transcript, canonical))
            fuzzy = float(fuzzy_locality_match(transcript, canonical))
            edit_dist = float(min_edit_distance_to_locality(transcript, canonical))
            rtf = latency_ms / audio_duration_ms if audio_duration_ms > 0 else float("nan")

            for metric, value in (
                ("wer", wer_val),
                ("cer", cer_val),
                ("locality_strict", strict),
                ("locality_fuzzy", fuzzy),
                ("edit_distance", edit_dist),
                ("latency_ms", latency_ms),
                ("rtf", rtf),
            ):
                rows.append({**base, "metric": metric, "value": value})

    cols = ["file", "model", "condition", "language_mix", "metric", "value"]
    return pd.DataFrame(rows, columns=cols)


# ---------------------------------------------------------------------------
# Aggregated summary (wide format)
# ---------------------------------------------------------------------------

def compute_summary(metrics_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    for model, group in metrics_df.groupby("model"):
        row: dict = {"model": model}

        for metric in ("wer", "cer", "locality_strict", "locality_fuzzy"):
            vals = group.loc[group["metric"] == metric, "value"].dropna()
            row[f"{metric}_mean"] = vals.mean() if len(vals) else float("nan")

        latencies = group.loc[group["metric"] == "latency_ms", "value"].dropna()
        row["latency_mean_ms"] = latencies.mean() if len(latencies) else float("nan")
        row["latency_p50_ms"] = latencies.quantile(0.50) if len(latencies) else float("nan")
        row["latency_p95_ms"] = latencies.quantile(0.95) if len(latencies) else float("nan")

        rows.append(row)

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Sliced locality accuracy
# ---------------------------------------------------------------------------

def compute_sliced_metrics(metrics_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    slices: dict[str, pd.DataFrame] = {}
    strict_df = metrics_df[metrics_df["metric"] == "locality_strict"].dropna(subset=["value"])

    for col in ("condition", "language_mix"):
        if col not in strict_df.columns:
            continue
        slices[col] = (
            strict_df.groupby(["model", col])["value"]
            .mean()
            .reset_index()
            .rename(columns={"value": "locality_strict_acc"})
        )
    return slices


# ---------------------------------------------------------------------------
# Per-file locality inspection table
# ---------------------------------------------------------------------------

def build_locality_table(
    ground_truth: pd.DataFrame,
    cache: dict,
    display_models: list[str] | None = None,
) -> pd.DataFrame:
    """
    Returns a DataFrame showing the simplified-Latin transcript and strict-match
    result for each file × model — for visual verification of transliteration.
    Columns: file, canonical, <model>_simplified, <model>_hit, ...
    """
    if display_models is None:
        display_models = ["deepgram", "sarvam", "whisper"]

    rows: list[dict] = []
    for _, gt in ground_truth.iterrows():
        file_name = str(gt["file_name"])
        canonical = str(gt["locality_canonical"])
        norm_c = _normalised_canonical(canonical)
        r: dict = {
            "file": file_name,
            "canonical": canonical,
            "canonical_transliterated": norm_c,  # what the canonical is matched against
        }

        for model in display_models:
            entry = cache.get(_cache_key(file_name, model), {})
            transcript = entry.get("transcript", "") or ""
            error = entry.get("error") or ""

            if error:
                simplified, hit = "ERROR", "✗"
            elif not transcript:
                simplified, hit = "NO OUTPUT", "✗"
            else:
                simplified = normalize(_to_simplified_latin(transcript))
                dist = _best_window_distance(simplified, norm_c)
                hit = "✓" if dist <= 1 else ("~" if dist <= 3 else "✗")
                if len(simplified) > 48:
                    simplified = simplified[:48] + "…"

            r[f"{model}_simplified"] = simplified
            r[f"{model}_hit"] = hit

        rows.append(r)

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_metrics(ground_truth_path: Path = GROUND_TRUTH_CSV) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not TRANSCRIPTIONS_JSON.exists():
        raise FileNotFoundError(
            f"Transcriptions cache not found at {TRANSCRIPTIONS_JSON}. "
            "Run transcription step first."
        )

    ground_truth = pd.read_csv(ground_truth_path)

    with open(TRANSCRIPTIONS_JSON, "r", encoding="utf-8") as fh:
        cache = json.load(fh)

    metrics_df = compute_metrics(ground_truth, cache)
    metrics_df.to_csv(METRICS_CSV, index=False)
    print(f"Metrics written to {METRICS_CSV}")

    summary_df = compute_summary(metrics_df)
    summary_df.to_csv(SUMMARY_CSV, index=False)
    print(f"Summary written to {SUMMARY_CSV}")

    sliced = compute_sliced_metrics(metrics_df)
    for name, sdf in sliced.items():
        out = RESULTS_DIR / f"sliced_{name}.csv"
        sdf.to_csv(out, index=False)
        print(f"Sliced metrics ({name}) written to {out}")

    return metrics_df, summary_df
