import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from main_components.models import Seat, Ticket, SeatAvailability, Screening
from main_components.enums import PaymentStatus
from datetime import datetime, timedelta
import logging 

logging.basicConfig(level=logging.INFO)

class TicketService:
    def __init__(self, session: Session):
        self.session = session

    def get_ticket_by_id(self, ticket_id: int) -> Ticket:
        """Retrieves a ticket by its ID."""
        ticket = self.session.query(Ticket).filter_by(ticket_id=ticket_id).first()
        return ticket

    def get_tickets_by_booking(self, booking_id: str) -> list[Ticket]:
        """Retrieves all tickets for a specific booking."""
        tickets = self.session.query(Ticket).filter_by(booking_id=booking_id).all()
        return tickets
    
    def cancel_ticket(self, ticket_id: int) -> None:
        """Cancels a ticket."""
        # Tickets can be cancelled at least one day before the screening at 50 % charge. 
        # Get screening id from booking id and seat id.
        try:
            ticket = self.get_ticket_by_id(ticket_id)

            if not ticket:
                raise ValueError(f"Ticket with ID {ticket_id} not found.")
            
            seat_availability = self.session.query(SeatAvailability).filter_by(
                    seat_id=ticket.seat_id, booking_id=ticket.booking_id).first()
            
            if not seat_availability:
                raise ValueError(f"Seat availability for ticket with ID {ticket_id} not found.")
            
            screening = self.session.query(Screening).filter_by(screening_id=seat_availability.screening_id).first()

            if not screening:
                raise ValueError(f"Screening with ID {seat_availability.screening_id} not found.")
            
            # Check if ticket can be cancelled.
            if screening.date - datetime.now().date() < timedelta(days=1):
                raise ValueError("Tickets can only be cancelled at least one day before the screening.")
            
            # Otherwise, cancel ticket at 50% charge.
            ticket_price = ticket.ticket_price
            ticket.ticket_price = ticket_price / 2
            ticket.payment_status = PaymentStatus.REFUNDED
            self.session.commit()
            return True
        
        except Exception as e:
            self.session.rollback()
            logging.error(f"Failed to cancel ticket {ticket_id}: {e}")
            return False
        
    def get_all_tickets(self) -> list[Ticket]:
        """Retrieves all tickets."""
        tickets = self.session.query(Ticket).all()
        return tickets
    
    def update_ticket_details(self, ticket_id: int, qr_code: str = None, payment_status: PaymentStatus = None) -> Ticket:
        """Updates a ticket's details."""
        try:
            ticket = self.get_ticket_by_id(ticket_id)
            if not ticket:
                raise ValueError(f"Ticket with ID {ticket_id} not found.")
            if qr_code:
                ticket.qr_code = qr_code
            if payment_status:
                ticket.payment_status = payment_status
            self.session.commit()
            logging.info(f"Ticket details updated for ticket {ticket_id}.")
        except Exception as e:
            self.session.rollback()
            logging.error(f"Failed to update ticket {ticket_id}: {e}")
        return ticket