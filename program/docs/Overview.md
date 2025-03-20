# Cinema Booking System Backend - Overview

## Project Description

The Cinema Booking System Backend provides a comprehensive backend solution for managing a cinema's operations. It enables the management of cinemas, cities, city pricings, films, screenings, screens, seats, users, roles, permissions, bookings, tickets, and payments, offering a robust and scalable platform for online cinema booking.

## Key Features

- **Cinema Management:** Add, update, and manage cinema details.
- **Film Management:** Manage film information, including screenings and details.
- **Screening Management:** Schedule and manage film screenings.
- **Screen Management:** Manage screen details, including capacity and layout.
- **Seat Management:** Manage seat details, including availability and class.
- **Booking Management:** Create, retrieve, and manage bookings.
- **Ticket Management:** Create, retrieve, and manage tickets.
- **User Management:** Handles user registration, login, and roles.
- **Role and Permission Management:** Manage user roles and permissions.
- **Payment Processing:** Integrate payment gateways (Stripe) for online transactions.
- **City Management:** Add, update, and manage city details.
- **City Pricing Management:** Manage pricing based on city locations and timings (Morning, Afternoon, Night).

## Architecture Overview

The system is built using Python with SQLAlchemy for database interaction and a modular service-oriented architecture. It uses a MySQL database for data storage and relies on a set of services to manage different aspects of the cinema booking process. The Backend is designed to be easily extensible and adaptable to various cinema business models.

## How to Use

To begin using the Backend, please follow the setup instructions in [SETUP.md](SETUP.md). Once set up, you can use the service documentation in the `docs` folder to interact with the Backend.
