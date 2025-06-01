from db.models import Trip, Booking, Activity, session
from datetime import datetime

def list_trips():
    trips = session.query(Trip).all()
    if not trips:
        print("No trips found.")
        return
    for trip in trips:
        print(f"{trip.id}: {trip.destination} ({trip.start_date} to {trip.end_date})")

def add_trip():
    destination = input("Destination: ")
    start_date = input("Start date (YYYY-MM-DD): ")
    end_date = input("End date (YYYY-MM-DD): ")
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        trip = Trip(destination=destination, start_date=start_date_obj, end_date=end_date_obj)
        session.add(trip)
        session.commit()
        print(f"Added trip to {destination} (ID: {trip.id})")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

def trip_details():
    try:
        trip_id = int(input("Enter trip ID: "))
        trip = session.query(Trip).get(trip_id)
        if not trip:
            print(f"No trip found with ID {trip_id}")
            return
        
        print(f"\nTrip to {trip.destination}")
        print(f"Dates: {trip.start_date} to {trip.end_date}\n")
        
        bookings = session.query(Booking).filter_by(trip_id=trip_id).all()
        print("Bookings:")
        for booking in bookings:
            print(f"  Flight: {booking.flight}")
            print(f"  Hotel: {booking.hotel}\n")
        
        activities = session.query(Activity).filter_by(trip_id=trip_id).order_by(Activity.date, Activity.time).all()
        if not activities:
            print("No activities planned.")
            return
        
        daily_schedule = {}
        for activity in activities:
            date_str = activity.date.strftime("%Y-%m-%d")
            if date_str not in daily_schedule:
                daily_schedule[date_str] = []
            daily_schedule[date_str].append(activity)
        
        print("Daily Schedule:")
        for date, activities_list in daily_schedule.items():
            print(f"\n{date}:")
            for activity in sorted(activities_list, key=lambda x: x.time):
                print(f"  {activity.time.strftime('%H:%M')} - {activity.name}")
    except ValueError:
        print("Invalid input. Please enter a number.")

def add_activity():
    try:
        trip_id = int(input("Enter trip ID: "))
        name = input("Activity name: ")
        date_str = input("Date (YYYY-MM-DD): ")
        time_str = input("Time (HH:MM): ")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.strptime(time_str, "%H:%M").time()
        activity = Activity(name=name, date=date, time=time, trip_id=trip_id)
        session.add(activity)
        session.commit()
        print(f"Added activity '{name}' to trip ID {trip_id}")
    except ValueError:
        print("Invalid date/time format. Please use YYYY-MM-DD for date and HH:MM for time.")

def add_booking():
    try:
        trip_id = int(input("Enter trip ID: "))
        flight = input("Flight details: ")
        hotel = input("Hotel details: ")
        trip = session.query(Trip).get(trip_id)
        if not trip:
            print(f"No trip found with ID {trip_id}")
            return
        booking = Booking(flight=flight, hotel=hotel, trip_id=trip_id)
        session.add(booking)
        session.commit()
        print(f"Added booking to trip ID {trip_id}")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main_menu():
    while True:
        print("\n=== Travel Itinerary Planner ===")
        print("1. List all trips")
        print("2. Add a new trip")
        print("3. View trip details")
        print("4. Add an activity to a trip")
        print("5. Add booking information")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")
        
        if choice == "1":
            list_trips()
        elif choice == "2":
            add_trip()
        elif choice == "3":
            trip_details()
        elif choice == "4":
            add_activity()
        elif choice == "5":
            add_booking()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 5.")

if __name__ == '__main__':
    main_menu()
