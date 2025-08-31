from datetime import date
from flask import Flask, jsonify, render_template, request, send_from_directory, url_for, redirect
from flights import search_daytrips  # uses your existing mock/search logic

app = Flask(__name__)

# ---------- helpers ----------
def today_iso() -> str:
    return date.today().isoformat()

@app.context_processor
def inject_defaults():
    # default_date is used by the index form (mobile + desktop)
    return {"default_date": today_iso()}

# ---------- pages ----------
@app.get("/")
def index():
    return render_template("index.html")

@app.get("/search")
def search_page():
    """HTML results page."""
    params = {
        "origin": (request.args.get("origin") or "").upper(),
        "destination": (request.args.get("destination") or "").upper(),
        "trip_date": request.args.get("trip_date") or today_iso(),
        "morning_arrival": request.args.get("morning_arrival") == "true",
        "evening_departure": request.args.get("evening_departure") == "true",
        "max_price": request.args.get("max_price"),
    }
    flights = search_daytrips(**params)
    return render_template("results.html", flights=flights, params=params)

@app.get("/api/search")
def api_search():
    """JSON API for programmatic access (mobile client, tests, etc.)."""
    params = {
        "origin": (request.args.get("origin") or "").upper(),
        "destination": (request.args.get("destination") or "").upper(),
        "trip_date": request.args.get("trip_date") or today_iso(),
        "morning_arrival": request.args.get("morning_arrival", "true").lower() == "true",
        "evening_departure": request.args.get("evening_departure", "true").lower() == "true",
        "max_price": request.args.get("max_price"),
    }
    flights = search_daytrips(**params)
    return jsonify({"ok": True, "params": params, "flights": flights})

@app.get("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")

@app.get("/pricing")
def pricing():
    return render_template("pricing.html")

@app.get("/faq")
def faq():
    return render_template("faq.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/contact")
def contact():
    return render_template("contact.html")

# ---------- assets / PWA (mobile-friendly install) ----------
@app.get("/manifest.webmanifest")
def webmanifest():
    # serve the manifest from /static so browsers can install to home screen
    return send_from_directory("static", "manifest.webmanifest", mimetype="application/manifest+json")

@app.get("/sw.js")
def service_worker():
    # basic service worker (if you add static/sw.js)
    return send_from_directory("static", "sw.js", mimetype="application/javascript")

# Optional: serve logo by path if any template calls url_for('logo')
@app.get("/logo.svg")
def logo():
    return send_from_directory("static", "logo.svg", mimetype="image/svg+xml")


# ---------- error pages ----------
@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Dev server (Render/production uses gunicorn via Procfile)
    app.run(host="0.0.0.0", port=5050, debug=True)
