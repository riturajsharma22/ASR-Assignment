# ASR Shootout — Bangalore Locality Names (Hindi/Hinglish)

Benchmark of three speech-to-text systems on 20 self-recorded MP3 audio samples of
Bangalore locality names spoken in natural Hindi/Hinglish conversational sentences
with varied recording conditions.

---

## Models

| Model | Type | Backend | Notes |
|-------|------|---------|-------|
| Deepgram nova-3 | Cloud API (baseline) | deepgram-sdk | multilingual nova-3 |
| Whisper large-v3 | Local CPU | faster-whisper | set `WHISPER_MODEL_SIZE=medium` in `.env` to reduce load |
| Sarvam AI Saarika v2 | Cloud API | REST | requires `SARVAM_API_KEY` |

---

## Quickstart

### 1. Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. Install dependencies

Install in two steps — order matters:

```bash
# Step 1 — CPU-only PyTorch
pip install torch==2.4.1+cpu --index-url https://download.pytorch.org/whl/cpu

# Step 2 — everything else
pip install -r requirements.txt
```

### 3. Configure API keys

```bash
cp .env.example .env   # Windows: copy .env.example .env
# Edit .env — fill in DEEPGRAM_API_KEY, SARVAM_API_KEY, HF_TOKEN
```

### 4. Add audio and ground truth

- Drop your 20 MP3 files into `data/audio/`
- Open `data/ground_truth.csv` and add one row per file

**Ground truth schema:**

| Column | Values / Notes |
|--------|----------------|
| `file_name` | e.g. `01_koramangala_quiet.mp3` |
| `full_transcript` | Exact spoken sentence |
| `locality_canonical` | Official English spelling, e.g. `Koramangala`, `HSR Layout` |
| `language_mix` | `hindi` / `hinglish` / `kannada` / `english` |
| `condition` | `quiet` / `traffic` / `phone` / `whispered` / `rushed` |
| `speaker_notes` | Free-text observations |

### 5. Run the full pipeline

```bash
python -m src.run_all
```

Options:

```
--force            Re-transcribe all files, ignoring the cache
--skip-transcribe  Skip transcription; reuse existing results/transcriptions.json
--skip-metrics     Transcribe only, do not compute metrics
```

---

## Output files

| File | Description |
|------|-------------|
| `results/transcriptions.json` | Cached transcripts and latencies keyed by `file__model` |
| `results/metrics.csv` | Long-format per-(file, model) metrics |
| `results/summary.csv` | Wide-format per-model aggregates |
| `results/sliced_condition.csv` | Locality accuracy by recording condition |
| `results/sliced_language_mix.csv` | Locality accuracy by language mix |
| `results/failures.md` | Side-by-side failure analysis for every strict-match miss |

---

## Limitations

- **CPU speed**: Whisper large-v3 may take 5–30× real-time on CPU. Use
  `WHISPER_MODEL_SIZE=medium` in `.env` for faster iteration.
- **Sarvam language code**: Set to `unknown` for auto-detection. Switch to
  `hi-IN` in `transcribe.py` if auto-detection performs poorly.
- **Locality matching**: Uses character-level sliding-window Levenshtein; may
  miss transliteration variants far from the canonical spelling.
- **Single speaker**: Results reflect one speaker's recordings and may not
  generalise to other accents or microphones.
