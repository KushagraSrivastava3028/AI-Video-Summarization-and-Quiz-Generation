from __future__ import annotations
import os
from typing import Optional
from app.config import config
from app.utils.llm_clients import get_openai_client


class TranscriptionResult:
    def __init__(self, text: str, model: str, path: Optional[str] = None):
        self.text = text
        self.model = model
        self.path = path


def transcribe_audio(audio_path: str) -> TranscriptionResult:
    # Try OpenAI Whisper API
    if config.use_openai_whisper_api and config.openai_api_key:
        client = get_openai_client()
        if client is not None:
            try:
                with open(audio_path, "rb") as f:
                    resp = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f,
                        response_format="verbose_json",
                        temperature=0.2,
                    )
                text = getattr(resp, "text", None) or resp.get("text") if isinstance(resp, dict) else None
                if not text and hasattr(resp, "text"):
                    text = resp.text
                if not text:
                    text = ""
                return TranscriptionResult(text=text.strip(), model="openai-whisper-1", path=audio_path)
            except Exception:
                pass

    # Local whisper fallback
    try:
        import whisper  # type: ignore
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        text = result.get("text", "").strip()
        return TranscriptionResult(text=text, model="whisper-local-base", path=audio_path)
    except Exception:
        # Last resort: pretend minimal transcript by filename
        basename = os.path.basename(audio_path)
        return TranscriptionResult(text=f"Transcription unavailable for {basename}.", model="none", path=audio_path)