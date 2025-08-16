from __future__ import annotations
import os
from typing import Optional
from app.config import config

_mistral_client = None
_openai_client = None


def get_mistral_client():
    global _mistral_client
    if _mistral_client is not None:
        return _mistral_client
    api_key = config.mistral_api_key
    if not api_key:
        return None
    try:
        from mistralai import Mistral
        _mistral_client = Mistral(api_key=api_key)
        return _mistral_client
    except Exception:
        return None


def get_openai_client():
    global _openai_client
    if _openai_client is not None:
        return _openai_client
    api_key = config.openai_api_key
    if not api_key:
        return None
    try:
        from openai import OpenAI
        _openai_client = OpenAI(api_key=api_key)
        return _openai_client
    except Exception:
        return None