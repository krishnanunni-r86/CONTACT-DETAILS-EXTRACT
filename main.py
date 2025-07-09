
# main.py
# Main entry point for the Contact Details Extraction API and audio scheduler.


import whisper  # Speech-to-text model
import spacy    # NLP for entity extraction
import re
import phonenumbers
import entity_extractor  # Custom module for audio transcription and entity extraction
from flask import Flask, request, jsonify  # Web API
import os
import threading
import audio_scheduler  # Custom module for scheduled audio processing
import json


# Initialize Flask app and models
app = Flask(__name__)
model = whisper.load_model("base")  # Load Whisper model for transcription
nlp = spacy.load("en_core_web_sm")  # Load spaCy model for NLP


# API endpoint for extracting details from uploaded audio
@app.route("/extract-details", methods=["POST"])
def extract_details():
    # Check if audio file is present in the request
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]
    audio_path = f"temp_{audio_file.filename}"
    audio_file.save(audio_path)

    try:
        # Transcribe audio and extract entities
        transcript = entity_extractor.transcribe_audio(audio_path)
        details = entity_extractor.extract_entities(transcript)
    finally:
        # Clean up temporary file
        os.remove(audio_path)

    return jsonify({
        "transcript": transcript,
        "details": details
    })


# Function to start the background audio scheduler
def start_scheduler():
    with open("audio_scheduler_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    audio_scheduler.process_audio_files(config)


# Main entry point: start scheduler in background and run Flask app
if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    app.run(debug=True)

