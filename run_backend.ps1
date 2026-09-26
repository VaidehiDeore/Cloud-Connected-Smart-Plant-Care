python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Set-Location backend
python -m uvicorn app:app --reload --port 8000
