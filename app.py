from flask_login import LoginManager, login_required, current_user
from controllers.BookingController import BookingController
from controllers.EventController import EventController
from controllers.LoginController import LoginController
from controllers.PaymentController import PaymentController
from controllers.VendoController import VendoController
from controllers.AdminController import AdminController
from models.Users import User
from models.Bookings import Booking
from models.Events import Event
from models.Enums import PaymentStatus
from models.LoginHistory import LoginHistory
from db.db import SessionLocal, engine
from db.base import Base
from flask_cors import CORS
from flask import Flask, render_template, redirect, url_for, request, abort, flash
from controllers.UserController import UserController
from UIControllers.DashboardController import AdminDashboard, OrganizerDashboard, UserDashboard, Dashboard
from config import APP_NAME, MAINTENANCE_MODE, DEFAULT_ROLE

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
        
        @app.route("/api/event/get-all", methods=["GET"])
        def get_all_events():
            events = EventController()
            return events.GetAll()

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

        @app.route('/api/booking/get-my-bookings', methods=["GET"])
        @login_required
        def get_my_bookings():
            booking = BookingController()
            return booking.GetMyBookings()

        @app.route("/api/booking/payment/pay", methods=["POST"])
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
        def check_payment_status(payment_id):
            payment = PaymentController()
            return payment.CheckStatus(payment_id=payment_id)

        @app.route("/api/payment/create", methods=["POST"])
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

        # vendor controller
        @app.route("/api/vendor/get", methods=["GET"])
        def get_vendor():
            vendor = VendoController()
            return vendor.GetAllVendor()

        # view route
        @app.route("/", methods=["GET"])
        def index():
            if MAINTENANCE_MODE:
                return "Situs sedang dalam pemeliharaan"
            return render_template("index.html")

        @app.route("/login", methods=["GET"])
        def login():
            return render_template("login.html")

        @app.route("/register", methods=["GET"])
        def register():
            return render_template("register.html")

        # @app.route("/dashboard", methods=["GET"])
        # @login_required
        # def dashboard():
        #     return render_template("dashboard.html")
        
        @app.route("/dashboard", methods=["GET"])
        @login_required
        def dashboard_view():
            user = current_user

            if user.role.value == 'admin':
                dashboard = AdminDashboard(user)
            elif user.role.value == 'organizer':
                dashboard = OrganizerDashboard(user)
            elif user.role.value == 'user':
                dashboard = UserDashboard(user)
            else:
                dashboard = Dashboard(user)  # fallback default, aman dari UnboundLocalError

            return render_template('dashboard.html',
                                sidebar_items=dashboard.get_sidebar_items(),
                                main_message=dashboard.get_main_message(),
                                page_title=dashboard.get_page_title())
        
        @app.route('/user_tiket')
        @login_required
        def user_tiket():
            user = current_user
            if user.role.value == 'admin':
                dashboard = AdminDashboard(user)
            elif user.role.value == 'organizer':
                dashboard = OrganizerDashboard(user)
            elif user.role.value == 'user':
                dashboard = UserDashboard(user)
            else:
                dashboard = Dashboard(user)

            session = SessionLocal()
            customer_id = current_user.id  # sesuaikan kalau perlu
            active_bookings = session.query(Booking).filter(
            Booking.customer_id == customer_id,
            Booking.payment_status.in_([
                PaymentStatus.PENDING,
                PaymentStatus.SUCCESS
            ])
            ).all()
            session.close()

            return render_template('user_tiket.html',
                                bookings=active_bookings,
                                user=user,
                                sidebar_items=dashboard.get_sidebar_items(),
                                page_title="Tiket Saya")
        
        @app.route('/riwayat_tiket')
        @login_required
        def riwayat_tiket():
            user = current_user
            if user.role.value == 'admin':
                dashboard = AdminDashboard(user)
            elif user.role.value == 'organizer':
                dashboard = OrganizerDashboard(user)
            elif user.role.value == 'user':
                dashboard = UserDashboard(user)
            else:
                dashboard = Dashboard(user)

            session = SessionLocal()
            customer_id = current_user.id

            # ✅ gunakan enum PaymentStatus bukan string
            bookings = session.query(Booking).filter(
                Booking.customer_id == customer_id,
                Booking.payment_status.in_([
                    PaymentStatus.SUCCESS,
                    PaymentStatus.REFUNDED,
                    PaymentStatus.CANCELLED
                ])
            ).all()
            session.close()

            return render_template('user_tiket.html',
                                bookings=bookings,
                                user=user,
                                sidebar_items=dashboard.get_sidebar_items(),
                                page_title="Riwayat Tiket")
    
        @app.route("/search", methods=["GET"])
        def search():
            query = request.args.get("q", "")
            # Anda bisa tambahkan logika pencarian di sini
            return render_template("search_results.html", query=query)
        
        @app.route("/profile", methods=["GET"])
        @login_required
        def profile():
            user = current_user

            if user.role.value == 'admin':
                dashboard = AdminDashboard(user)
            elif user.role.value == 'organizer':
                dashboard = OrganizerDashboard(user)
            elif user.role.value == 'user':
                dashboard = UserDashboard(user)
            else:
                dashboard = Dashboard(user)  # fallback default

            return render_template('profile.html',
                                page_title="Profil Pengguna",
                                sidebar_items=dashboard.get_sidebar_items(),
                                username=user.username,
                                email=user.email,
                                role=user.role.value)
        
        @app.route('/admin/dashboard')
        @login_required
        def admin_dashboard():
            if current_user.role.value != 'admin':
                return redirect(url_for('dashboard_view'))
            
            dashboard = AdminDashboard(current_user)
            session = SessionLocal()
            total_users = session.query(User).count()
            total_events = session.query(Event).count()
            total_tickets_sold = session.query(Booking).count()
            session.close()

            return render_template('dashboard_admin.html',
                                sidebar_items=dashboard.get_sidebar_items(),
                                page_title="Dashboard Admin",
                                total_users=total_users,
                                total_events=total_events,
                                total_tickets_sold=total_tickets_sold)

        @app.route('/pesanan')
        @login_required
        def pesanan():
            if current_user.role.value != 'admin':
                return redirect(url_for('dashboard_view'))
            
            dashboard = AdminDashboard(current_user)
            session = SessionLocal()
            bookings = session.query(Booking).join(Event).filter(Booking.customer_id == current_user.id).all()
            session.close()
            
            return render_template('pesanan.html', sidebar_items=dashboard.get_sidebar_items(), bookings=bookings)
        
        @app.route('/activity-log')
        @login_required
        def activity_log():
            dashboard = AdminDashboard(current_user)
            session = SessionLocal()
            logs = session.query(LoginHistory).filter_by(user_id=current_user.id).order_by(LoginHistory.logout_date.desc()).all()
            session.close()
            return render_template('activity_log.html', sidebar_items=dashboard.get_sidebar_items(), login_history=logs)
        
        @app.route('/dashboard/users')
        @login_required
        def dashboard_users():
            if current_user.role.value != 'admin':
                abort(403)
            dashboard = AdminDashboard(current_user)
            session = SessionLocal()
            users = session.query(User).order_by(User.created_at.desc()).all()
            session.close()
            return render_template('pengguna.html', sidebar_items=dashboard.get_sidebar_items(), users=users)


        @app.route('/dashboard/users/<string:user_id>/role', methods=['POST'])
        @login_required
        def ubah_role_user(user_id):
            if current_user.role.value != 'admin':
                abort(403)
            new_role = request.form.get('role')
            session = SessionLocal()
            user = session.query(User).filter_by(id=user_id).first()
            if user and user.id != current_user.id:
                user.role.value = new_role
                session.commit()
                flash('Role pengguna berhasil diubah.', 'success')
            session.close()
            return redirect(url_for('dashboard_users'))


        @app.route('/dashboard/users/<string:user_id>/hapus', methods=['POST'])
        @login_required
        def hapus_user(user_id):
            if current_user.role.value != 'admin':
                abort(403)
            session = SessionLocal()
            user = session.query(User).filter_by(id=user_id).first()
            if user and user.id != current_user.id:
                session.delete(user)
                session.commit()
                flash('Pengguna berhasil dihapus.', 'success')
            session.close()
            return redirect(url_for('dashboard_users'))
        

        @app.route('/admin/pengaturan')
        @login_required
        def pengaturan():
            if current_user.role.value != 'admin':
                abort(403)
            
            dashboard = AdminDashboard(current_user)

            pengaturan = {
                "app_name": APP_NAME,
                "maintenance_mode": MAINTENANCE_MODE,
                "default_role": DEFAULT_ROLE
            }

            return render_template('pengaturan.html', sidebar_items=dashboard.get_sidebar_items(), pengaturan=pengaturan)





    def run(self):
        self.app.run(debug=True, port=5555)
 
if __name__ == "__main__":
    eventWebsite = EventWebsite()
    eventWebsite.run()
