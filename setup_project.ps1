# setup_project.ps1
# PowerShell script to set up the Python project for deployment/demo

Write-Host "Creating virtual environment..."
python -m venv venv

Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate

Write-Host "Installing dependencies..."
pip install -r requirements.txt

Write-Host "Downloading spaCy English model..."
python -m spacy download en_core_web_sm

Write-Host "Setup complete!"
Write-Host "Please ensure ffmpeg is installed and added to your system PATH."
Write-Host "To run the server:"
Write-Host "python main.py"
