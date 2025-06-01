import click
from db.models import Trip, Booking, Activity, session
from datetime import datetime

@click.group()
def cli():
    """Travel Itinerary Planner CLI"""
    pass

@cli.command()
def list_trips():
    """List all trips"""
    trips = session.query(Trip).all()
    if not trips:
        click.echo("No trips found.")
        return
    
    for trip in trips:
        click.echo(f"{trip.id}: {trip.destination} ({trip.start_date} to {trip.end_date})")

@cli.command()
@click.option('--destination', prompt='Destination', help='Trip destination')
@click.option('--start-date', prompt='Start date (YYYY-MM-DD)', help='Start date')
@click.option('--end-date', prompt='End date (YYYY-MM-DD)', help='End date')
def add_trip(destination, start_date, end_date):
    """Add a new trip"""
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        trip = Trip(
            destination=destination,
            start_date=start_date,
            end_date=end_date
        )
        session.add(trip)
        session.commit()
        click.echo(f"Added trip to {destination} (ID: {trip.id})")
    except ValueError:
        click.echo("Invalid date format. Please use YYYY-MM-DD.")

@cli.command()
@click.argument('trip_id', type=int)
def trip_details(trip_id):
    """View details of a specific trip"""
    trip = session.query(Trip).get(trip_id)
    if not trip:
        click.echo(f"No trip found with ID {trip_id}")
        return
    
    # Display trip info
    click.echo(f"\nTrip to {trip.destination}")
    click.echo(f"Dates: {trip.start_date} to {trip.end_date}\n")
    
    # Display bookings
    bookings = session.query(Booking).filter_by(trip_id=trip_id).all()
    click.echo("Bookings:")
    for booking in bookings:
        click.echo(f"  Flight: {booking.flight}")
        click.echo(f"  Hotel: {booking.hotel}\n")
    
    # Display activities grouped by date (using dict for daily schedules)
    activities = session.query(Activity).filter_by(trip_id=trip_id).order_by(Activity.date, Activity.time).all()
    
    if not activities:
        click.echo("No activities planned.")
        return
    
    daily_schedule = {}
    for activity in activities:
        date_str = activity.date.strftime("%Y-%m-%d")
        if date_str not in daily_schedule:
            daily_schedule[date_str] = []
        daily_schedule[date_str].append(activity)
    
    click.echo("Daily Schedule:")
    for date, activities_list in daily_schedule.items():
        click.echo(f"\n{date}:")
        # Using list sorting by time
        activities_sorted = sorted(activities_list, key=lambda x: x.time)
        for activity in activities_sorted:
            click.echo(f"  {activity.time.strftime('%H:%M')} - {activity.name}")

@cli.command()
@click.argument('trip_id', type=int)
@click.option('--name', prompt='Activity name', help='Name of the activity')
@click.option('--date', prompt='Date (YYYY-MM-DD)', help='Date of the activity')
@click.option('--time', prompt='Time (HH:MM)', help='Time of the activity')
def add_activity(trip_id, name, date, time):
    """Add an activity to a trip"""
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time, "%H:%M").time()
        
        activity = Activity(
            name=name,
            date=date_obj,
            time=time_obj,
            trip_id=trip_id
        )
        session.add(activity)
        session.commit()
        click.echo(f"Added activity '{name}' to trip ID {trip_id}")
    except ValueError:
        click.echo("Invalid date/time format. Please use YYYY-MM-DD for date and HH:MM for time.")

@cli.command()
@click.argument('trip_id', type=int)
@click.option('--flight', prompt='Flight details', help='Flight information')
@click.option('--hotel', prompt='Hotel details', help='Hotel information')
def add_booking(trip_id, flight, hotel):
    """Add booking information to a trip"""
    trip = session.query(Trip).get(trip_id)
    if not trip:
        click.echo(f"No trip found with ID {trip_id}")
        return
    
    booking = Booking(
        flight=flight,
        hotel=hotel,
        trip_id=trip_id
    )
    session.add(booking)
    session.commit()
    click.echo(f"Added booking to trip ID {trip_id}")

if __name__ == '__main__':
    cli()