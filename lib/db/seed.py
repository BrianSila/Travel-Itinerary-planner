from models import Trip, Booking, Activity, session
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

def clear_data():
    session.query(Trip).delete()
    session.query(Booking).delete()
    session.query(Activity).delete()
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
    for trip in trips:
        booking = Booking(
            flight=fake.airline(),
            hotel=fake.company(),
            trip_id=trip.id
        )
        session.add(booking)
    
    # Create activities for each trip
    activities = [
        "City Tour", "Museum Visit", "Beach Day", 
        "Hiking", "Food Tasting", "Shopping"
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
    clear_data()
    seed_data()
    print("Database seeded successfully!")