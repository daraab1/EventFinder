from flask import Blueprint, render_template, request
from .services.ticketmaster import search_events, get_event

bp = Blueprint("main", __name__)

@bp.get("/")
def home():
    return render_template("home.html")

@bp.get("/events")
def show_events():
    city = request.args.get("city", "").strip()
    keyword = request.args.get("keyword", "").strip()
    events = search_events(city=city, keyword=keyword)
    return render_template("results.html", events=events, city=city, keyword=keyword)

@bp.get("/event/<event_id>")
def event_detail(event_id):
    ev = get_event(event_id)
    return render_template("event_detail.html", ev=ev)
