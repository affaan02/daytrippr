# Tripski (MVP)

Day-trip flight finder MVP (mock data).

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python app.py
# open http://127.0.0.1:5000
```

## Deploy (anywhere that runs Python)

- Use `gunicorn` / `uvicorn` (for Flask, gunicorn works): `gunicorn app:app -b 0.0.0.0:$PORT`
- Heroku-style `Procfile` included: `web: gunicorn app:app`
- Expose `PORT` env var as required by your platform.

## Notes

- Data is mocked in `flights.py`. Swap `generate_options_for_day` with a real provider later.
- Morning arrival / evening return filters are enforced in code using `AppConfig`.

## API

`GET /api/search?origin=SFO&destination=DTW&trip_date=2025-09-20&morning_arrival=true&evening_departure=true&max_price=220`

Deployed from VS Code on Sat Aug 30 15:45:49 PDT 2025
