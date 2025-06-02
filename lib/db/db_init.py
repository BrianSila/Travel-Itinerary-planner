# db_init.py
from sqlalchemy import create_engine
from models import Base  # Assuming your models are in models.py

def initialize_database():
    engine = create_engine('sqlite:///travel_itinerary.db')
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == '__main__':
    initialize_database()