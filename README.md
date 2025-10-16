# Arrow Travel Tracker (Hybrid)

Hybrid architecture:
- **Streamlit backend** (app.py): authentication, add trips, CSV persistence, JSON endpoint
- **Vercel proxy** (api/proxy.js): fetches Streamlit JSON and adds CORS
- **React frontend** (frontend/): beautiful dashboard that reads live data from the proxy

## Quick local run (backend only)

1. Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # mac/linux
   venv\Scripts\activate         # windows
   pip install -r requirements.txt
