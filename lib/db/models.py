from sqlalchemy import create_engine, Column, String, Integer, Date, Time, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

engine = create_engine('sqlite:///travel_itinerary.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Table -1
class Trip( Base ):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)
    destinations = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    bookings = relationship('Booking', back_populates='trip', cascade='all, delete-orphan')
    activities = relationship('Activity', back_populates='trip', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Trip(id={self.id}, destination='{self.destinations}', dates='{self.start_date} to {self.end_date}')>"
    
# Table -2
class Booking( Base ):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    flight = Column(String)
    hotel = Column(String)
    trip_id = Column(Integer, ForeignKey('trips.id'))

    trip = relationship('Trip', back_populates='bookings')

    def __repr__(self):
        return f"<Booking(id={self.id}, flight='{self.flight}', hotel='{self.hotel}')>"

# Table -3
class Activity( Base ):
    __tablename__ = 'activities'

    id  = Column(Integer, primary_key=True)
    name = Column(String)
    time = Column(Time)
    date = Column(Date)
    trip_id = Column(Integer, ForeignKey('trips.id'))

    trip = relationship('Trip', back_populates='activities')

    def __repr__(self):
        return f"<Activity(id={self.id}, name='{self.name}', time='{self.time}')>"