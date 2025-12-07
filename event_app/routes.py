from flask import Blueprint, render_template, request
from datetime import datetime
from . import db
from .models import Event, User, SavedEvent
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

    #  search and after log it into event + saved_event tables
    if city or keyword:
       
        demo_email = "dxh37@pct.edu"
        user = User.query.filter_by(email=demo_email).first()
        if not user:
            user = User(email=demo_email, name="Daraab")
            db.session.add(user)
            db.session.commit()   

        search_name = keyword or (f"Search in {city}" if city else "Search")
        tm_id = f"search-{datetime.utcnow().timestamp()}"

        ev_row = Event(
            tm_id=tm_id,
            name=search_name,
            city=city or None,
            start_datetime=datetime.utcnow(),
        )
        db.session.add(ev_row)
        db.session.commit()      

        saved = SavedEvent(
            user_id=user.id,
            event_id=ev_row.id,
            created_at=datetime.utcnow(),
        )
        db.session.add(saved)
        db.session.commit()

    return render_template("results.html", events=events, city=city, keyword=keyword)


@bp.get("/event/<event_id>")
def event_detail(event_id):
    ev = get_event(event_id)
    return render_template("event_detail.html", ev=ev)
