from flask_login import LoginManager, login_required, current_user

from controllers.BookingController import BookingController
from controllers.EventController import EventController
from controllers.LoginController import LoginController
from controllers.PaymentController import PaymentController
from controllers.VendoController import VendoController
from models.Users import User
from db.db import SessionLocal, engine, Base
from flask_cors import CORS
from flask import Flask, render_template, redirect, url_for
from controllers.UserController import UserController

class EventWebsite:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'super_secret_key'
        CORS(self.app, supports_credentials=True)
        self.routes()

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
        self.login_manager.login_view='login'
        self.login_manager.user_loader(self.load_user)  # ⬅️ daftarkan loader-nya

        # Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def load_user(user_id):
        session = SessionLocal()
        user = session.query(User).filter(User.id == user_id).first()
        session.close()
        return user

    def routes(self):
        app = self.app

        @app.route("/api/user/create", methods=["POST"])
        def register_user():
            user = UserController()
            return user.Create()

        @app.route("/api/user/login", methods=["POST"])
        def login_user():
            login = LoginController()
            return login.Login()


        @app.route("/api/user/logout", methods=["GET","POST"])
        @login_required
        def logout_user():
            login = LoginController()
            return login.Logout()

        @app.route("/api/user/get", methods=["GET"])
        def get_user():
            user = UserController()
            return user.Get()


        # event api
        @app.route("/api/event/create", methods=["POST"])
        # @login_required
        def create_event():
            # if current_user.role != "admin":
            #     return {"msg": "Only admin can create event"}, 403

            event = EventController()
            return event.CreateEvent()


        @app.route("/api/event/get", methods=["GET"])
        def get_event():
            event = EventController()
            return event.GetAll()

        #vendor api
        @app.route("/api/vendor/create", methods=["POST"])
        # @login_required
        def create_vendor():
            # if current_user.role != "admin":
            #     return {"msg": "Only admin can create vendor"}, 403
            vendor = VendoController()
            return vendor.CreateVendor()

        # booking controller
        @app.route("/api/booking/create", methods=["POST"])
        def create_booking():
            booking = BookingController()
            return booking.CreateBooking()

        @app.route("/api/booking/payment/pay", methods=["POST"])
        def pay_booking():
            booking = BookingController()
            return booking.PayBooking()

        # payment controller
        @app.route("/api/payment/check-status/<payment_id>", methods=["GET"])
        def check_payment_status(payment_id):
            payment = PaymentController()
            return payment.CheckStatus(payment_id=payment_id)

        @app.route("/api/payment/create", methods=["POST"])
        def create_payment():
            payment = PaymentController()
            return payment.CreatePayment()

        # vendor controller
        @app.route("/api/vendor/get", methods=["GET"])
        def get_vendor():
            vendor = VendoController()
            return vendor.GetAllVendor()

        # view route
        @app.route("/", methods=["GET"])
        def index():
            return render_template("index.html")

        @app.route("/login", methods=["GET"])
        def login():
            return render_template("login.html")

        @app.route("/register", methods=["GET"])
        def register():
            return render_template("register.html")

        @app.route("/dashboard", methods=["GET"])
        @login_required
        def dashboard():
            return render_template("dashboard.html")



    def run(self):
        self.app.run(debug=True, port=5555)


if __name__ == "__main__":
    eventWebsite = EventWebsite()
    eventWebsite.run()
