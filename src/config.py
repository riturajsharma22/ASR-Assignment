from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
AUDIO_DIR = DATA_DIR / "audio"
GROUND_TRUTH_CSV = DATA_DIR / "ground_truth.csv"
RESULTS_DIR = ROOT_DIR / "results"
TRANSCRIPTIONS_JSON = RESULTS_DIR / "transcriptions.json"
METRICS_CSV = RESULTS_DIR / "metrics.csv"
SUMMARY_CSV = RESULTS_DIR / "summary.csv"
FAILURES_MD = RESULTS_DIR / "failures.md"

# ---------------------------------------------------------------------------
# API keys — set in .env, never hard-code
# ---------------------------------------------------------------------------
DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY", "")
SARVAM_API_KEY: str = os.getenv("SARVAM_API_KEY", "")
HF_TOKEN: str = os.getenv("HF_TOKEN", "")

# ---------------------------------------------------------------------------
# Local model settings
# ---------------------------------------------------------------------------
# Switch to "medium" in .env if large-v3 is too slow on CPU (~5-30x real-time)
WHISPER_MODEL_SIZE: str = os.getenv("WHISPER_MODEL_SIZE", "large-v3")

SAMPLE_RATE: int = 16_000
