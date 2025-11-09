# PowerShell script to start the BananaPredictor API
Write-Host "Starting BananaPredictor API..." -ForegroundColor Green

# Activate virtual environment if it exists
if (Test-Path "..\venv\Scripts\Activate.ps1") {
    & "..\venv\Scripts\Activate.ps1"
}

# Start the API
python main.py

