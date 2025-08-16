from __future__ import annotations
from typing import List, Optional
from app.config import config
from app.utils.llm_clients import get_mistral_client


def _heuristic_summarize(text: str, max_points: int = 5) -> List[str]:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    if not sentences:
        return []
    step = max(1, max(len(sentences) // max_points, 1))
    highlights = sentences[0::step][:max_points]
    return [f"- {h}." for h in highlights]


def summarize_text(text: str) -> dict:
    client = get_mistral_client()
    prompt = (
        "Summarize the following educational content into concise bullet point highlights. "
        "Return 5-7 bullets focusing on core concepts, definitions, formulas, and examples.\n\n"
        f"CONTENT:\n{text}\n\n"
        "Return strictly as a JSON object with keys 'summary' (string) and 'highlights' (list of strings)."
    )
    if client is not None and config.mistral_model:
        try:
            resp = client.chat.complete(
                model=config.mistral_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            content = None
            if hasattr(resp, "choices") and resp.choices:
                msg = resp.choices[0].message
                if hasattr(msg, "content"):
                    content = msg.content
            if not content and isinstance(resp, dict):
                content = resp["choices"][0]["message"]["content"]
            import json
            try:
                data = json.loads(content)
                if isinstance(data, dict) and "summary" in data and "highlights" in data:
                    return {"summary": data["summary"], "highlights": data["highlights"]}
            except Exception:
                pass
        except Exception:
            pass

    # Fallback: heuristic
    highlights = _heuristic_summarize(text)
    summary = " ".join(h.strip("- ") for h in highlights) if highlights else text[:300]
    return {"summary": summary, "highlights": highlights}