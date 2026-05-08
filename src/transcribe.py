"""
ASR model implementations and batch transcription pipeline.

Cache format  (results/transcriptions.json):
  { "<file_name>__<model_name>": { ...TranscriptionResult fields... }, ... }

Re-runs skip cached pairs unless --force is passed to run_transcriptions().
"""

import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from pathlib import Path

import librosa
from tqdm import tqdm

from .config import (
    DEEPGRAM_API_KEY,
    SARVAM_API_KEY,
    HF_TOKEN,
    WHISPER_MODEL_SIZE,
    SAMPLE_RATE,
    TRANSCRIPTIONS_JSON,
)


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class TranscriptionResult:
    transcript: str
    latency_ms: float
    audio_duration_ms: float
    raw_response: dict | None
    error: str | None


class ASRModel(ABC):
    name: str

    @abstractmethod
    def transcribe(self, audio_path: Path) -> TranscriptionResult: ...


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _audio_duration_ms(audio_path: Path) -> float:
    return librosa.get_duration(path=str(audio_path)) * 1000.0


def _cache_key(file_name: str, model_name: str) -> str:
    return f"{file_name}__{model_name}"


# ---------------------------------------------------------------------------
# Model 1 — Deepgram nova-3 (mandatory baseline)
# ---------------------------------------------------------------------------

class DeepgramModel(ASRModel):
    name = "deepgram"

    def __init__(self) -> None:
        if not DEEPGRAM_API_KEY:
            raise ValueError("DEEPGRAM_API_KEY is not set in .env")
        from deepgram import DeepgramClient, PrerecordedOptions
        self._client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
        self._options = PrerecordedOptions(
            model="nova-3",
            language="multi",
            smart_format=True,
        )

    def transcribe(self, audio_path: Path) -> TranscriptionResult:
        duration_ms = _audio_duration_ms(audio_path)
        try:
            with open(audio_path, "rb") as fh:
                buffer_data = fh.read()
            t0 = time.perf_counter()
            response = self._client.listen.rest.v("1").transcribe_file(
                {"buffer": buffer_data, "mimetype": "audio/mpeg"},
                self._options,
            )
            latency_ms = (time.perf_counter() - t0) * 1000.0
            transcript = response.results.channels[0].alternatives[0].transcript
            return TranscriptionResult(
                transcript=transcript,
                latency_ms=latency_ms,
                audio_duration_ms=duration_ms,
                raw_response=None,
                error=None,
            )
        except Exception as exc:
            return TranscriptionResult(
                transcript="",
                latency_ms=0.0,
                audio_duration_ms=duration_ms,
                raw_response=None,
                error=str(exc),
            )


# ---------------------------------------------------------------------------
# Model 2 — OpenAI Whisper large-v3 (via faster-whisper, CPU)
# ---------------------------------------------------------------------------

class WhisperModel(ASRModel):
    name = "whisper"

    def __init__(self) -> None:
        from faster_whisper import WhisperModel as _FWModel
        # WHISPER_MODEL_SIZE defaults to "large-v3".
        # Set WHISPER_MODEL_SIZE=medium in .env if large-v3 is too slow on CPU.
        self._model = _FWModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")

    def transcribe(self, audio_path: Path) -> TranscriptionResult:
        duration_ms = _audio_duration_ms(audio_path)
        try:
            audio, _ = librosa.load(str(audio_path), sr=SAMPLE_RATE, mono=True)
            t0 = time.perf_counter()
            # segments is a lazy generator — actual decoding happens during iteration
            segments, info = self._model.transcribe(audio, language="hi")
            transcript = " ".join(seg.text.strip() for seg in segments)
            latency_ms = (time.perf_counter() - t0) * 1000.0
            return TranscriptionResult(
                transcript=transcript,
                latency_ms=latency_ms,
                audio_duration_ms=duration_ms,
                raw_response={
                    "detected_language": info.language,
                    "language_probability": info.language_probability,
                },
                error=None,
            )
        except Exception as exc:
            return TranscriptionResult(
                transcript="",
                latency_ms=0.0,
                audio_duration_ms=duration_ms,
                raw_response=None,
                error=str(exc),
            )


# ---------------------------------------------------------------------------
# Model 3 — AI4Bharat IndicConformer Hindi (NeMo, AI4Bharat fork)
#
# Requires the AI4Bharat NeMo fork — NOT the standard NVIDIA nemo_toolkit:
#   pip install "nemo_toolkit[asr] @ git+https://github.com/AI4Bharat/NeMo.git"
#
# NeMo's transcribe() takes file paths, so we write a temporary WAV via
# soundfile before calling it, then clean up.
# ---------------------------------------------------------------------------

