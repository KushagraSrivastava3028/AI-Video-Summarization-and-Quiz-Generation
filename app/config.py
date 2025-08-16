import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class AppConfig:
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret")
    upload_dir: str = os.getenv("UPLOAD_DIR", "/workspace/storage/uploads")
    transcripts_dir: str = os.getenv("TRANSCRIPTS_DIR", "/workspace/storage/transcripts")
    results_dir: str = os.getenv("RESULTS_DIR", "/workspace/storage/results")

    # LLM providers
    mistral_api_key: str | None = os.getenv("MISTRAL_API_KEY")
    mistral_model: str = os.getenv("MISTRAL_MODEL", "open-mixtral-8x7b")

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    use_openai_whisper_api: bool = os.getenv("USE_OPENAI_WHISPER_API", "false").lower() == "true"

    # AWS optional
    enable_s3: bool = os.getenv("ENABLE_S3", "false").lower() == "true"
    aws_region: str | None = os.getenv("AWS_REGION")
    aws_bucket: str | None = os.getenv("AWS_S3_BUCKET")


config = AppConfig()

# Ensure storage directories exist
for directory in [config.upload_dir, config.transcripts_dir, config.results_dir]:
    os.makedirs(directory, exist_ok=True)