@echo off
echo ==========================================
echo SmartCart AI Service Setup (Windows)
echo ==========================================
echo.

echo Step 1: Creating Python virtual environment...
python -m venv .venv

echo Step 2: Activating virtual environment...
call .venv\Scripts\activate.bat

echo Step 3: Installing dependencies...
pip install -r requirements.txt

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env and add your API keys
echo 2. Run: psql -U your_user -d smartcart -f setup_database.sql
echo 3. Run: python ingest.py (to load products)
echo 4. Run: uvicorn main:app --reload --port 8001
echo.
pause