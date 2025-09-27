from datetime import datetime
from app import db

class Event(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date        = db.Column(db.DateTime, nullable=False)
    time        = db.Column(db.String(10), nullable=False)
    location    = db.Column(db.String(200), nullable=False)
    category    = db.Column(db.String(50), nullable=False)
    max_attendees = db.Column(db.Integer, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    
    registrations = db.relationship('Registration', backref='event', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.title}>'

class Registration(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    event_id    = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    name        = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(100), nullable=False)
    phone       = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Registration {self.name} for Event {self.event_id}>'
    