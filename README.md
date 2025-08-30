# Daytrippr (MVP)

Daytrippr helps you find **same-day flights** — morning arrivals, evening returns — in one clean search.

This is an MVP built with **Flask + Tailwind**, using mocked flight data for now. Later, real flight APIs (Amadeus, Skyscanner, Duffel, etc.) can be plugged in without changing the UI.

---

## 🚀 Features
- Search by origin, destination, date, and budget
- Filter for morning arrivals / evening returns
- Mock flight results with airlines, flight numbers, times, and prices
- Google Flights deeplink for booking
- Clean Tailwind-styled UI

---

## 🛠️ Tech Stack
- **Backend:** Python 3.12, Flask, Gunicorn  
- **Frontend:** Jinja2 templates, TailwindCSS  
- **Deployment:** Render / Railway / any WSGI-friendly host

---

## 💻 Run Locally
Clone the repo:
```bash
git clone https://github.com/affaan02/daytrippr.git
cd daytrippr
