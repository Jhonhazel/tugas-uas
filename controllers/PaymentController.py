from datetime import datetime

from flask_login import current_user

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

    def GetMyPayments(self):
        if current_user.is_anonymous:
            return jsonify({"msg": "User not logged in"}), 401

        payments = self._db.query(PaymentInfo).filter(PaymentInfo.user_id == current_user.id).all()

        if not payments:
            return jsonify({"data": []}), 200

        return jsonify({"data": [model_to_dict(p) for p in payments]}), 200

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
        user_id = current_user.id

        booking = self._db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return jsonify({"msg": "Booking not found"}), 404

        ticket = self._db.query(Ticket).filter(Ticket.booking_id == booking_id).first()
        event = self._db.query(Event).filter(Event.id == booking.event_id).first()

        if booking.payment_status == "SUCCESS":
            return jsonify({"msg": "Already paid"}), 200

        payment_data = {
            "id": generate_random_string(),
            "method": self.data['method'],
            "bank_name": self.data['bank_name'],
            "card_number": self.data['card_number'],
            "status": "SUCCESS",
            "tax": 0.12,
            "amount": ticket.price + (ticket.price * 0.12),
            "payment_date": datetime.now(),
            "user_id": user_id,
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

    def CancelPayment(self):
        booking_id = self.data['booking_id']
        payment_id = self.data['payment_id']

        payment = self._db.query(PaymentInfo).filter(PaymentInfo.id == payment_id).first()
        booking = self._db.query(Booking).filter(Booking.id == booking_id).first()

        if not payment or not booking:
            return jsonify({"msg": "Payment or Booking not found"}), 404

        event = self._db.query(Event).filter(Event.id == booking.event_id).first()
        if not event:
            return jsonify({"msg": "Event not found"}), 404

        if payment.status.value == "cancelled" and booking.payment_status.value == "success":
            return jsonify({"msg": "Payment already cancelled"}), 200

        if payment.status.value == "success" and booking.payment_status.value == "success":
            return jsonify({"msg": "Cannot cancel payment due to payment already paid"}), 400

        payment.status = "CANCELLED"
        booking.payment_status = "CANCELLED"
        event.current_capacity -= 1
        event.is_fullybooked = event.current_capacity >= event.capacity
        event.is_available = not event.is_fullybooked
        event.tikets_count -= 1  # Recheck if this logic is correct for your use case

        try:
            self._db.commit()
            self._db.refresh(payment)
            self._db.refresh(booking)
            self._db.refresh(event)
        except Exception as e:
            self._db.rollback()
            return jsonify({"msg": "Failed to cancel payment", "error": str(e)}), 500
        finally:
            self._db.close()

        return jsonify({"msg": "Payment cancelled"}), 200

    def RefundPayment(self):
        booking_id = self.data['booking_id']

        booking = self._db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return jsonify({"msg": "Booking not found"}), 404

        payment = self._db.query(PaymentInfo).filter(PaymentInfo.id == booking.payment_id).first()
        event = self._db.query(Event).filter(Event.id == booking.event_id).first()

        if not payment:
            return jsonify({"msg": "Booking or payment not found"}), 404

        if booking.payment_status == "cancelled" or payment.status == "cancelled":
            return jsonify({"msg": "Booking can't be refunded cause payment is already cancelled"}), 400

        if booking.payment_status == "failed" or payment.status == "failed":
            return jsonify({"msg": "Booking can't be refunded cause payment is already failed"}), 400

        if booking.payment_status == "refunded" or payment.status == "refunded":
            return jsonify({"msg": "Booking already refunded"}), 400

        booking.payment_status = "REFUNDED"
        payment.status = "REFUNDED"
        payment.payment_date = datetime.now()
        event.current_capacity -= 1
        event.is_fullybooked = event.current_capacity >= event.capacity
        event.is_available = not event.is_fullybooked
        event.tikets_count -= 1

        try:
            self._db.commit()
        except Exception as e:
            print(e)
            self._db.rollback()
            return jsonify({"msg": "Failed to refund booking"}), 500
        finally:
            self._db.close()

        return jsonify({"msg": "Booking refunded"}), 200

