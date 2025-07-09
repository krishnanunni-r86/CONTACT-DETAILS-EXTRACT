
# Import required libraries
import os
import time
import shutil
import json
import entity_extractor  # Custom module for transcription and extraction



# Process audio files in a scheduled loop
def process_audio_files(config):
    input_dir = config["input_dir"]
    output_dir = config["output_dir"]
    archive_dir = config["archive_dir"]
    poll_interval = config.get("poll_interval", 10)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(archive_dir, exist_ok=True)
    while True:
        # List all supported audio files in the input directory
        audio_files = [f for f in os.listdir(input_dir) if f.lower().endswith((".wav", ".mp3", ".m4a", ".flac", ".ogg"))]
        for audio_file in audio_files:
            input_path = os.path.join(input_dir, audio_file)
            print(f"Processing: {input_path}")
            try:
                # Transcribe audio and extract entities
                transcript = entity_extractor.transcribe_audio(input_path)
                details = entity_extractor.extract_entities(transcript)
                output_data = {
                    "transcript": transcript,
                    "details": details
                }
                # Save extracted details as JSON
                output_filename = os.path.splitext(audio_file)[0] + ".json"
                output_path = os.path.join(output_dir, output_filename)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(output_data, f, ensure_ascii=False, indent=2)
                # Move the file to archive (overwrite if exists)
                if os.path.exists(input_path):
                    archive_path = os.path.join(archive_dir, audio_file)
                    if os.path.exists(archive_path):
                        os.remove(archive_path)
                    shutil.move(input_path, archive_path)
                    print(f"Processed and archived: {audio_file}")
            except Exception as e:
                print(f"Error processing {audio_file}: {e}")
                # If the file still exists and was not processed, do not try to move it again
        # Wait before next poll
        time.sleep(poll_interval)


# Main entry point for standalone execution
if __name__ == "__main__":
    # Load config from external JSON file
    with open("audio_scheduler_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    process_audio_files(config)
