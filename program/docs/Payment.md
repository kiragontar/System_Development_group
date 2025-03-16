# Payment Service Documentation

## Overview

The Payment Service manages payment-related operations, including creating, updating, retrieving, and refunding payments.

## Class: `PaymentService`

The `PaymentService` class provides the following methods:

### `create_payment(booking_id, payment_method, amount, transaction_id=None)`
Creates a new payment.

**Parameters:**
- `booking_id` (str): The ID of the associated booking.
- `payment_method` (str): The method used for payment.
- `amount` (float): The amount of the payment.
- `transaction_id` (str, optional): The transaction ID provided by the payment gateway.

**Returns:**
- `Payment`: The newly created `Payment` object.

**Example:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Payment, Booking
from services.payment_service import PaymentService
from enums import PaymentStatus
from datetime import datetime

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Create test data , you should extract screen, seat ids not assign them by strings. (right now its done for simplicity.)
booking = Booking(screening_id=1, price=50.0, seats=["1", "2", "3"], customer_name="Test Customer")
session.add(booking)
session.commit()

payment_service = PaymentService(session)
booking_service = BookingService(session) # create booking service

# Retrieve the booking using booking service
retrieved_booking = booking_service.get_booking_by_id(booking.booking_id)


payment = payment_service.create_payment( 
    booking_id=retrieved_booking.booking_id, #(assuming you have a Booking object)
    payment_method="Credit Card",
    amount=retrieved_booking.price(),
    transaction_id="TXN456"
)
print(f"Payment created: {payment.payment_id}")
```

### `update_payment_status(payment_id, payment_status, transaction_id=None)`
Updates the payment status and optionally sets the transaction ID.

**Parameters:**
- `payment_id` (int): The ID of the payment to update.
- `payment_status` (PaymentStatus): The new payment status.
- `transaction_id` (str, optional): The transaction ID provided by the payment gateway.

**Returns:**
- `Payment`: The updated `Payment` object, or `None` if the payment is not found.

**Example:**
```python
updated_payment = payment_service.update_payment_status(
    payment_id=payment.payment_id,
    payment_status=PaymentStatus.PAID,
    transaction_id="TXN789"
)
if updated_payment:
    print(f"Payment status updated: {updated_payment.payment_status}")
```

### `get_payment_by_id(payment_id)`
Retrieves a payment by its ID.

**Parameters:**
- `payment_id` (int): The ID of the payment to retrieve.

**Returns:**
- `Payment`: The `Payment` object if found, or `None` if not found.

**Example:**
```python
payment = payment_service.get_payment_by_id(payment.payment_id)
if payment:
    print(f"Payment found: {payment.payment_id}")
```

### `get_payments_by_booking(booking_id)`
Retrieves all payments for a specific booking.

**Parameters:**
- `booking_id` (str): The ID of the booking.

**Returns:**
- `list[Payment]`: A list of `Payment` objects associated with the booking.

**Example:**
```python
payments = payment_service.get_payments_by_booking(booking.booking_id)
for p in payments:
    print(f"Payment for booking: {p.payment_id}")
```

### `refund_payment(payment_id)`
Refunds a payment by its ID.

**Parameters:**
- `payment_id` (int): The ID of the payment to refund.

**Returns:**
- `bool`: `True` if the payment was refunded, `False` otherwise.

**Example:**
```python
refunded = payment_service.refund_payment(payment.payment_id)
print(f"Payment refunded: {refunded}")
```

## Relationships
- **Booking**: A payment is associated with a booking 