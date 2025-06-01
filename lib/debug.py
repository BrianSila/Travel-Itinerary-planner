from db.models import session, Trip, Booking, Activity

def debug_trips():
    """Debug function to show all trips"""
    trips = session.query(Trip).all()
    for trip in trips:
        print(trip)
        for booking in trip.bookings:
            print("  ", booking)
        for activity in trip.activities:
            print("  ", activity)

if __name__ == '__main__':
    debug_trips()