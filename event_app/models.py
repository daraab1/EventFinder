from datetime import datetime
from . import db


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    tm_id = db.Column(db.String(64), unique=True)   # Ticketmaster ID
    name = db.Column(db.String(512), nullable=False)
    city = db.Column(db.String(256))
    start_datetime = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SavedEvent(db.Model):
    __tablename__ = "saved_event"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships (nice to show in a diagram)
    user = db.relationship("User", backref=db.backref("saved_events", lazy=True))
    event = db.relationship("Event", backref=db.backref("saved_by", lazy=True))
