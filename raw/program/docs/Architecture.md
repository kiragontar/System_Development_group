# Cinema Booking System Backend - Architecture

## System Architecture Overview

The Cinema Booking System Backend follows a modular, service-oriented architecture, designed for scalability and maintainability. It primarily comprises the following components:

## Database Layer

-   **MySQL Database:** Stores all persistent data, including cinema details, film information, screenings, bookings, users, and payment records.
-   **SQLAlchemy ORM:** Acts as an abstraction layer between the database and the application services, allowing for database interactions using Python objects.

## Models Layer

-   **Data Models:** Defines the structure of the data entities in the system, such as `Cinema`, `Film`, `Screening`, `Booking`, `User`, etc.
-   **SQLAlchemy Declarative Base:** Models are defined as Python classes that inherit from the SQLAlchemy declarative base, allowing for easy mapping to database tables.
-   **Abstraction:** This layer primarily handles data representation and database interactions. Services interact with these models to perform CRUD operations.
-   **Direct Interaction:** While the model layer provides the underlying data structure, direct interaction with models is generally handled by the service layer to enforce business logic and data validation.

## Service Layer

-   **Booking Service:** Manages booking creation, retrieval, and modification.
-   **Cinema Service:** Handles cinema-related operations, such as adding, updating, and retrieving cinema details.
-   **City Service:** Manages city details, including adding, updating, and retrieving city information.
-   **Film Service:** Manages film information, including adding, updating, and retrieving film details.
-   **Payment Service:** Integrates with payment gateways (Stripe) for online transactions and manages payment records.
-   **Permission Service:** Manages role permissions.
-   **Pricing Service:** Manages pricing rules, including city-based pricing and time-based pricing.
-   **Role Service:** Manages user roles.
-   **Screening Service:** Schedules and manages film screenings.
-   **Screen Service:** Manages screen details, including capacity and usage.
-   **Seat Service:** Manages seat details, including availability and class.
-   **Ticket Service:** Manages ticket creation and retrieval.
-   **User Service:** Handles user registration, login, and role assignment.

## Application Logic

-   **Python Backend:** The core application logic is written in Python, leveraging SQLAlchemy for database interactions.
-   **Modular Design:** Services are designed to be independent and reusable, promoting code maintainability and scalability.

## Data Flow

1.  **Client Request:** A client (e.g., a web application) sends a request to the backend.
2.  **Service Processing:** The request is routed to the appropriate service, which processes the request and interacts with the database via SQLAlchemy.
3.  **Database Interaction:** SQLAlchemy translates the service's requests into SQL queries and interacts with the MySQL database.
4.  **Response:** The service returns a response to the client.