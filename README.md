# EduVideo Summarizer & Quiz Generator

This project ingests educational videos, transcribes them, summarizes the content into concise highlights, and generates quizzes to aid comprehension.

- Web UI and REST API built with Flask
- Transcription via Whisper (API or local optional)
- Summarization and quiz generation via Mixtral (Mistral API) with local fallback
- Optional AWS S3 storage integration

## Quickstart

1. Create and configure environment

```bash
cp .env.example .env
make install  # base deps only
# Optionally, for local models (large):
make install-all
```

2. Run the web app

```bash
make run
# Open http://localhost:8000
```

3. Run tests

```bash
make test
```

## Configuration

Set env vars in `.env`:
- `MISTRAL_API_KEY`: Use Mixtral via Mistral API when available
- `OPENAI_API_KEY` and `USE_OPENAI_WHISPER_API=true` to use Whisper API for transcription
- If not set, the app falls back to local or heuristic summarization/quiz generation
- Optional S3: set `ENABLE_S3=true`, `AWS_REGION`, `AWS_S3_BUCKET`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`

## Notes on Optional Dependencies

Local Whisper and transformer models are heavy and may require `ffmpeg` and `torch`.
Install them only if needed:

```bash
pip install -r requirements-optional.txt
```

## API

- `POST /api/process` (multipart/form-data): field `file` with video/audio; returns summary and quiz
- `POST /api/process-text` (JSON): `{ "text": "..." }` to bypass transcription
- `GET /api/health`: health check

## License
MIT