from models import Trip, Booking, Activity, session, Base, engine
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

def create_tables():
    """Create all database tables before seeding"""
    Base.metadata.create_all(engine)

def clear_data():
    """Clear existing data from all tables"""
    # Note the order matters due to foreign key constraints
    session.query(Activity).delete()
    session.query(Booking).delete()
    session.query(Trip).delete()
    session.commit()

def seed_data():
    # Create trips
    trips = []
    for _ in range(3):
        start_date = fake.date_between(start_date='-30d', end_date='+30d')
        end_date = start_date + timedelta(days=random.randint(3, 14))
        trip = Trip(
            destination=fake.city(),
            start_date=start_date,
            end_date=end_date
        )
        trips.append(trip)
        session.add(trip)
    
    session.commit()
    
    # Create bookings for each trip
    airlines = ["Delta", "United", "American", "Southwest", "JetBlue", "Spirit"]
    hotel_chains = ["Marriott", "Hilton", "Hyatt", "InterContinental", "Accor", "Wyndham"]
    
    for trip in trips:
        booking = Booking(
            flight=f"{random.choice(airlines)} {random.randint(100, 999)}",  # Generate flight info
            hotel=f"{random.choice(hotel_chains)} {fake.city()}",  # Generate hotel info
            trip_id=trip.id
        )
        session.add(booking)
    
    # Create activities for each trip
    activities = [
        "City Tour", "Museum Visit", "Beach Day", 
        "Hiking", "Food Tasting", "Shopping",
        "Concert", "Theater Show", "Wine Tasting",
        "Boat Cruise", "Cooking Class", "Local Market"
    ]
    
    for trip in trips:
        current_date = trip.start_date
        while current_date <= trip.end_date:
            num_activities = random.randint(1, 3)
            for _ in range(num_activities):
                activity = Activity(
                    name=random.choice(activities),
                    time=datetime.strptime(f"{random.randint(9, 18)}:00", "%H:%M").time(),
                    date=current_date,
                    trip_id=trip.id
                )
                session.add(activity)
            current_date += timedelta(days=1)
    
    session.commit()

if __name__ == '__main__':
    create_tables()
    clear_data()
    seed_data()
    print("Database seeded successfully!")