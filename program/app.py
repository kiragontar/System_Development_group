import mysql.connector # To connect with the MYsql table created in MYSQL workbench.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models.booking import Booking
from models.cinema_film import CinemaFilm
from models.cinema import Cinema
from models.city_pricing import CityPricing
from models.city import City
from models.film import Film
from enums import PaymentStatus
from models.payment import Payment
from models.permissions import Permission
from models.role import Role
from models.screen import Screen
from models.screening import Screening
from models.seat import Seat
from models.ticket import Ticket
from models.user import User
from models import Base  # Import your Base metadata

conn = mysql.connector.connect(
    host="localhost",
    user="MickelUWE",
    password="g<bI1Z11iC]c", 
    database="Cinema"
)

DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo = True) # Initialises connection to the existing database, echo=True enables debugging (Printing out all queries it executes).
SessionLocal = sessionmaker(bind=engine) # Creates database sessions

Base.metadata.create_all(engine)

print("Tables created successfully!")

def test_db_connection():
    """
    Attempts to connect to the database and prints the status

    Args:
        None
    Returns:
        None
    Raises:
        Exception: If an unexpected error occurs.
    """
    try:
        with engine.connect() as connection: # engine.connect() opens a direct connection to the database, "with" automatically closes connection after execution.
            print("✅ Successfully connected to the database!")
    except Exception as e:
            print("❌ Error:", e)

test_db_connection()

#Create all tables defined in your models
#Base.metadata.create_all(engine)
#print("Tables created successfully!")

