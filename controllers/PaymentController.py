from datetime import datetime
from lib.model_to_dicts import model_to_dict
from lib.string_func import generate_random_string
from models.Bookings import Booking
from models.Events import Event
from models.PaymentInfo import PaymentInfo
from controllers.Controllers import Controller
from flask import jsonify
from models.Tickets import Ticket

class PaymentController(Controller):
    def __init__(self):
        super().__init__()

    def CheckStatus(self, payment_id: str):
        payment = self._db.query(PaymentInfo).filter(PaymentInfo.id == payment_id).first()

        if not payment:
            return jsonify({"msg": "Payment not found"}), 404

        data = model_to_dict(payment)

        return jsonify({
            "id": payment.id,
            "status": payment.status.value,
        }), 200

    def CreatePayment(self):
        booking_id = self.data['booking_id']

        booking = self._db.query(Booking).filter(Booking.id == booking_id).first()
        ticket = self._db.query(Ticket).filter(Ticket.booking_id == booking_id).first()
        event = self._db.query(Event).filter(Event.id == booking.event_id).first()

        payment_data = {
            "id": generate_random_string(),
            "method": self.data['method'],
            "bank_name": self.data['bank_name'],
            "card_number": self.data['card_number'],
            "status": "SUCCESS",
            "tax": 0.12,
            "amount": ticket.price + (ticket.price * 0.12),
            "payment_date": datetime.now()
        }

        try:
            payment = PaymentInfo(**payment_data)
            booking.payment_status = "SUCCESS"
            event.current_capacity += 1
            event.is_fullybooked = event.current_capacity >= event.capacity
            event.is_available = not event.is_fullybooked
            event.tikets_count += 1

            self._db.add(payment)
            self._db.commit()
            self._db.refresh(payment)
            self._db.refresh(booking)
            self._db.refresh(event)
            self._db.close()

            return jsonify({
                "msg": "Payment successful",
            }), 200

        except Exception as e:
            print(e)
            self._db.rollback()
            return jsonify({"msg": "Failed to process payment"}), 500