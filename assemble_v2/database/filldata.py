import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
import mysql.connector # To connect with the MYsql table created in MYSQL workbench.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, time
import random
import sys
import os
import uuid

program_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "program"))
services_path = os.path.abspath(os.path.join(program_path, "services")) 

# Add the program_path and services_path to sys.path in the correct order
if program_path not in sys.path:
    sys.path.insert(0, program_path)
if services_path not in sys.path:
    sys.path.insert(1, services_path)

from main_components.services.city_service import CityService
from main_components.models import Booking, cinema,city,Film,permissions,role,Screen,Screening,Seat,ticket,user, SeatAvailability
from main_components.models import Base
from main_components.services.booking_service import BookingService, BookingNotFoundError, BookingTimeoutError
from main_components.services.cinema_service import CinemaService
from main_components.services.city_service import CityService
from main_components.services.film_service import FilmService
from main_components.services.permission_service import PermissionService
from main_components.services.role_service import RoleService
from main_components.services.screen_service import ScreenService
from main_components.services.screening_service import ScreeningService
from main_components.services.seat_service import SeatService
from main_components.services.ticket_service import TicketService
from main_components.services.user_service import UserService 
from main_components.enums import PaymentStatus
# Create a connection to the database
conn = mysql.connector.connect(
    host="localhost",
    user="MickelUWE",
    password="g<bI1Z11iC]c",
    database="Cinema"
)   
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo = False) # Initialises connection to the existing database, echo=True enables debugging (Printing out all queries it executes).
SessionLocal = sessionmaker(bind=engine) # Creates database sessions

def fill_city():
    session = SessionLocal()
    city_service = CityService(session)
    try:
        cities = [
            {"name": "Birmingham","country": "UK", "price_morning" : 5, "price_afternoon" : 6, "price_evening" : 7},
            {"name": "Bristol","country": "UK", "price_morning" : 6, "price_afternoon" : 7, "price_evening" : 8},
            {"name": "Cardiff","country": "UK", "price_morning" : 5, "price_afternoon" : 6, "price_evening" : 7},
            {"name": "London","country": "UK", "price_morning" : 10, "price_afternoon" : 11, "price_evening" : 12}
        ]
        for city_data in cities:
            try:
                city_service.create_city(city_data["name"], city_data["country"], city_data["price_morning"], city_data["price_afternoon"], city_data["price_evening"])
            except IntegrityError:
                print(f"Duplicate entry found for city: {city_data['name']} in {city_data['country']}")
                session.rollback()

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error filling city data: {e}")
    finally:
        session.close()

fill_city()


def fill_cinema():
    session = SessionLocal()
    cinema_service = CinemaService(session)
    city_service = CityService(session) 
    try:
        cinemas = [
            {"city": city_service.get_city_by_name("Birmingham").city_id, "name": "HC-Birm1", "address": "Birm1address"},
            {"city": city_service.get_city_by_name("Birmingham").city_id, "name": "HC-Birm2", "address": "Birm2address"},
            {"city": city_service.get_city_by_name("Bristol").city_id, "name": "HC-Bris1", "address": "Bris1address"},
            {"city": city_service.get_city_by_name("Bristol").city_id, "name": "HC-Bris2", "address": "Bris2address"},
            {"city": city_service.get_city_by_name("Cardiff").city_id, "name": "HC-Card1", "address": "Card1address"},
            {"city": city_service.get_city_by_name("Cardiff").city_id, "name": "HC-Card2", "address": "Card2address"},
            {"city": city_service.get_city_by_name("London").city_id, "name": "HC-Lond1", "address": "Lond1address"},
            {"city": city_service.get_city_by_name("London").city_id, "name": "HC-Lond2", "address": "Lond2address"}
        ]
        for cinema_data in cinemas:
            try:
                cinema_service.create_cinema(cinema_data["city"], cinema_data["name"], cinema_data["address"])
            except IntegrityError:
                print(f"Duplicate entry found for cinema: {cinema_data['name']} in {cinema_data['address']}")
                session.rollback()

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error filling cinema data: {e}")
    finally:
        session.close()

fill_cinema()

