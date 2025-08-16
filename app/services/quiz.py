from __future__ import annotations
from typing import List, Dict
from app.config import config
from app.utils.llm_clients import get_mistral_client


def _heuristic_quiz_from_text(text: str, num_questions: int = 5) -> List[Dict]:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    questions = []
    for idx, s in enumerate(sentences[:num_questions]):
        q = f"What is the main idea of: '{s[:80]}...?" if len(s) > 80 else f"What is the main idea of: '{s}'?"
        options = [
            f"It explains: {s[:60]}",
            "It asks an unrelated question",
            "It provides a historical anecdote",
            "It describes a counterexample",
        ]
        questions.append({
            "question": q,
            "options": options,
            "answer": options[0],
        })
    return questions


def generate_quiz(text: str, num_questions: int = 6) -> List[Dict]:
    client = get_mistral_client()
    prompt = (
        "From the following educational content, create a quiz with multiple-choice questions.\n"
        f"Generate {num_questions} questions. Each question should have exactly 4 options and one correct answer.\n"
        "Return strictly as JSON: a list of objects with keys 'question', 'options' (list of 4 strings), and 'answer' (string equal to one option).\n\n"
        f"CONTENT:\n{text}"
    )
    if client is not None and config.mistral_model:
        try:
            resp = client.chat.complete(
                model=config.mistral_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            content = None
            if hasattr(resp, "choices") and resp.choices:
                msg = resp.choices[0].message
                if hasattr(msg, "content"):
                    content = msg.content
            if not content and isinstance(resp, dict):
                content = resp["choices"][0]["message"]["content"]
            import json
            data = json.loads(content)
            if isinstance(data, list) and data:
                return data
        except Exception:
            pass
    return _heuristic_quiz_from_text(text, num_questions=num_questions)