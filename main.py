# Restore Flask API for audio upload and extraction
from flask import Flask, request, jsonify
import entity_extractor
import os
import json

app = Flask(__name__)

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
    return jsonify({"transcript": transcript, "details": details})



def get_output_dir_from_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config.get('output_dir', 'output')


def run_scheduler():
    import audio_scheduler
    config_path = 'audio_scheduler_config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    audio_scheduler.process_audio_files(config)


@app.route("/export-excel", methods=["POST"])
def trigger_excel_export():
    import audio_scheduler
    success = audio_scheduler.export_excel()
    if success:
        return jsonify({"status": "Excel exported"})
    else:
        return jsonify({"status": "No data to export"}), 400

if __name__ == "__main__":
    import threading
    print("Starting scheduler in background thread...")
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    print("Starting Flask app...")
    app.run(debug=True)

