from __future__ import annotations
import os
import uuid
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from typing import Optional
from app.config import config


def generate_file_path(directory: str, original_filename: str) -> str:
    base, ext = os.path.splitext(original_filename)
    unique_name = f"{base}-{uuid.uuid4().hex[:8]}{ext}"
    return os.path.join(directory, unique_name)


def maybe_upload_to_s3(local_path: str, s3_key_prefix: str = "") -> Optional[str]:
    if not config.enable_s3 or not config.aws_region or not config.aws_bucket:
        return None
    try:
        s3_client = boto3.client("s3", region_name=config.aws_region)
        key = os.path.join(s3_key_prefix.strip("/"), os.path.basename(local_path)) if s3_key_prefix else os.path.basename(local_path)
        s3_client.upload_file(local_path, config.aws_bucket, key)
        return f"s3://{config.aws_bucket}/{key}"
    except (BotoCoreError, ClientError):
        return None