from db.models import Trip, Booking, Activity, session, Base, engine
from datetime import datetime
from sqlalchemy import select, delete

def initialize_database():
    """Create database tables if they don't exist"""
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")

def list_trips():
    trips = session.scalars(select(Trip)).all()
    if not trips:
        print("No trips found.")
        return
    print("\n--- Your Trips ---")
    for trip in trips:
        print(f"{trip.id}: {trip.destination} ({trip.start_date} to {trip.end_date})")

def add_trip():
    print("\n--- Add New Trip ---")
    destination = input("Destination: ").strip()
    while True:
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        end_date = input("End date (YYYY-MM-DD): ").strip()
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            
            if end_date_obj < start_date_obj:
                print("Error: End date must be after start date.")
                continue
                
            trip = Trip(
                destination=destination, 
                start_date=start_date_obj, 
                end_date=end_date_obj
            )
            session.add(trip)
            session.commit()
            print(f"\n✓ Added trip to {destination} (ID: {trip.id})")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def update_trip():
    print("\n--- Update Trip ---")
    list_trips()
    try:
        trip_id = int(input("\nEnter trip ID to update: "))
        trip = session.get(Trip, trip_id)
        if not trip:
            print(f"\n✗ No trip found with ID {trip_id}")
            return

        print("\nLeave blank to keep current value:")
        new_destination = input(f"Destination [{trip.destination}]: ").strip()
        new_start_date = input(f"Start date [{trip.start_date}] (YYYY-MM-DD): ").strip()
        new_end_date = input(f"End date [{trip.end_date}] (YYYY-MM-DD): ").strip()

        if new_destination:
            Trip.destination = new_destination
        
        date_changed = False
        if new_start_date or new_end_date:
            try:
                start_date = trip.start_date
                end_date = trip.end_date
                
                if new_start_date:
                    start_date = datetime.strptime(new_start_date, "%Y-%m-%d").date()
                if new_end_date:
                    end_date = datetime.strptime(new_end_date, "%Y-%m-%d").date()
                
                if end_date < start_date:
                    print("Error: End date must be after start date.")
                    return
                
                trip.start_date = start_date
                trip.end_date = end_date
                date_changed = True
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                return

        session.commit()
        print("\n✓ Trip updated successfully!")
    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_trip():
    print("\n--- Delete Trip ---")
    list_trips()
    try:
        trip_id = int(input("\nEnter trip ID to delete: "))
        trip = session.get(Trip, trip_id)
        if not trip:
            print(f"\n✗ No trip found with ID {trip_id}")
            return

        # Show confirmation with trip details
        print(f"\nYou are about to delete this trip:")
        print(f"Destination: {trip.destination}")
        print(f"Dates: {trip.start_date} to {trip.end_date}")
        
        confirm = input("\nAre you sure? This will also delete all associated bookings and activities. (y/n): ").strip().lower()
        if confirm == 'y':
            # Delete associated bookings and activities first
            session.execute(delete(Booking).where(Booking.trip_id == trip_id))
            session.execute(delete(Activity).where(Activity.trip_id == trip_id))
            session.delete(trip)
            session.commit()
            print("\n✓ Trip deleted successfully!")
        else:
            print("\nDeletion cancelled.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def trip_details():
    print("\n--- Trip Details ---")
    list_trips()
    try:
        trip_id = int(input("\nEnter trip ID to view details: "))
        trip = session.get(Trip, trip_id)
        if not trip:
            print(f"\n✗ No trip found with ID {trip_id}")
            return
        
        print(f"\n=== Trip to {trip.destination} ===")
        print(f"Dates: {trip.start_date} to {trip.end_date}")
        print(f"Duration: {(trip.end_date - trip.start_date).days + 1} days\n")
        
        # Display bookings
        bookings = session.scalars(select(Booking).where(Booking.trip_id == trip_id)).all()
        if bookings:
            print("--- Bookings ---")
            for booking in bookings:
                print(f"✈ Flight: {booking.flight or 'Not specified'}")
                print(f"🏨 Hotel: {booking.hotel or 'Not specified'}\n")
        else:
            print("No bookings added yet.\n")
        
        # Display activities
        activities = session.scalars(
            select(Activity)
            .where(Activity.trip_id == trip_id)
            .order_by(Activity.date, Activity.time)
        ).all()
        
        if activities:
            print("--- Itinerary ---")
            daily_schedule = {}
            for activity in activities:
                date_str = activity.date.strftime("%Y-%m-%d")
                if date_str not in daily_schedule:
                    daily_schedule[date_str] = []
                daily_schedule[date_str].append(activity)
            
            for date, activities_list in daily_schedule.items():
                print(f"\n📅 {date}:")
                for activity in sorted(activities_list, key=lambda x: x.time):
                    print(f"  ⏰ {activity.time.strftime('%H:%M')} - {activity.name}")
        else:
            print("No activities planned yet.")
            
    except ValueError:
        print("Invalid input. Please enter a number.")

def add_activity():
    print("\n--- Add Activity ---")
    list_trips()
    try:
        trip_id = int(input("\nEnter trip ID to add activity: "))
        trip = session.get(Trip, trip_id)
        if not trip:
            print(f"\n✗ No trip found with ID {trip_id}")
            return
            
        name = input("Activity name: ").strip()
        while True:
            date_str = input("Date (YYYY-MM-DD): ").strip()
            time_str = input("Time (HH:MM): ").strip()
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                time = datetime.strptime(time_str, "%H:%M").time()
                
                if date < trip.start_date or date > trip.end_date:
                    print(f"\n✗ Date must be between {trip.start_date} and {trip.end_date}")
                    continue
                    
                activity = Activity(
                    name=name, 
                    date=date, 
                    time=time, 
                    trip_id=trip_id
                )
                session.add(activity)
                session.commit()
                print(f"\n✓ Added activity '{name}' to trip ID {trip_id}")
                break
            except ValueError:
                print("\n✗ Invalid format. Use YYYY-MM-DD for date and HH:MM for time.")
    except ValueError:
        print("\n✗ Invalid input. Please enter a number.")

def add_booking():
    print("\n--- Add Booking ---")
    list_trips()
    try:
        trip_id = int(input("\nEnter trip ID to add booking: "))
        trip = session.get(Trip, trip_id)
        if not trip:
            print(f"\n✗ No trip found with ID {trip_id}")
            return
            
        flight = input("Flight details (leave blank if none): ").strip()
        hotel = input("Hotel details (leave blank if none): ").strip()
        
        if not flight and not hotel:
            print("No booking details provided. Nothing was added.")
            return
            
        booking = Booking(
            flight=flight if flight else None,
            hotel=hotel if hotel else None,
            trip_id=trip_id
        )
        session.add(booking)
        session.commit()
        print("\n✓ Booking added successfully!")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main_menu():
    initialize_database()
    
    while True:
        print("\n=== 🌍 Travel Itinerary Planner ===")
        print("1. List all trips")
        print("2. Add a new trip")
        print("3. Update a trip")
        print("4. Delete a trip")
        print("5. View trip details")
        print("6. Add an activity to a trip")
        print("7. Add booking information")
        print("0. Exit")

        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == "1":
            list_trips()
        elif choice == "2":
            add_trip()
        elif choice == "3":
            update_trip()
        elif choice == "4":
            delete_trip()
        elif choice == "5":
            trip_details()
        elif choice == "6":
            add_activity()
        elif choice == "7":
            add_booking()
        elif choice == "0":
            print("\nThank you for using Travel Itinerary Planner. Goodbye! ✈")
            session.close()
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 7.")

if __name__ == '__main__':
    main_menu()