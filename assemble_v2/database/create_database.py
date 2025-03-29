import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
import mysql.connector # To connect with the MYsql table created in MYSQL workbench.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main_components.models import Base
from main_components.models.booking import Booking
from main_components.models.seat_availability import SeatAvailability
from main_components.models.cinema import Cinema
from main_components.models.city import City
from main_components.models.film import Film
from main_components.enums import PaymentStatus
from main_components.models.permissions import Permission
from main_components.models.role import Role
from main_components.models.screen import Screen
from main_components.models.screening import Screening
from main_components.models.seat import Seat
from main_components.models.ticket import Ticket
from main_components.models.user import User
from main_components.models import Base  # Import your Base metadata

conn = mysql.connector.connect(
    host="localhost",
    user="MickelUWE",
    password="g<bI1Z11iC]c", 
    database="Cinema"
)

DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo = True) # Initialises connection to the existing database, echo=True enables debugging (Printing out all queries it executes).
SessionLocal = sessionmaker(bind=engine) # Creates database sessions

# Base.metadata.create_all(engine)

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

try:
    Base.metadata.drop_all(engine)
    print("All tables dropped.")

    Base.metadata.create_all(engine)
    print("All tables created.")

    print("Database reset successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
