import os
import requests

BASE_URL = "https://app.ticketmaster.com/discovery/v2"

def _api_get(path: str, params: dict) -> dict:
    """Small wrapper to call Ticketmaster and return JSON (raises on HTTP errors)."""
    params = {k: v for k, v in params.items() if v not in ("", None)}
    r = requests.get(f"{BASE_URL}{path}", params=params, timeout=12)
    r.raise_for_status()
    return r.json()

def _extract_event_summary(item: dict) -> dict:
    """Normalize an event into the fields we use everywhere (incl. coords for maps)."""
    venues = item.get("_embedded", {}).get("venues", []) or []
    v = venues[0] if venues else {}

    lat = (v.get("location") or {}).get("latitude")
    lon = (v.get("location") or {}).get("longitude")
    if lat is None or lon is None:
        gp = v.get("geoPoint") or {}
        lat = lat or gp.get("latitude")
        lon = lon or gp.get("longitude")

    addr = v.get("address") or {}
    line1 = addr.get("line1")
    city = (v.get("city") or {}).get("name")
    state = (v.get("state") or {}).get("stateCode")
    country = (v.get("country") or {}).get("countryCode")

    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "url": item.get("url"),
        "start": item.get("dates", {}).get("start", {}).get("dateTime"),
        "venue": v.get("name"),
        "address": ", ".join([p for p in [line1, city, state, country] if p]),
        "city": city,
        "lat": float(lat) if lat not in (None, "") else None,
        "lon": float(lon) if lon not in (None, "") else None,
    }

def search_events(city: str = "", keyword: str = "") -> list[dict]:
    """Find events; returns simplified dicts with coords when available."""
    api_key = os.getenv("TICKETMASTER_API_KEY", "").strip()
    if not api_key:
        return []

    data = _api_get("/events.json", {
        "apikey": api_key,
        "size": 20,
        "sort": "date,asc",
        "locale": "*",
        "city": city or None,
        "keyword": keyword or None,
    })
    items = data.get("_embedded", {}).get("events", [])
    return [_extract_event_summary(it) for it in items]

def get_event(event_id: str) -> dict:
    """Fetch a single event (used by the details page + Leaflet)."""
    api_key = os.getenv("TICKETMASTER_API_KEY", "").strip()
    if not api_key:
        return {}
    data = _api_get(f"/events/{event_id}.json", {"apikey": api_key, "locale": "*"})
    return _extract_event_summary(data)
