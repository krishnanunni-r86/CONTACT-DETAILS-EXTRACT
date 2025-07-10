# Contact Details Extraction API - Slide Deck (Markdown)

---
## Slide 1: Solution Overview
- Automates extraction of contact details from audio files
- Uses advanced speech-to-text and NLP
- Delivers structured data: Name, Address, Email, Phone, Location

---
## Slide 2: Key Features
- Audio transcription with state-of-the-art models
- Entity extraction for contact details
- Automated folder monitoring and scheduling
- REST API for real-time extraction
- Archiving of processed files

---
## Slide 3: Workflow
1. Audio files placed in input directory or uploaded via API
2. System transcribes and extracts details
3. Results saved as JSON in output directory
4. Processed files archived
5. API endpoint `/extract-details` for on-demand use

---
## Slide 4: Example Output
```
{
  "transcript": "Hi, my name is Jake Harrison. I live at 327, Elk Meadow Drive Austin, Texas, 78745. You can reach me at jake.herison@example.com or call me at 512-555-7284.",
  "details": {
    "NAME": [
      {"value": "Jake Harrison", "confidence": 0.95}
    ],
    "GPE": [
      {"value": "Austin", "confidence": 0.93},
      {"value": "Texas", "confidence": 0.93}
    ],
    "ADDRESS": [
      {"value": "327, Elk Meadow Drive Austin, Texas, 78745", "confidence": 0.88}
    ],
    "EMAIL": [
      {"value": "jake.herison@example.com", "confidence": 0.99}
    ],
    "PHONE": [
      {"value": "+1 512-555-7284", "confidence": 0.99}
    ]
  }
}
```

---
## Slide 5: Business Value
- Saves time and reduces manual errors
- Scalable for high volumes
- Integrates with business systems (CRM, support, compliance)
- Maintains audit trail of processed data

---
## Slide 6: Configuration & Requirements
- Input, output, and archive directories configurable
- API endpoint: `/extract-details`
- Supported audio formats: WAV, MP3, M4A, FLAC, OGG
- Python 3.8+ and required packages

---
## Slide 7: Contact
For more information or a demo, contact the project team.
