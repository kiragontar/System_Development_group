from sqlalchemy.orm import Session
from models import Seat, Ticket
from services.pricing_service import PricingService

class TicketService:
    def __init__(self, session: Session):
        self.session = session

    def create_ticket(self, booking_id: str, seat_id: int, screening_id: str, original_ticket_price: float, qr_code: str = None) -> Ticket:
        """Creates a new ticket."""
        seat = self.session.query(Seat).filter_by(seat_id=seat_id).first()
        if not seat: # Error handling, we need to make sure seat exists while making ticket.
            raise ValueError(f"Seat with ID {seat_id} not found.")
        
        ticket = Ticket(booking_id=booking_id, seat_id=seat_id, screening_id=screening_id, original_ticket_price=original_ticket_price, qr_code=qr_code)
        self.session.add(ticket)
        self.session.commit()
        return ticket
    
    def get_ticket_by_id(self, ticket_id: int) -> Ticket:
        """Retrieves a ticket by its ID."""
        ticket = self.session.query(Ticket).filter_by(ticket_id=ticket_id).first()
        return ticket

    def get_tickets_by_booking(self, booking_id: str) -> list[Ticket]:
        """Retrieves all tickets for a specific booking."""
        tickets = self.session.query(Ticket).filter_by(booking_id=booking_id).all()
        return tickets

    def get_tickets_by_screening(self, screening_id: int) -> list[Ticket]:
        """Retrieves all tickets for a specific screening."""
        tickets = self.session.query(Ticket).filter_by(screening_id=screening_id).all()
        return tickets
