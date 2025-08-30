"""
flights.py
Simple day-trip flight generator and filter.
This is placeholder logic for the MVP. Later swap `generate_options_for_day`
with calls to real APIs (Amadeus, Skyscanner, Duffel, etc.).
"""

from __future__ import annotations
from datetime import datetime, date, time
from typing import Dict, Any, List
from config import AppConfig
import hashlib

# demo airlines
AIRLINES = [
    "Delta", "United", "American", "Frontier",
    "Spirit", "Alaska", "JetBlue", "Southwest"
]

def normalize_iata(code: str) -> str:
    code = (code or "").upper().strip()
    return code[:3] if len(code) >= 3 else code

def airports_sane(origin: str, destination: str) -> bool:
    return origin != destination and len(origin) == 3 and len(destination) == 3

def search_daytrips(
    origin: str,
    destination: str,
    trip_date: str,
    morning_arrival: bool = True,
    evening_departure: bool = True,
    max_price: int | None = None,
) -> List[Dict[str, Any]]:
    """Main entry point for the app to fetch filtered options."""
    origin = normalize_iata(origin)
    destination = normalize_iata(destination)
    if not airports_sane(origin, destination):
        return []

    d = datetime.strptime(trip_date, "%Y-%m-%d").date()
    all_opts = generate_options_for_day(origin, destination, d)

    filtered = []
    for opt in all_opts:
        # enforce morning arrival cutoff
        if morning_arrival:
            arr_hour = int(opt["outbound"]["arrive_time_local"][11:13])
            if arr_hour > AppConfig.MORNING_ARRIVE_END_HOUR:
                continue
        # enforce evening return earliest departure
        if evening_departure:
            dep_hour = int(opt["return"]["depart_time_local"][11:13])
            if dep_hour < AppConfig.EVENING_DEPART_START_HOUR:
                continue
        # price filter
        if max_price is not None and opt["price_total"] > max_price:
            continue

        filtered.append(opt)

    # sort results
    filtered.sort(key=lambda r: (r["price_total"], r["total_duration_minutes"]))
    return filtered

def generate_options_for_day(origin: str, dest: str, d: date) -> List[Dict[str, Any]]:
    """
    Deterministic pseudo-options for a given day/route.
    Change this to call a live API later.
    """
    # simple fixed schedule patterns
    patterns = [
        dict(out_dep=time(6, 15), out_arr=time(9, 35),  ret_dep=time(19, 15), ret_arr=time(22, 35)),
        dict(out_dep=time(7, 30), out_arr=time(10, 50), ret_dep=time(18, 45), ret_arr=time(22, 5)),
        dict(out_dep=time(8, 5),  out_arr=time(11, 20), ret_dep=time(20, 5),  ret_arr=time(23, 25)),
    ]

    route_key = f"{origin}-{dest}-{d.isoformat()}"
    h = int(hashlib.sha1(route_key.encode()).hexdigest(), 16)

    results: List[Dict[str, Any]] = []
    for i, pat in enumerate(patterns):
        airline = AIRLINES[(h + i) % len(AIRLINES)]
        out_fn = 100 + (h + i) % 800
        ret_fn = 500 + ((h >> 4) + i) % 800

        out_dep_dt = datetime.combine(d, pat["out_dep"])
        out_arr_dt = datetime.combine(d, pat["out_arr"])
        ret_dep_dt = datetime.combine(d, pat["ret_dep"])
        ret_arr_dt = datetime.combine(d, pat["ret_arr"])

        out_dur = int((out_arr_dt - out_dep_dt).total_seconds() // 60)
        ret_dur = int((ret_arr_dt - ret_dep_dt).total_seconds() // 60)
        total_dur = out_dur + ret_dur

        base = 149 + (h % 60)     # base price between 149–208
        spread = i * 20           # bump price per option
        price_total = base + spread

        out_seg = {
            "airline": airline,
            "flight_number": str(out_fn),
            "origin": origin,
            "destination": dest,
            "depart_time_local": out_dep_dt.strftime("%Y-%m-%d %H:%M"),
            "arrive_time_local": out_arr_dt.strftime("%Y-%m-%d %H:%M"),
            "duration_minutes": out_dur,
        }
        ret_seg = {
            "airline": airline,
            "flight_number": str(ret_fn),
            "origin": dest,
            "destination": origin,
            "depart_time_local": ret_dep_dt.strftime("%Y-%m-%d %H:%M"),
            "arrive_time_local": ret_arr_dt.strftime("%Y-%m-%d %H:%M"),
            "duration_minutes": ret_dur,
        }

        result = {
            "outbound": out_seg,
            "return": ret_seg,
            "price_total": price_total,
            "currency": AppConfig.CURRENCY,
            "total_duration_minutes": total_dur,
            "morning_arrival": out_arr_dt.hour <= AppConfig.MORNING_ARRIVE_END_HOUR,
            "evening_departure": ret_dep_dt.hour >= AppConfig.EVENING_DEPART_START_HOUR,
            "deeplink": _google_flights_link(origin, dest, d),
            "tags": ["Morning arrival", "Evening return"],
        }
        results.append(result)

    return results

def _google_flights_link(origin: str, dest: str, d: date) -> str:
    ds = d.strftime("%Y-%m-%d")
    return f"https://www.google.com/travel/flights?hl=en#flt={origin}.{dest}.{ds}*{dest}.{origin}.{ds}"
