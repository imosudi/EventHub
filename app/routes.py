from app import app, db
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os

# Import models and forms
from .models import  Event, Registration
from .forms import EventForm, RegistrationForm

# Routes
@app.route('/')
def index():
    """Home page showing upcoming events"""
    upcoming_events = Event.query.filter(Event.date >= datetime.today().date()).order_by(Event.date.asc()).limit(3).all()
    return render_template('index.html', events=upcoming_events)

@app.route('/events')
def events():
    """Page showing all events with filtering and search"""
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    # Build query based on filters
    query = Event.query.filter(Event.date >= datetime.today().date())
    
    if category:
        query = query.filter(Event.category == category)
    if search:
        query = query.filter(Event.title.contains(search) | Event.description.contains(search))
    
    events = query.order_by(Event.date.asc()).all()
    return render_template('events.html', events=events)

@app.route('/events/create', methods=['GET', 'POST'])
def create_event():
    """Create a new event"""
    form = EventForm()
    
    if form.validate_on_submit():
        # Convert date string to datetime object
        event_date = datetime.strptime(form.date.data, '%Y-%m-%d')
        
        # Create new event
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=event_date,
            time=form.time.data,
            location=form.location.data,
            category=form.category.data,
            max_attendees=form.max_attendees.data
        )
        
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('events'))
    
    return render_template('create_event.html', form=form)

@app.route('/events/<int:event_id>')
def event_detail(event_id):
    """Show event details"""
    event = Event.query.get_or_404(event_id)
    registrations_count = Registration.query.filter_by(event_id=event_id).count()
    return render_template('event_detail.html', event=event, registrations_count=registrations_count)

@app.route('/events/<int:event_id>/register', methods=['GET', 'POST'])
def register_event(event_id):
    """Register for an event"""
    event = Event.query.get_or_404(event_id)
    form = RegistrationForm()
    
    # Check if event is full
    registrations_count = Registration.query.filter_by(event_id=event_id).count()
    if registrations_count >= event.max_attendees:
        flash('This event is fully booked!', 'error')
        return redirect(url_for('event_detail', event_id=event_id))
    
    if form.validate_on_submit():
        # Check if email already registered for this event
        existing_registration = Registration.query.filter_by(
            event_id=event_id, 
            email=form.email.data
        ).first()
        
        if existing_registration:
            flash('This email is already registered for this event!', 'error')
            return render_template('register.html', form=form, event=event)
        
        # Create new registration
        registration = Registration(
            event_id=event_id,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        
        db.session.add(registration)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('event_detail', event_id=event_id))
    
    return render_template('register.html', form=form, event=event)

# API Routes
@app.route('/api/events')
def api_events():
    """JSON API endpoint for events"""
    events = Event.query.filter(Event.date >= datetime.today().date()).order_by(Event.date.asc()).all()
    events_data = []
    
    for event in events:
        events_data.append({
            'id': event.id,
            'title': event.title,
            'date': event.date.strftime('%Y-%m-%d'),
            'time': event.time,
            'location': event.location,
            'category': event.category,
            'description': event.description[:100] + '...' if len(event.description) > 100 else event.description
        })
    
    return jsonify(events_data)

@app.route('/api/events/<int:event_id>')
def api_event_detail(event_id):
    """JSON API endpoint for specific event"""
    event = Event.query.get_or_404(event_id)
    registrations_count = Registration.query.filter_by(event_id=event_id).count()
    
    event_data = {
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.strftime('%Y-%m-%d'),
        'time': event.time,
        'location': event.location,
        'category': event.category,
        'max_attendees': event.max_attendees,
        'current_attendees': registrations_count,
        'spots_remaining': event.max_attendees - registrations_count
    }
    
    return jsonify(event_data)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Create database tables
def create_tables():
    with app.app_context():
        db.create_all()

# Initialise the application
if __name__ == '__main__':
    create_tables()
    app.run(debug=True)