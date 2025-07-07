if (Test-Path ".\venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated."
} else {
    Write-Host "Error: Virtual environment not found. Please create it first."
}