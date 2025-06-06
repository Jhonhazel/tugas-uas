from flask_login import LoginManager, login_required

from constant.constant import DASHBOARD_UI_LIST
from controllers.AdminController import AdminController
from controllers.BookingController import BookingController
from controllers.EventController import EventController
from controllers.LoginController import LoginController
from controllers.PaymentController import PaymentController
from lib.get_current_user import get_current_user
from models.Users import User
from db.db import SessionLocal, engine, Base
from flask_cors import CORS
from flask import Flask, render_template
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


        @app.route("/api/user/logout", methods=["GET"])
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
        @login_required
        def create_event():
            event = EventController()
            return event.CreateEvent()

        @app.route("/api/event/get-all", methods=["GET"])
        def get_all_events():
            events = EventController()
            return events.GetAll()


        @app.route("/api/event/get/details/<event_id>", methods=["GET"])
        def get_event(event_id):
            event = EventController()
            return event.GetDetails(event_id)

        # booking controller
        @app.route("/api/booking/create", methods=["POST"])
        @login_required
        def create_booking():
            booking = BookingController()
            return booking.CreateBooking()

        @app.route('/api/booking/get-my-bookings', methods=["GET"])
        @login_required
        def get_my_bookings():
            booking = BookingController()
            return booking.GetMyBookings()

        @app.route("/api/booking/payment/pay", methods=["POST"])
        @login_required
        def pay_booking():
            booking = BookingController()
            return booking.PayBooking()

        # payment controller
        @app.route('/api/payment/get-my-payments', methods=["GET"])
        @login_required
        def get_all_my_payments():
            payment = PaymentController()
            return payment.GetMyPayments()

        @app.route("/api/payment/check-status/<payment_id>", methods=["GET"])
        @login_required
        def check_payment_status(payment_id):
            payment = PaymentController()
            return payment.CheckStatus(payment_id=payment_id)

        @app.route("/api/payment/create", methods=["POST"])
        @login_required
        def create_payment():
            payment = PaymentController()
            return payment.CreatePayment()

        @app.route("/api/payment/cancel", methods=["POST"])
        @login_required
        def cancel_payment():
            payment = PaymentController()
            return payment.CancelPayment()

        @app.route("/api/payment/refund-my-booking", methods=["POST"])
        @login_required
        def refund_payment():
            payment = PaymentController()
            return payment.RefundPayment()

        # admin api
        @app.route("/api/admin/create", methods=["POST"])
        @login_required
        def create_admin():
            admin = AdminController()
            return admin.CreateAdmin()

        # view route
        @app.route("/", methods=["GET"])
        def index():
            current_user = get_current_user()
            return render_template("index.html", current_user=current_user)

        # dashboard ui
        @app.route("/admin/dashboard", methods=["GET"])
        @login_required
        def dashboard():
            user = get_current_user()
            sidebar_items = DASHBOARD_UI_LIST[user["role"]]
            return render_template("dashboard.html", sidebar_items=sidebar_items)

        @app.route("/pesanan", methods=["GET"])
        def pesanan():
            return render_template("pesanan.html")
        @app.route("/admin/dashboard/user", methods=["GET"])
        def dashboard_user():
            current_user = get_current_user()
            return render_template("pengguna.html", current_user=current_user)
        @app.route("/admin/dashboard/pengaturan", methods=["GET"])
        def dashboard_pengaturan():
            current_user = get_current_user()
            return render_template("pengaturan.html", current_user=current_user)

        @app.route('/user_tiket', methods=["GET"])
        def user_tiket():
            return render_template("user_tiket.html")

        @app.route('/profile', methods=["GET"])
        def profile():
            return render_template("profile.html")

        @app.route('/activity_log', methods=["GET"])
        def activity_log():
            return render_template("activity_log.html")

    #     auth ui
        @app.route("/login", methods=["GET"])
        def login():
            return render_template("login.html")

        @app.route("/register", methods=["GET"])
        def register():
            return render_template("register.html")


    def run(self):
        self.app.run(debug=True, port=5555)


if __name__ == "__main__":
    eventWebsite = EventWebsite()
    eventWebsite.run()
