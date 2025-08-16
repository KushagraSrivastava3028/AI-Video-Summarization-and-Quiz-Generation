from __future__ import annotations
import os
from typing import Optional


def extract_audio_if_video(input_path: str) -> str:
    """
    If the input is a video file, extract audio track to .wav.
    If already audio, return the input path.
    """
    ext = os.path.splitext(input_path)[1].lower()
    if ext in {".wav", ".mp3", ".m4a", ".flac", ".ogg"}:
        return input_path
    try:
        import ffmpeg  # type: ignore
    except Exception:
        # If ffmpeg isn't available, return original; Whisper may still handle some containers.
        return input_path

    output_path = os.path.splitext(input_path)[0] + ".wav"
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path, format="wav", acodec="pcm_s16le", ac=1, ar="16000")
            .overwrite_output()
            .run(quiet=True)
        )
        return output_path
    except Exception:
        return input_path