class IndicConformerModel(ASRModel):
    name = "indicconformer"
    _MODEL_ID = "ai4bharat/indicconformer_stt_hi_hybrid_ctc_rnnt_large"

    def __init__(self) -> None:
        import nemo.collections.asr as nemo_asr
        self._model = nemo_asr.models.ASRModel.from_pretrained(self._MODEL_ID)
        self._model.freeze()
        self._model = self._model.to("cpu")
        # CTC decoder is faster than RNNT on CPU and produces comparable accuracy
        self._model.cur_decoder = "ctc"

    def transcribe(self, audio_path: Path) -> TranscriptionResult:
        import tempfile
        import soundfile as sf
        duration_ms = _audio_duration_ms(audio_path)
        try:
            # NeMo needs 16 kHz mono WAV; load via librosa then write temp file
            audio, _ = librosa.load(str(audio_path), sr=SAMPLE_RATE, mono=True)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            sf.write(str(tmp_path), audio, SAMPLE_RATE)
            try:
                t0 = time.perf_counter()
                results = self._model.transcribe(
                    [str(tmp_path)],
                    batch_size=1,
                    logprobs=False,
                    language_id="hi",
                    verbose=False,
                )
                latency_ms = (time.perf_counter() - t0) * 1000.0
            finally:
                tmp_path.unlink(missing_ok=True)
            transcript = str(results[0]) if results else ""
            return TranscriptionResult(
                transcript=transcript,
                latency_ms=latency_ms,
                audio_duration_ms=duration_ms,
                raw_response=None,
                error=None,
            )
        except Exception as exc:
            return TranscriptionResult(
                transcript="",
                latency_ms=0.0,
                audio_duration_ms=duration_ms,
                raw_response=None,
                error=str(exc),
            )


# ---------------------------------------------------------------------------
# Model 4 — Sarvam AI Saarika v2 (REST API)
# ---------------------------------------------------------------------------

class SarvamModel(ASRModel):
    name = "sarvam"
    _API_URL = "https://api.sarvam.ai/speech-to-text"

    def __init__(self) -> None:
        if not SARVAM_API_KEY:
            raise ValueError(
                "SARVAM_API_KEY is not set. "
                "Sign up at https://dashboard.sarvam.ai and add the key to .env"
            )
        self._headers = {"api-subscription-key": SARVAM_API_KEY}

    def transcribe(self, audio_path: Path) -> TranscriptionResult:
        import requests as _req
        duration_ms = _audio_duration_ms(audio_path)
        try:
            with open(audio_path, "rb") as fh:
                audio_bytes = fh.read()
            files = {"file": (audio_path.name, audio_bytes, "audio/mpeg")}
            # language_code="unknown" requests automatic language detection (handles Hinglish)
            data = {"model": "saarika:v2.5", "language_code": "unknown"}
            t0 = time.perf_counter()
            resp = _req.post(
                self._API_URL,
                headers=self._headers,
                files=files,
                data=data,
                timeout=30,
            )
            latency_ms = (time.perf_counter() - t0) * 1000.0
            resp.raise_for_status()
            body = resp.json()
            transcript = body.get("transcript", "")
            return TranscriptionResult(
                transcript=transcript,
                latency_ms=latency_ms,
                audio_duration_ms=duration_ms,
                raw_response={"language_code": body.get("language_code")},
                error=None,
            )
        except Exception as exc:
            return TranscriptionResult(
                transcript="",
                latency_ms=0.0,
                audio_duration_ms=duration_ms,
                raw_response=None,
                error=str(exc),
            )


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

def load_cache() -> dict:
    if TRANSCRIPTIONS_JSON.exists():
        with open(TRANSCRIPTIONS_JSON, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_cache(cache: dict) -> None:
    TRANSCRIPTIONS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(TRANSCRIPTIONS_JSON, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Main transcription loop
# ---------------------------------------------------------------------------

def run_transcriptions(
    audio_files: list[Path],
    models: list[ASRModel],
    force: bool = False,
) -> dict:
    cache = {} if force else load_cache()

    for model in models:
        pending = [
            af for af in audio_files
            if force
            or _cache_key(af.name, model.name) not in cache
            or cache[_cache_key(af.name, model.name)].get("error")  # retry previously errored entries
        ]
        if not pending:
            print(f"[{model.name}] all {len(audio_files)} file(s) already cached — skipping")
            continue

        print(f"\n[{model.name}] processing {len(pending)}/{len(audio_files)} file(s)...")
        for audio_path in tqdm(pending, desc=model.name, unit="file"):
            result = model.transcribe(audio_path)
            if result.error:
                tqdm.write(f"  WARN {audio_path.name}: {result.error}")
            cache[_cache_key(audio_path.name, model.name)] = asdict(result)
            save_cache(cache)  # persist after every file so partial runs are recoverable

    return cache
