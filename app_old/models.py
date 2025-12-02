# app/models.py
from datetime import datetime
from . import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tm_id = db.Column(db.String(64), unique=True)   # Ticketmaster id (optional for now)
    name = db.Column(db.String(512))
    city = db.Column(db.String(256))
    start_datetime = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
