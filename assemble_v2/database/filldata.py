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
from main_components.models import Booking, CinemaFilm,cinema,city_pricing,city,film,payment,permissions,role,Screen,Screening,Seat,ticket,user
from main_components.models import Base
from main_components.services.booking_service import BookingService, InvalidScreeningError, NoSeatsSelectedError
from main_components.services.cinema_service import CinemaService
from main_components.services.city_service import CityService
from main_components.services.film_service import CinemaFilmService
from main_components.services.payment_service import PaymentService
from main_components.services.permission_service import PermissionService
from main_components.services.pricing_service import PricingService
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
            {"name": "Birmingham","country": "UK"},
            {"name": "Bristol","country": "UK"},
            {"name": "Cardiff","country": "UK"},
            {"name": "London","country": "UK"}
        ]
        for city_data in cities:
            try:
                city_service.create_city(city_data["name"], city_data["country"])
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
            {"name": "HC-Birm1", "address": "Birm1address" ,"city": city_service.get_city_by_name("Birmingham").city_id},
            {"name": "HC-Birm2", "address": "Birm2address" ,"city": city_service.get_city_by_name("Birmingham").city_id},
            {"name": "HC-Bris1", "address": "Bris1address" ,"city": city_service.get_city_by_name("Bristol").city_id},
            {"name": "HC-Bris2", "address": "Bris2address" ,"city": city_service.get_city_by_name("Bristol").city_id},
            {"name": "HC-Card1", "address": "Card1address" ,"city": city_service.get_city_by_name("Cardiff").city_id},
            {"name": "HC-Card2", "address": "Card2address" ,"city": city_service.get_city_by_name("Cardiff").city_id},
            {"name": "HC-Lond1", "address": "Lond1address" ,"city": city_service.get_city_by_name("London").city_id},
            {"name": "HC-Lond2", "address": "Lond2address" ,"city": city_service.get_city_by_name("London").city_id}
        ]
        for cinema_data in cinemas:
            try:
                cinema_service.create_cinema(cinema_data["name"], cinema_data["address"], cinema_data["city"])
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
    cinema_service = CinemaService(session)
    cinema = cinema_service.get_cinema_by_name(1)
    cinema_film_service = CinemaFilmService(cinema, session)
    try:
        films = [
            {"name": "The Shawshank Redemption", "genre": ["Drama"], "cast": ["Tim Robbins", "Morgan Freeman"], "description": "A story of hope and friendship.", "age_rating": 15, "critic_rating": 9.3, "runtime": 142, "release_date": datetime(1994, 9, 23)}, 
            {"name": "The Godfather", "genre": ["Crime", "Drama"], "cast": ["Marlon Brando", "Al Pacino"], "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "age_rating": 17, "critic_rating": 9.2, "runtime": 175, "release_date": datetime(1972, 3, 24)}, 
            {"name": "The Dark Knight", "genre": ["Action", "Crime", "Drama"], "cast": ["Christian Bale", "Heath Ledger"], "description": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.", "age_rating": 13, "critic_rating": 9.0, "runtime": 152, "release_date": datetime(2008, 7, 18)},
            {"name": "Inception", "genre": ["Action", "Adventure", "Sci-Fi"], "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"], "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", "age_rating": 13, "critic_rating": 8.8, "runtime": 148, "release_date": datetime(2010, 7, 16)}, 
            {"name": "Fight Club", "genre": ["Drama"], "cast": ["Brad Pitt", "Edward Norton"], "description": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.", "age_rating": 18, "critic_rating": 8.8, "runtime": 139, "release_date": datetime(1999, 10, 15)}, 
            {"name": "Pulp Fiction", "genre": ["Crime", "Drama"], "cast": ["John Travolta", "Uma Thurman"], "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", "age_rating": 18, "critic_rating": 8.9, "runtime": 154, "release_date": datetime(1994, 10, 14)}
        ]
        for film_data in films:
            try:
                cinema_film_service.create_film(film_data["name"], film_data["genre"], film_data["cast"], film_data["description"], film_data["age_rating"], film_data["critic_rating"], film_data["runtime"], film_data["release_date"])
            except IntegrityError:
                print(f"Duplicate entry found for film: {film_data['name']}")
                session.rollback()
        session.commit()
    except Exception as e:
        session.rollback() 
        print(f"Error filling film data: {e}")
    finally:
        session.close()


fill_film()

def fill_cinema_film():
    session = SessionLocal()
    cinema_service = CinemaService(session)
    try:
        cinema1 = cinema_service.get_cinema_by_id(1)
        cinema2 = cinema_service.get_cinema_by_id(2)
        cinema3 = cinema_service.get_cinema_by_id(3)
        cinema4 = cinema_service.get_cinema_by_id(4)
        cinema5 = cinema_service.get_cinema_by_id(5)
        cinema6 = cinema_service.get_cinema_by_id(6)
        cinema7 = cinema_service.get_cinema_by_id(7)
        cinema8 = cinema_service.get_cinema_by_id(8)

        # Create CinemaFilmService with a valid cinema
        cinema_film_service = CinemaFilmService(cinema1,session)

        film1 = cinema_film_service.get_film_by_name("The Shawshank Redemption")
        film2 = cinema_film_service.get_film_by_name("The Godfather")
        film3 = cinema_film_service.get_film_by_name("The Dark Knight")
        film4 = cinema_film_service.get_film_by_name("Inception")

        # Create the associations
        associations = [
            (cinema1, film1),  # cinema1 shows film1
            (cinema1, film2),  # cinema1 shows film2
            (cinema1, film3),
            (cinema1, film4),
            (cinema2, film1),  # cinema2 shows film1
            (cinema2, film2),
            (cinema2, film3),
            (cinema2, film4),
            (cinema3, film1),
            (cinema3, film2),
            (cinema3, film3),
            (cinema3, film4),
            (cinema4, film1),
            (cinema4, film2),
            (cinema4, film3),
            (cinema4, film4),
            (cinema5, film1),
            (cinema5, film2),
            (cinema5, film3),
            (cinema5, film4),
            (cinema6, film1),
            (cinema6, film2),
            (cinema6, film3),
            (cinema6, film4),
            (cinema7, film1),
            (cinema7, film2),
            (cinema7, film3),
            (cinema7, film4),
            (cinema8, film1),
            (cinema8, film2),
            (cinema8, film3),
            (cinema8, film4)
        ]
        # Add associations to the database
        for cinema, film in associations:
            cinema_film_service = CinemaFilmService(cinema, session)
            # Check if the association already exists (using .first())
            existing_association = session.query(CinemaFilm).filter(
                CinemaFilm.cinema_id == cinema.cinema_id,
                CinemaFilm.film_id == film.film_id
                ).first()
            if existing_association is None:  # Only insert if it doesn't exist
                try:
                    cinema_film_service.add_film_to_cinema(film=film)
                except IntegrityError:
                    print(f"Duplicate entry found for cinema: {cinema.name}, film: {film.name}")
                    session.rollback()
                except ValueError as e:
                    print(f"Error: {e}")
                    session.rollback()
        session.commit()
    except ValueError as e:
        session.rollback()
        print(f"Error: {e}")
    except Exception as e:
        session.rollback()
        print(f"Error filling cinema-film data: {e}")
    finally:
        session.close()

fill_cinema_film()

def fill_screen():
    session = SessionLocal()
    cinema_service = CinemaService(session)
    screen_service = ScreenService(session)
    try:
        cinemas = cinema_service.get_all_cinemas()
        for cinema in cinemas:
            screens = [
                {"id": "S1", "capacity_upper": 50, "capacity_lower": 50, "capacity_vip": 10},
                {"id": "S2", "capacity_upper": 40, "capacity_lower": 40, "capacity_vip": 10},
                {"id": "S3", "capacity_upper": 30, "capacity_lower": 30, "capacity_vip": 10},
                {"id": "S4", "capacity_upper": 20, "capacity_lower": 20, "capacity_vip": 10},
                {"id": "S5", "capacity_upper": 40, "capacity_lower": 10, "capacity_vip": 10},
                {"id": "S6", "capacity_upper": 40, "capacity_lower": 50, "capacity_vip": 10},
            ]
            for screen_data in screens:
                existing_screen = screen_service.get_screen_by_id(screen_data["id"], cinema.cinema_id)
                if existing_screen is None:
                    try:
                        screen_service.create_screen(screen_data["id"], cinema.cinema_id, screen_data["capacity_upper"], screen_data["capacity_lower"], screen_data["capacity_vip"])
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

def fill_screening(start_hour, start_minute):
    session = SessionLocal()
    screen_service = ScreenService(session)
    cinema_service = CinemaService(session)
    screening_service = ScreeningService(session)
    try:
        cinemas = cinema_service.get_all_cinemas()
        for cinema in cinemas:
            film_service = CinemaFilmService(cinema,session)
            films = film_service.get_all_films()
            screens = cinema_service.get_screens(cinema.cinema_id) # Get all screens for the cinema
            film_index = 0 # To cycle through films

            # Use the provided start time
            base_start_datetime = datetime(2024, 3, 26, start_hour, start_minute)

            for screen in screens:
                # Assign a film (round-robin)
                film = films[film_index % len(films)]
                film_index += 1

                end_datetime = base_start_datetime + timedelta(minutes=film.runtime)

                # Check if screening already exists.
                screening_exists = session.query(Screening).filter(
                    Screening.screen_id == screen.screen_id,
                    Screening.cinema_id == cinema.cinema_id,
                    Screening.start_time == base_start_datetime,
                ).first()
                
                if not screening_exists:
                    screening_service.create_screening(screen.screen_id, film.film_id,base_start_datetime.date(), base_start_datetime, end_datetime, cinema.cinema_id, 0, 0, 0)
                else:
                    print(f"Screening already exists: Cinema: {cinema.cinema_id}, Screen: {screen.screen_id}, Start: {base_start_datetime}")
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error filling screening data: {e}")
    finally:
        session.close()

fill_screening(10, 0)

def fill_seat():
    session = SessionLocal()
    screen_service = ScreenService(session)
    cinema_service = CinemaService(session)
    seat_service = SeatService(session)
    try:
        cinemas = cinema_service.get_all_cinemas()
        for cinema in cinemas:
            screens = screen_service.get_screens(cinema.cinema_id)
            for screen in screens: 
                total_seats = random.randint(50, 120)
                vip_seats = 10
                lower_hall_seats = int(total_seats * 0.3)
                upper_hall_seats = total_seats - vip_seats - lower_hall_seats
                seats_per_row = 10
                row_number = 1
                seat_number = 1
                seat_objects = []  # List to hold Seat objects for batch insert
                batch_size = 100  # Number of seats to insert in each batch


                # Create VIP Seats
                for _ in range(vip_seats):
                    seat_objects.append(Seat(screen_id=screen.screen_id, cinema_id=cinema.cinema_id, row_number=row_number, seat_number=seat_number, seat_class='VIP'))
                    seat_number += 1
                    if seat_number > seats_per_row:
                        row_number += 1
                        seat_number = 1
                    if len(seat_objects) >= batch_size:
                        session.bulk_save_objects(seat_objects)
                        session.commit()
                        seat_objects = []

                # Create Lower Hall Seats
                for _ in range(lower_hall_seats):
                    seat_objects.append(Seat(screen_id=screen.screen_id, cinema_id=cinema.cinema_id, row_number=row_number, seat_number=seat_number, seat_class='Lower Class'))
                    seat_number += 1
                    if seat_number > seats_per_row:
                        row_number += 1
                        seat_number = 1
                    if len(seat_objects) >= batch_size:
                        session.bulk_save_objects(seat_objects)
                        session.commit()
                        seat_objects = []

                # Create Upper Hall Seats
                for _ in range(upper_hall_seats):
                    seat_objects.append(Seat(screen_id=screen.screen_id, cinema_id=cinema.cinema_id, row_number=row_number, seat_number=seat_number, seat_class='Upper Class'))
                    seat_number += 1
                    if seat_number > seats_per_row:
                        row_number += 1
                        seat_number = 1
                    if len(seat_objects) >= batch_size:
                        session.bulk_save_objects(seat_objects)
                        session.commit()
                        seat_objects = []
                
                # Insert any remaining seats
                if seat_objects:
                    session.bulk_save_objects(seat_objects)
                    session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error filling seat data: {e}")
    finally:
        session.close()

fill_seat()

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
    user_service = UserService(session, role_service, cinema_service)
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

def fill_pricing():
    session = SessionLocal()
    pricing_service = PricingService(session)
    try:
        lower_class_prices = [
            {"city": "Birmingham", "time_of_day": "Morning", "price": 5.00},
            {"city": "Birmingham", "time_of_day": "Afternoon", "price": 6.00},
            {"city": "Birmingham", "time_of_day": "Evening", "price": 7.00},
            {"city": "Bristol", "time_of_day": "Morning", "price": 6.00},
            {"city": "Bristol", "time_of_day": "Afternoon", "price": 7.00},
            {"city": "Bristol", "time_of_day": "Evening", "price": 8.00},
            {"city": "Cardiff", "time_of_day": "Morning", "price": 5.00},
            {"city": "Cardiff", "time_of_day": "Afternoon", "price": 6.00},
            {"city": "Cardiff", "time_of_day": "Evening", "price": 7.00},
            {"city": "London", "time_of_day": "Morning", "price": 10.00},
            {"city": "London", "time_of_day": "Afternoon", "price": 11.00},
            {"city": "London", "time_of_day": "Evening", "price": 12.00}
        ]
        for lower_class_price in lower_class_prices:
            city = lower_class_price["city"]
            time_of_day = lower_class_price["time_of_day"]
            price = lower_class_price["price"]

            try:
                # Add lower class prices
                pricing_service.add_price(city, "Lower Class", time_of_day, price)

                # Calculate Upper class and VIP prices using get_price
                upper_class_price = pricing_service.get_price(city, "Upper Class", time_of_day)
                vip_price = pricing_service.get_price(city, "VIP", time_of_day)

                # Add upper class and vip prices
                pricing_service.add_price(city, "Upper Class", time_of_day, upper_class_price)
                pricing_service.add_price(city, "VIP", time_of_day, vip_price)

            except IntegrityError:
                print(f"Duplicate entry found for pricing: {city}, {time_of_day}")
                session.rollback()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error filling pricing data: {e}")
    finally:
        session.close()

fill_pricing()

def fill_booking():
    session = SessionLocal()
    seat_service = SeatService(session)
    ticket_service = TicketService(session)
    pricing_service = PricingService(session)
    booking_service = BookingService(session, seat_service, ticket_service, pricing_service)
    screening_service = ScreeningService(session)
    try:
        screening = screening_service.get_screening_by_id(37)
        seats_to_book = [seat_service.get_seat_by_id(19)]
    
        # Check if all seats were retrieved successfully
        if any(seat is None for seat in seats_to_book):
            print(f"Not all seats (1, 2, 3) exist for screening {screening.screening_id}.")
            return
        
        # Check seat availability
        unavailable_seats = [seat for seat in seats_to_book if not seat.is_available]

        if unavailable_seats:
            print(f"Some seats are unavailable for screening {screening.screening_id}: {[seat.seat_id for seat in unavailable_seats]}")
            return

        # Create booking
        customer_name = "SEventh Customer"
        customer_email= "SeventhCustomer@gmail.com"
        customer_phone= "12332332-4356-7890"
        try:
            booking = booking_service.create_booking(screening.screening_id, price=0, seats=seats_to_book, customer_name=customer_name, customer_email=customer_email, customer_phone=customer_phone)
        except ValueError as e:
            print(f"Skipping booking because of missing price for screening {screening.screening_id}: {e}")
        # Place booking
        booking_service.place_booking(booking.booking_id)
        session.commit()
        print((f"Bookings created successfully : {booking.booking_id}"))

    except (InvalidScreeningError, NoSeatsSelectedError) as e:
        session.rollback()
        print(f"Error creating bookings: {e}")
    except Exception as e:
        session.rollback()
        print(f"Error filling booking data: {e}")
    finally:
        session.close()

fill_booking()

def fill_payment():
    session = SessionLocal()
    payment_service = PaymentService(session)
    seat_service = SeatService(session)
    ticket_service = TicketService(session)
    pricing_service = PricingService(session)
    booking_service = BookingService(session, seat_service, ticket_service, pricing_service)
    try:
        bookings = booking_service.get_all_bookings()
        for booking in bookings:
            # Generate random payment details
            payment_method = random.choice(["Credit Card", "Debit Card", "Cash"])
            amount = booking.price
            transaction_id = str(uuid.uuid4())
            payment=payment_service.create_payment(booking.booking_id, payment_method,booking.price, transaction_id)

            # Update payment status (e.g., set to PAID)
            payment_service.update_payment_status(
                payment_id=payment.payment_id,
                payment_status=PaymentStatus.PAID,
                transaction_id=transaction_id
            )
            print(f"Payment created for booking {booking.booking_id}")

        session.commit()
        print("Payment created successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error filling payment data: {e}")
    finally:
        session.close()

fill_payment()