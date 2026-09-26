# PlantCare - Updated Working Version

This package contains the cleaned-up version of the Cloud-Connected Smart Plant Care project.

## What was fixed

- Overview, Analytics and Alerts now use one consistent sidebar navigation.
- Analytics is clickable from Overview and Alerts is clickable from Overview and Analytics.
- Alerts are displayed on their own page instead of being embedded in Overview.
- Active alerts have a visible **Acknowledge** button.
- Automatic watering no longer immediately resolves the low-moisture alert.
- Low-moisture alerts are deduplicated while the condition is unresolved.
- Acknowledged alerts remain acknowledged until a healthy sensor reading resolves them.
- SQLite datetime handling is normalized to avoid naive/aware datetime comparison errors.
- Frontend source uses ASCII-safe UI text and Lucide icons, removing the mojibake symbols seen in the previous build.
- `bcrypt==4.0.1` is pinned for compatibility with Passlib 1.7.4.
- Overview no longer contains the full alert list; use the Alerts page for alert management.

## Important: your existing data

This source package does **not** contain your local SQLite database or `.env` file.

When copying these files over your current project, keep your existing:

- `backend/plant_care.db`
- `.env`
- `.venv` if you want to keep the existing Python environment
- `frontend/node_modules` if already installed

## PowerShell startup

### Terminal 1 - Backend

```powershell
cd "D:\EDC Projects\Cloud-Connected-Smart-Plant-Care"
.\.venv\Scripts\Activate.ps1
cd backend
python -m uvicorn app:app --reload --port 8000
```

### Terminal 2 - Sensor simulator

```powershell
cd "D:\EDC Projects\Cloud-Connected-Smart-Plant-Care"
.\.venv\Scripts\Activate.ps1
cd sensor_simulator
python simulator.py --url http://127.0.0.1:8000 --interval 5
```

### Terminal 3 - Frontend

```powershell
cd "D:\EDC Projects\Cloud-Connected-Smart-Plant-Care\frontend"
npm run dev
```

Open `http://localhost:5173`.

## Test order

1. Login.
2. Confirm live sensor cards are updating.
3. Click **Analytics**.
4. Return to Overview.
5. Click **Alerts**.
6. Set moisture threshold to 30% if necessary.
7. Let the simulator cross below the threshold.
8. Confirm an ACTIVE low-moisture alert appears.
9. Click **Acknowledge**.
10. Confirm it becomes **ACKNOWLEDGED** and later **RESOLVED** after a healthy reading.
11. Test **Water now** and confirm watering history and moisture increase.