def fill_film():
    session = SessionLocal()
    film_service = FilmService(session)
    try:
        films = [
            {"name": "The Shawshank Redemption", "genre": ["Drama"], "cast": ["Tim Robbins", "Morgan Freeman"], "description": "A story of hope and friendship.", "age_rating": 15, "critic_rating": 9.3, "runtime": 142, "release_date": datetime(1994, 9, 23)}, 
            {"name": "The Godfather", "genre": ["Crime", "Drama"], "cast": ["Marlon Brando", "Al Pacino"], "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "age_rating": 17, "critic_rating": 9.2, "runtime": 175, "release_date": datetime(1972, 3, 24)}, 
            {"name": "The Dark Knight", "genre": ["Action", "Crime", "Drama"], "cast": ["Christian Bale", "Heath Ledger"], "description": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.", "age_rating": 13, "critic_rating": 9.0, "runtime": 152, "release_date": datetime(2008, 7, 18)},
            {"name": "Inception", "genre": ["Action", "Adventure", "Sci-Fi"], "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"], "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", "age_rating": 13, "critic_rating": 8.8, "runtime": 148, "release_date": datetime(2010, 7, 16)}, 
            {"name": "Fight Club", "genre": ["Drama"], "cast": ["Brad Pitt", "Edward Norton"], "description": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.", "age_rating": 18, "critic_rating": 8.8, "runtime": 139, "release_date": datetime(1999, 10, 15)}, 
            {"name": "Pulp Fiction", "genre": ["Crime", "Drama"], "cast": ["John Travolta", "Uma Thurman"], "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", "age_rating": 18, "critic_rating": 8.9, "runtime": 154, "release_date": datetime(1994, 10, 14)}
        ]
        changes_made = False # flag to track database changes.
        for film_data in films:
            # Check for duplicates directly here
            existing_film = session.query(Film).filter_by(name=film_data["name"], release_date=film_data["release_date"]).first()
            if existing_film is None:
                try:
                    film_service.create_film(film_data["name"], film_data["genre"], film_data["cast"], film_data["description"], film_data["age_rating"], film_data["critic_rating"], film_data["runtime"], film_data["release_date"])
                    changes_made = True
                except IntegrityError:
                    print(f"Duplicate entry found for film: {film_data['name']}")
                    session.rollback()
            else:
                print(f"Film already exists: {film_data['name']} ({film_data['release_date']})")
        if changes_made: # only commit if changes occurred.
            session.commit()
    except Exception as e:
        session.rollback() 
        print(f"Error filling film data: {e}")
    finally:
        session.close()


fill_film()

def fill_screen():
    session = SessionLocal()
    cinema_service = CinemaService(session)
    screen_service = ScreenService(session)
    try:
        cinemas = cinema_service.get_all_cinemas()
        for cinema in cinemas:
            screens = [
                {"id": "S1", "total_capacity" : 100, "row_number" : 10},
                {"id": "S2", "total_capacity" : 120, "row_number" : 8},
                {"id": "S3", "total_capacity" : 90, "row_number" : 5},
                {"id": "S4", "total_capacity" : 50, "row_number" : 15},
                {"id": "S5", "total_capacity" : 70, "row_number" : 20},
                {"id": "S6", "total_capacity" : 85, "row_number" : 17},
            ]
            for screen_data in screens:
                existing_screen = screen_service.get_screen_by_id(screen_data["id"], cinema.cinema_id)
                if existing_screen is None:
                    try:
                        screen_service.create_screen(screen_data["id"], cinema.cinema_id, screen_data["total_capacity"], screen_data["row_number"])
                    except IntegrityError:
                        print(f"Duplicate entry found for screen: {screen_data['id']} in cinema: {cinema.cinema_id}")
                        session.rollback()
                else:
                    print(f"Screen {screen_data['id']} already exists in cinema: {cinema.cinema_id}. Skipping.")
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error filling screen data: {e}")
    finally:
        session.close()

fill_screen()

def fill_seat():
    session = SessionLocal()
    screen_service = ScreenService(session)
    cinema_service = CinemaService(session)
    try:
        cinemas = cinema_service.get_all_cinemas()
        for cinema in cinemas:
            screens = screen_service.get_screens(cinema.cinema_id)
            for screen in screens: 
                total_seats = random.randint(50, 120)
                vip_seats = 10
                lower_hall_seats = int(total_seats * 0.3)
                upper_hall_seats = total_seats - vip_seats - lower_hall_seats
                seat_objects = []  # List to hold Seat objects for batch insert

                # Create VIP Seats
                for _ in range(vip_seats):
                    seat_objects.append(Seat(screen_id=screen.screen_id, cinema_id=cinema.cinema_id, seat_type='VIP'))
                # Create Lower Hall Seats
                for _ in range(lower_hall_seats):
                    seat_objects.append(Seat(screen_id=screen.screen_id, cinema_id=cinema.cinema_id, seat_type='Lower'))
                # Create Upper Hall Seats
                for _ in range(upper_hall_seats):
                    seat_objects.append(Seat(screen_id=screen.screen_id, cinema_id=cinema.cinema_id, seat_type='Upper'))
                
                # Batch insert all seats
                try:
                    session.bulk_save_objects(seat_objects)
                except IntegrityError:
                    session.rollback()
                    print("Duplicate entry found for seats you are inserting.")
                except Exception as e:
                    session.rollback()
                    print(f"Error during seat insertion: {e}")
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error filling seat data: {e}")
    finally:
        session.close()

fill_seat()

def fill_screening(start_hour, start_minute):
    session = SessionLocal()
    screen_service = ScreenService(session)
    cinema_service = CinemaService(session)
    film_service = FilmService(session)
    screening_service = ScreeningService(session)
    try:
        cinemas = cinema_service.get_all_cinemas()
        films = film_service.get_all_films()
        base_date = datetime.now().date()
        start_time = time(start_hour,start_minute)
        screening_datetime = datetime.combine(base_date, start_time)
        for cinema in cinemas:
            screens = screen_service.get_screens(cinema.cinema_id)
            for screen in screens:
                # Pick a random film for this screen
                film = random.choice(films)
                # Check for duplicates before creating a screening
               # Check for duplicates using filter_by()
                existing_screening = session.query(Screening).filter_by(
                    screen_id=screen.screen_id,
                    cinema_id=cinema.cinema_id,
                    start_time=screening_datetime
                ).first()
                if not existing_screening:
                    try:
                        screening_service.create_screening(film.film_id, screen.screen_id, cinema.cinema_id, base_date, screening_datetime, screening_availability=0)
                    except IntegrityError:
                        session.rollback()
                        screening_datetime = datetime.combine(base_date, start_time)
                        print(f"IntegrityError: Screening already exists: Cinema: {cinema.cinema_id}, Screen: {screen.screen_id}, Start: {screening_datetime}")
                    except Exception as e:
                        session.rollback()
                        print(f"Error creating screening: {e}")
                else:
                    print(f"Screening already exists: Cinema: {cinema.cinema_id}, Screen: {screen.screen_id}, Start: {screening_datetime}")
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error filling screening data: {e}")
    finally:
        session.close()

fill_screening(10, 0)


def fill_seat_availability():
    session = SessionLocal()
    screening_service = ScreeningService(session)
    try:
        screenings = screening_service.get_all_screenings()
        for screening in screenings:
            # Get all seats for the cinema of the screening.
            cinema_id = screening.cinema_id
            screen_id = screening.screen_id
            seats = session.query(Seat).filter_by(cinema_id=cinema_id, screen_id=screen_id).all()

            if not seats:
                print(f"No seats found for cinema {cinema_id}, screen {screen_id} in screening {screening.screening_id}.")
                continue  # Move to the next screening

            for seat in seats:
                # Check if a SeatAvailability record already exists
                existing_availability = session.query(SeatAvailability).filter_by(screening_id=screening.screening_id,seat_id=seat.seat_id).first()

                if not existing_availability:
                    seat_availability = SeatAvailability(screening_id=screening.screening_id, seat_id=seat.seat_id, booking_id=None, seat_availability=1) # Initally no booking. and seats are available
                    session.add(seat_availability)
                else:
                    print(f"Seat availability already exists for screening {screening.screening_id}, seat {seat.seat_id}. Skipping.")

        session.commit()
    
    except Exception as e:
        session.rollback()
        print(f"Error populating seat availability: {e}")
    finally:
        session.close()

fill_seat_availability()



def fill_booking():
    session = SessionLocal()
    seat_service = SeatService(session)
    ticket_service = TicketService(session)
    booking_service = BookingService(session, ticket_service)
    screening_service = ScreeningService(session)
    try:
        seat1 = seat_service.get_seat_by_id("S1_C1_1")
        seat2 = seat_service.get_seat_by_id("S1_C1_10")
        seat3 = seat_service.get_seat_by_id("S1_C1_13")
        if not seat1 or not seat2 or not seat3:
            print("Error: One or more seats not found.")
            return

        seats_to_book = [seat1.seat_id, seat2.seat_id, seat3.seat_id]

        customer_name = "Customer1"
        customer_email = "Customer1@gmail.com"
        customer_phone = "123-456-7890"

        screening = screening_service.get_screening_by_id(1)
        if not screening:
            print("Error: Screening not found.")
            return

        bookings = booking_service.create_booking(seat_ids=seats_to_book, customer_name= customer_name, customer_email= customer_email, customer_phone=customer_phone, screening_id=screening.screening_id)
        if bookings is None:
            print(f"Failed to create booking for seats {seats_to_book} and screening {screening.screening_id}")

    except (BookingNotFoundError, BookingTimeoutError) as e:
        session.rollback()
        print(f"Error creating bookings: {e}")
    except Exception as e:
        session.rollback()
        print(f"Error filling booking data: {e}")
    finally:
        session.close()

fill_booking()


def fill_permission():
    session = SessionLocal()
    permission_service = PermissionService(session)
    try:
        permissions = [
            {"name": "view_film_listings"},
            {"name": "create_bookings"},
            {"name": "create_bookings_other_cinemas"},
            {"name": "cancel_bookings"},
            {"name": "view_bookings"},
            {"name": "manage_screenings"},
            {"name": "manage_films"},
            {"name": "generate_reports"},
            {"name": "manage_cinemas"},
            {"name": "manage_screens"},
            {"name": "manage_seats"},
            {"name": "manage_pricing"},
            {"name": "view_manager_analytics"},
            {"name": "admin_view"}, 
            {"name": "manager_view"}  
        ]
        for permission_data in permissions:
            try:
                permission_service.create_permission(permission_data["name"])
            except IntegrityError:
                print(f"Duplicate entry found for permission: {permission_data['name']}")
                session.rollback()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error filling permission data: {e}")
    finally:
        session.close()

fill_permission()

def fill_role():
    session = SessionLocal()
    role_service = RoleService(session)
    permission_service = PermissionService(session)
    try:
        roles = [
            {"name": "Manager"},
            {"name": "Admin"},
            {"name": "Staff"}
        ]
        for role_data in roles:
            role = role_service.create_role(role_data["name"])
        session.commit()
    except IntegrityError:
        session.rollback()
        print(f"Duplicate entry found for role: {role_data['name']}")
    except Exception as e:
        session.rollback()
        print(f"Error filling role data: {e}")
    
    try:
        permissions = permission_service.get_all_permissions()
        all_permission_names = [permission.name for permission in permissions]
        role_permissions = {
            "Manager": all_permission_names,
            "Admin" : ["view_film_listings", "create_bookings", "create_bookings_other_cinemas", "cancel_bookings",
                "view_bookings", "manage_screenings", "manage_screens", "manage_films", "generate_reports",
                "manage_seats", "manage_pricing", "admin_view"],
            "Staff" : ["view_film_listings", "create_bookings", "cancel_bookings", "view_bookings"]
        }
        for role_name, permission_name in role_permissions.items():
            role = role_service.get_role_by_name(role_name)
            if role:
                for permission_name in permission_name:
                    permission = next((p for p in permissions if p.name == permission_name), None)
                    if permission:
                        try:
                            role_service.add_permission_to_role(role.role_id, permission.permission_id)
                        except IntegrityError:
                            print(f"Duplicate entry found for role: {role_name}, permission: {permission_name}")
                            session.rollback()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error filling role-permission data: {e}")
    finally:
        session.close()

fill_role()

def fill_user():
    session = SessionLocal()
    role_service = RoleService(session)
    cinema_service = CinemaService(session)
    user_service = UserService(session)
    try:
        cinema1 = cinema_service.get_cinema_by_id(1)
        users = [
            {"username": "admin1", "password": "admin1pass$", "firstname": "Admin1", "lastname": "Admin1", "role": "Admin"},
            {"username": "manager1", "password": "manager1pass$", "firstname": "Manager1", "lastname": "Manager1", "role": "Manager"},
            {"username": "staff1", "password": "staff1pass$", "firstname": "Staff1", "lastname": "Staff1", "role": "Staff"}
        ]
        for user_data in users:
            try:
                user_service.create_user(user_data["username"], user_data["password"], user_data["firstname"], user_data["lastname"], role_service.get_role_by_name(user_data["role"]).role_id, cinema1.cinema_id)
            except IntegrityError:
                print(f"Duplicate entry found for user: {user_data['username']}")
                session.rollback()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error filling user data: {e}")
    finally:
        session.close()

fill_user()