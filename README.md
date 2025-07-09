# PythonScriptProject

A simple Python script project for audio transcription and entity extraction via a Flask API.

## Getting Started (Deployment Guide)

### 1. Prerequisites
- Python 3.8 or newer (https://www.python.org/downloads/)
- [ffmpeg](https://ffmpeg.org/download.html) installed and added to your system PATH


### 2. Setup Steps
#### Option 1: Automated Setup (Recommended for Windows)
1. **Clone or unzip this project folder on your target machine.**
2. **Open a PowerShell terminal in the project directory.**
3. **Run the setup script:**
   ```powershell
   .\setup_project.ps1
   ```
   This will create a virtual environment, install dependencies, and download the spaCy model.
4. **After setup, run the Flask API server:**
   ```powershell
   python main.py
   ```

#### Option 2: Manual Setup
1. **Create a virtual environment (recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Download the spaCy English model:**
   ```powershell
   python -m spacy download en_core_web_sm
   ```
4. **Run the Flask API server:**
   ```powershell
   python main.py
   ```


### 3. Using the API
- The server will run at `http://127.0.0.1:5000` by default.
- Send a POST request to `/extract-details` with an audio file (form field name: `audio`).

#### Example using `curl`:
```powershell
curl -X POST -F "audio=@yourfile.wav" http://127.0.0.1:5000/extract-details
```


### 4. Using the Scheduler and API Together
By default, running `python main.py` will now start both the Flask API and the scheduler in the same process.

1. Configure the scheduler by editing `audio_scheduler_config.json`:
   - `input_dir`: Folder to watch for new audio files (e.g., `in_progress`)
   - `output_dir`: Folder where JSON results will be written (e.g., `output`)
   - `archive_dir`: Folder where processed audio files will be moved (e.g., `archive`)
   - `poll_interval`: How often (in seconds) to check for new files

2. Place your audio files in the folder specified by `input_dir`.
3. Start both the API and scheduler together:
   ```powershell
   python main.py
   ```
4. The script will process each audio file, write a JSON result to `output_dir`, and move the audio file to `archive_dir`, while also serving the API.

### 5. Notes
- Make sure `ffmpeg` is installed and available in your system PATH. Whisper requires it for audio processing.
- For demonstration, you can zip this folder and share it. The recipient just needs to follow the steps above.
