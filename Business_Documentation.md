# Contact Details Extraction API - Business Documentation

## Overview
This solution automates the extraction of contact details from audio files. It leverages advanced speech-to-text and natural language processing (NLP) technologies to transcribe audio and extract structured information such as names, addresses, emails, and phone numbers.

## Key Features
- **Audio Transcription:** Converts speech in audio files to text using state-of-the-art models.
- **Entity Extraction:** Identifies and extracts key contact details (Name, Address, Email, Phone, Location) from the transcribed text.
- **Automated Scheduling:** Monitors a specified folder for new audio files and processes them automatically.
- **API Access:** Provides a REST API endpoint for on-demand extraction via HTTP POST requests.
- **Archiving:** Moves processed audio files to an archive folder to prevent duplicate processing.

1. **Audio File Ingestion:**
   - Place audio files in the configured input directory, or upload via the API.
2. **Processing:**
   - The system transcribes the audio and extracts contact details.
   - Results are saved as JSON files in the output directory.
3. **Archiving:**
   - Processed audio files are moved to the archive directory.
4. **API Usage:**
   - Send a POST request with an audio file to `/extract-details` to receive extracted details in real time.

## Example Output
```
{
  "transcript": "Hi, my name is Jake Harrison. I live at 327, Elk Meadow Drive Austin, Texas, 78745. You can reach me at jake.herison@example.com or call me at 512-555-7284.",
  "details": {
    "NAME": ["Jake Harrison"],
    "GPE": ["Austin", "Texas"],
    "ADDRESS": ["327, Elk Meadow Drive Austin, Texas, 78745"],
    "EMAIL": ["jake.herison@example.com"],

## Business Value

## Configuration
- **API Endpoint:** `/extract-details` for real-time extraction.

## Requirements
- Audio files in supported formats (WAV, MP3, M4A, FLAC, OGG)
3. **Archiving and Output Organization:**
- Python 3.8+
- Required Python packages (see `requirements.txt`)

## Contact
For more information or a demo, please contact the project team.
