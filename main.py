# main.py

import whisper
import spacy
import re
import phonenumbers
import entity_extractor
from flask import Flask, request, jsonify
import os
import threading
import audio_scheduler
import json

app = Flask(__name__)
model = whisper.load_model("base")
nlp = spacy.load("en_core_web_sm")

@app.route("/extract-details", methods=["POST"])
def extract_details():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]
    audio_path = f"temp_{audio_file.filename}"
    audio_file.save(audio_path)

    try:
        transcript = entity_extractor.transcribe_audio(audio_path)
        details = entity_extractor.extract_entities(transcript)
    finally:
        os.remove(audio_path)

    return jsonify({
        "transcript": transcript,
        "details": details
    })

def start_scheduler():
    with open("audio_scheduler_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    audio_scheduler.process_audio_files(config)

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    app.run(debug=True)

