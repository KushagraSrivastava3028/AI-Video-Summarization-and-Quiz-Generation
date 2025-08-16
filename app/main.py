from __future__ import annotations
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from app.config import config
from app.utils.storage import generate_file_path, maybe_upload_to_s3
from app.utils.audio import extract_audio_if_video
from app.services.transcribe import transcribe_audio
from app.services.summarize import summarize_text
from app.services.quiz import generate_quiz


def create_app() -> Flask:
    app = Flask(__name__, template_folder=os.path.abspath("templates"), static_folder=os.path.abspath("static"))
    app.secret_key = config.secret_key

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/api/process")
    def process_file():
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400
        filename = secure_filename(file.filename)
        local_path = generate_file_path(config.upload_dir, filename)
        file.save(local_path)

        audio_path = extract_audio_if_video(local_path)
        transcript_result = transcribe_audio(audio_path)

        summary_data = summarize_text(transcript_result.text)
        quiz_data = generate_quiz(transcript_result.text)

        # Optionally upload artifacts
        transcript_path = os.path.join(config.transcripts_dir, os.path.basename(os.path.splitext(local_path)[0]) + ".txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript_result.text)
        maybe_upload_to_s3(transcript_path, s3_key_prefix="transcripts")

        return jsonify({
            "summary": summary_data["summary"],
            "highlights": summary_data["highlights"],
            "quiz": quiz_data,
            "transcription_model": transcript_result.model,
        })

    @app.post("/api/process-text")
    def process_text():
        payload = request.get_json(silent=True) or {}
        text = payload.get("text", "")
        if not text.strip():
            return jsonify({"error": "text is required"}), 400
        summary_data = summarize_text(text)
        quiz_data = generate_quiz(text)
        return jsonify({
            "summary": summary_data["summary"],
            "highlights": summary_data["highlights"],
            "quiz": quiz_data,
        })

    return app


app = create_app()