import os
from datetime import datetime, timedelta, date
from flask import Flask, render_template, request, jsonify, send_from_directory
from flights import search_daytrips, airports_sane, normalize_iata
from config import AppConfig

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(AppConfig)

@app.get("/")
def index():
    today = date.today()
    default_date = today + timedelta(days=7)
    return render_template(
        "index.html",
        default_date=default_date.strftime("%Y-%m-%d"),
        sample_origins=["SFO", "SJC", "OAK", "DTW", "LAX", "ORD", "ATL", "PHX", "MCO"],
        sample_dests=["DTW", "SFO", "SEA", "LAX", "LAS", "PHX", "DEN", "BOS", "JFK"],
    )

@app.get("/search")
def search_page():
    params = _read_params()
    results = search_daytrips(**params)
    return render_template("results.html", results=results, params=params, count=len(results))

@app.get("/api/search")
def api_search():
    params = _read_params()
    results = search_daytrips(**params)
    return jsonify({"count": len(results), "results": results, "params": params})

@app.get("/logo.svg")
def logo():
    return send_from_directory("static", "logo.svg", mimetype="image/svg+xml")

# ---- extra pages ----
@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")

@app.get("/pricing")
def pricing():
    return render_template("pricing.html")

@app.get("/faq")
def faq():
    return render_template("faq.html")

@app.get("/contact")
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

def _read_params():
    origin = normalize_iata(request.args.get("origin", "SFO"))
    destination = normalize_iata(request.args.get("destination", "DTW"))
    trip_date = request.args.get("trip_date") or (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    try:
        datetime.strptime(trip_date, "%Y-%m-%d")
    except ValueError:
        trip_date = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")

    morning_arrival = request.args.get("morning_arrival", "true").lower() != "false"
    evening_departure = request.args.get("evening_departure", "true").lower() != "false"
    max_price = request.args.get("max_price", "").strip()
    max_price = int(max_price) if max_price.isdigit() else None

    return dict(
        origin=origin,
        destination=destination,
        trip_date=trip_date,
        morning_arrival=morning_arrival,
        evening_departure=evening_departure,
        max_price=max_price,
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5050"))  # defaults to 5050 now
    app.run(host="0.0.0.0", port=port, debug=True)
