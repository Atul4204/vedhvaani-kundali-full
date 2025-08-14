# VedhVaani Kundali Engine - Full Feature (FastAPI)

This project provides:
- FastAPI endpoints for Kundali JSON and PDF
- Optional real calculations using pyswisseph (Swiss Ephemeris). If not installed, a deterministic fallback is used.
- North/South Indian SVG chart generator
- PDF report generation (ReportLab fallback; WeasyPrint supported if system deps installed)
- i18n (hi/mr/en) templates for report text

## Quick start (local)
1. python -m venv .venv
2. source .venv/bin/activate  # Windows: .venv\Scripts\activate
3. pip install -r requirements.txt
   - If you don't want pyswisseph or WeasyPrint, you can remove them from requirements before install.
4. uvicorn app.main:app --reload
5. Open http://127.0.0.1:8000/docs

## Railway deploy notes
- Railway's default Nix build may not include system libs needed by WeasyPrint; if you need robust HTML->PDF, use the Dockerfile (Railway supports Dockerfile builds).
- Alternatively, this project uses ReportLab (pure-Python) as a fallback and will work without system deps.

## Enabling real ephemeris (pyswisseph)
1. Download Swiss Ephemeris files into `app/ephe/` (se_* files).
2. Set environment variable `EPHE_PATH` to `/app/ephe` (or appropriate path).
3. Install pyswisseph (already in requirements) and restart.

## Endpoints
- GET / -> health
- GET /health -> health
- POST /kundali/basic -> JSON kundali (params: y,m,d,hour,lat,lon,lang,chart_style)
- POST /kundali/pdf -> PDF download (same JSON body as above)

## Notes
- This repo includes a deterministic fallback so the API always starts and can be tested without heavy deps.
- For production accuracy, follow the README steps to add ephemeris files and optionally switch to Docker build.
