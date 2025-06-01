from datetime import datetime
from db.models import session, Trip, Activity

def get_trip_by_id(trip_id):
    """Helper function to get a trip by ID"""
    return session.query(Trip).get(trip_id)

def get_activities_for_trip(trip_id):
    """
    Helper function to get activities for a trip, sorted by date and time
    Returns a list of activities sorted by date and time
    """
    activities = session.query(Activity).filter_by(trip_id=trip_id).all()
    # Using tuple for sorting keys (date, time)
    return sorted(activities, key=lambda x: (x.date, x.time))

def create_daily_schedule(activities):
    """
    Create a daily schedule dictionary from activities
    Returns a dict with dates as keys and lists of activities as values
    """
    schedule = {}
    for activity in activities:
        date_str = activity.date.strftime("%Y-%m-%d")
        if date_str not in schedule:
            schedule[date_str] = []
        schedule[date_str].append({
            'time': activity.time.strftime('%H:%M'),
            'name': activity.name
        })
    return schedule

def validate_date(date_str):
    """
    Validate date format (YYYY-MM-DD)
    Returns datetime.date object if valid, None otherwise
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

def validate_time(time_str):
    """
    Validate time format (HH:MM)
    Returns datetime.time object if valid, None otherwise
    """
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except (ValueError, TypeError):
        return None