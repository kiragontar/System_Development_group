from sqlalchemy.orm import Session
from models import PaymentStatus, Payment



class PaymentService:
    def __init__(self, session: Session):
        self.session = session

    def create_payment(self, booking_id: str, payment_method: str, amount: float, transaction_id: str = None) -> Payment:
        """Creates a new payment."""
        payment = Payment(booking_id=booking_id, payment_method=payment_method, amount=amount, transaction_id=transaction_id)
        self.session.add(payment)
        self.session.commit()
        return payment
    
    def update_payment_status(self, payment_id: int, payment_status: PaymentStatus, transaction_id: str = None) -> Payment:
        payment = PaymentService.get_payment_by_id(payment_id)
        if payment:
            payment.set_payment_status(payment_status)
            if transaction_id:
                payment.set_transaction_id(transaction_id)
            self.session.commit()
            return payment
        return None

    def get_payment_by_id(self, payment_id: int) -> Payment:
        """Retrieves a payment by its ID."""
        payment = self.session.query(Payment).filter_by(payment_id=payment_id).first()
        return payment

    def get_payments_by_booking(self, booking_id: str) -> list[Payment]:
        """Retrieves all payments for a specific booking."""
        payments = self.session.query(Payment).filter_by(booking_id=booking_id).all()
        return payments
    
    def refund_payment(self, payment_id: int) -> bool:
        """Refunds a payment by its ID."""
        payment = self.session.query(Payment).filter_by(payment_id=payment_id).first()
        if payment:
            payment.payment_status = PaymentStatus.REFUNDED
            self.session.commit()
            return True
        return False