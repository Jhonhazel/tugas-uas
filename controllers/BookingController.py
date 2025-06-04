from flask_login import current_user

from lib.has_time_passed import has_time_passed
from lib.model_to_dicts import model_to_dict
from models.Bookings import Booking
from lib.string_func import generate_random_string
from controllers.Controllers import Controller
from flask import jsonify
from models.Customers import Customer
from models.Events import Event
from models.PaymentInfo import PaymentInfo
from models.Tickets import Ticket
from datetime import datetime

class BookingController(Controller):
    def __init__(self):
        super().__init__()

    def GetMyBookings(self):
        if current_user.is_anonymous:
            return jsonify({"msg": "User not logged in"}), 401

        bookings = self._db.query(Booking).filter(Booking.user_id == current_user.id).all()

        if not bookings:
            return jsonify({"data": []}), 200

        return jsonify({"data": [model_to_dict(p) for p in bookings]}), 200

    def CreateBooking(self):
        event_id = self.data['event_id']
        user_id = current_user.id

        if not user_id:
            return jsonify({"msg": "User is not logged in"}), 403

        # Ambil data event sebagai object ORM
        event_obj = self._db.query(Event).filter(Event.id == event_id).first()

        if not event_obj:
            return jsonify({"msg": "Event not found"}), 404

        if (event_obj.current_capacity >= event_obj.capacity) and event_obj.is_fullybooked:
            return jsonify({"msg": "Event is fully booked"}), 400

        # Data customer
        customer_data = {
            "id": generate_random_string(),
            "first_name": self.data['first_name'],
            "last_name": self.data['last_name'],
            "phone": self.data['phone'],
            "email": self.data['email'],
            "address": self.data['address'],
            "gov_id": self.data['gov_id'],
            "user_id": user_id
        }

        # Data payment
        price = event_obj.price
        tax = 0.12
        amount = price + (price * tax)
        payment_data = {
            "id": generate_random_string(),
            "method": self.data['method'],
            "bank_name": self.data['bank_name'],
            "card_number": self.data['card_number'],
            "tax": tax,
            "amount": amount,
            "user_id": user_id
        }

        # Data booking
        booking_id = generate_random_string()
        booking_data = {
            "id": booking_id,
            "event_id": event_id,
            "customer_id": customer_data['id'],
            "payment_id": payment_data['id'],
            "user_id": user_id,
        }

        # Data ticket
        ticket_data = {
            "id": generate_random_string(),
            "price": price,
            "booking_id": booking_id,
            "event_id": event_id,
            "user_id": user_id,
        }

        try:
            # Buat object SQLAlchemy
            booking = Booking(**booking_data)
            ticket = Ticket(**ticket_data)
            payment = PaymentInfo(**payment_data)
            customer = Customer(**customer_data)

            # Tambahkan ke session
            self._db.add_all([booking, ticket, payment, customer])

            # Update event secara langsung
            event_obj.current_capacity += 1
            event_obj.is_fullybooked = event_obj.current_capacity >= event_obj.capacity
            event_obj.is_available = not event_obj.is_fullybooked
            event_obj.tikets_count += 1

            # Commit perubahan
            self._db.commit()

            return jsonify({
                "msg": "Booking created",
                "booking_id": booking_id,
                "payment_id": payment_data['id'],
                "price": amount
            }), 201

        except Exception as e:
            print(e)
            self._db.rollback()
            return jsonify({"msg": "Error creating booking"}), 500

    def PayBooking(self):
        booking_id = self.data['booking_id']
        payment_id = self.data['payment_id']

        booking = self._db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return jsonify({"msg": "Booking not found"}), 404

        payment = self._db.query(PaymentInfo).filter(PaymentInfo.id == payment_id).first()
        if not payment:
            return jsonify({"msg": "Payment not found"}), 404

        event = self._db.query(Event).filter(Event.id == booking.event_id).first()

        # check is time is more than 30 min, than canceled booking automaticly
        if (has_time_passed(booking.created_at, 1) and payment.status != "SUCCESS"):
            booking.payment_status = "FAILED"
            payment.status = "FAILED"
            payment.payment_date = datetime.now()
            event.current_capacity -= 1
            event.is_fullybooked = event.current_capacity >= event.capacity
            event.is_available = not event.is_fullybooked
            event.tikets_count -= 1

            self._db.commit()
            return jsonify({"msg": "Payment declined due to timeout"}), 200

        if payment.staus == "SUCCESS":
            return jsonify({"msg": "Already paid"}), 200

        booking.payment_status = "SUCCESS"
        payment.status = "SUCCESS"
        payment.payment_date = datetime.now()

        try:
            self._db.commit()
            return jsonify({"msg": "Payment successful"}), 200
        except Exception as e:
            print(e)
            self._db.rollback()
            return jsonify({"msg": "Failed to process payment"}), 500



