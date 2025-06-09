from flask_login import LoginManager, login_required, current_user
from constant.constant import DASHBOARD_UI_LIST, BANK_LIST, CARD_TYPE
from controllers.AdminController import AdminController
from controllers.BookingController import BookingController
from controllers.EventController import EventController
from controllers.LoginController import LoginController
from controllers.PaymentController import PaymentController
from controllers.PaymentMethodController import PaymentMethodController
from lib.get_current_user import get_current_user
from lib.model_to_dicts import model_to_dict
from models.PaymentMethod import PaymentMethod
from models.Users import User
from models.Bookings import Booking
from models.Events import Event
from models.Enums import PaymentStatusEnum
from models.LoginHistory import LoginHistory
from models.PaymentInfo import PaymentInfo
from models.Tickets import Ticket
from models.Users import User
from models.Customers import Customer
from db.db import SessionLocal, engine, Base
from flask_cors import CORS
from flask import Flask, render_template, redirect, url_for, request, abort, flash, make_response
from controllers.UserController import UserController
from flask_moment import Moment
from cryptography.fernet import Fernet
import pdfkit
from datetime import datetime
import uuid
from sqlalchemy.orm import joinedload

class EventWebsite:
    def __init__(self):
        self.app = Flask(__name__)
        self.moment = Moment(self.app)
        self.app.secret_key = 'super_secret_key'
        CORS(self.app, supports_credentials=True)
        self.routes()

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
        self.login_manager.login_view='login'
        self.login_manager.user_loader(self.load_user)

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

        # view route
        @app.route("/", methods=["GET"])
        def index():
            user = get_current_user()
            return render_template("index.html", current_user=user)
        
        @app.route("/events", methods=["GET"])
        def events():
            session = SessionLocal()
            events = session.query(Event).order_by(Event.started_at.desc()).all()
            return render_template('events.html', events=events)

        @app.route("/login", methods=["GET"])
        def login():
            return render_template("login.html")

        @app.route("/register", methods=["GET"])
        def register():
            return render_template("register.html")

        @app.route("/dashboard", methods=["GET"])
        @login_required
        def dashboard_view():
            user = current_user
            sidebar_items = DASHBOARD_UI_LIST[user.role.value]

            return render_template('dashboard.html',
                                sidebar_items=sidebar_items)
        
        @app.route('/user_tiket')
        @login_required
        def user_tiket():
            sidebar_items = DASHBOARD_UI_LIST.get(current_user.role.value, [])

            session = SessionLocal()
            customer_id = current_user.id

            active_bookings = (
                session.query(Booking)
                .options(
                    joinedload(Booking.event),  
                    joinedload(Booking.customer)  
                )
                .filter(
                    Booking.user_id == customer_id,
                    Booking.payment_status.in_([PaymentStatusEnum.PENDING, PaymentStatusEnum.SUCCESS])
                )
                .all()
            )
            results = []
            for booking in active_bookings:
                results.append({
                    "booking": model_to_dict(booking),
                    "event": model_to_dict(booking.event),
                    "customer": model_to_dict(booking.customer),
                })

            return render_template('user_tiket.html', bookings=results, user=current_user, sidebar_items=sidebar_items)


        @app.route('/riwayat_tiket')
        @login_required
        def riwayat_tiket():
            sidebar_items = DASHBOARD_UI_LIST.get(current_user.role.value, [])

            session = SessionLocal()
            customer_id = current_user.id

            bookings = (
                session.query(Booking)
                .filter(
                    Booking.user_id == customer_id,
                    Booking.payment_status.in_([PaymentStatusEnum.SUCCESS, PaymentStatusEnum.REFUNDED, PaymentStatusEnum.CANCELLED])
                )
                .join(Event)  
                .all()
            )
            
            results = []
            for booking in bookings:
                results.append({
                    "booking": model_to_dict(booking),
                    "event": model_to_dict(booking.event),
                    "customer": model_to_dict(booking.customer),
                })

            return render_template('user_tiket.html', bookings=results, user=current_user, sidebar_items=sidebar_items)

        # paymenet method api
        @app.route('/api/payment/method/add', methods=["POST"])
        @login_required
        def add_payment_method():
            payment = PaymentMethodController()
            return payment.CreatePaymentMethod()

        @app.route('/api/payment/method/remove', methods=["DELETE"])
        @login_required
        def remove_payment_method():
            payment = PaymentMethodController()
            return payment.DeletePaymentMethod()

        @app.route("/search", methods=["GET"])
        def search():
            query = request.args.get("q", "")
            return render_template("search_results.html", query=query)
        
        @app.route("/profile", methods=["GET"])
        @login_required
        def profile():
            user = current_user
            sidebar_items = DASHBOARD_UI_LIST[user.role.value]

            return render_template('profile.html',
                                sidebar_items=sidebar_items,
                                username=user.username,
                                email=user.email,
                                role=user.role.value)
        
        @app.route('/admin/dashboard')
        @login_required
        def admin_dashboard():
            user = current_user
            if user.role.value != 'admin':
                return redirect(url_for('dashboard_view'))
            
            sidebar_items = DASHBOARD_UI_LIST[user.role.value]
            session = SessionLocal()
            total_users = session.query(User).count()
            total_events = session.query(Event).count()
            total_tickets_sold = session.query(Booking).count()
            session.close()

            return render_template('dashboard_admin.html',
                                sidebar_items=sidebar_items,
                                total_users=total_users,
                                total_events=total_events,
                                total_tickets_sold=total_tickets_sold)

        @app.route('/pesanan')
        @login_required
        def pesanan():
            if current_user.role.value != 'admin':
                return redirect(url_for('dashboard_view'))
            
            sidebar_items = DASHBOARD_UI_LIST[current_user.role.value]

            session = SessionLocal()
            bookings = (
                session.query(Booking)
                .join(Event)
                .join(Customer)
                .all()
            )
            return render_template('pesanan.html', sidebar_items=sidebar_items, bookings=bookings)
        
        @app.route('/activity-log')
        @login_required
        def activity_log():
            sidebar_items = DASHBOARD_UI_LIST[current_user.role.value]

            session = SessionLocal()
            logs = session.query(LoginHistory).filter_by(user_id=current_user.id).order_by(LoginHistory.logout_date.desc()).all()
            session.close()
            return render_template('activity_log.html', sidebar_items=sidebar_items, login_history=logs)
        
        @app.route('/dashboard/users')
        @login_required
        def dashboard_users():
            user = current_user
            if user.role.value != 'admin':
                return redirect(url_for('dashboard_view'))
            
            sidebar_items = DASHBOARD_UI_LIST[user.role.value]
            session = SessionLocal()
            users = session.query(User).order_by(User.created_at.desc()).all()
            session.close()
            return render_template('pengguna.html', sidebar_items=sidebar_items, users=users)


        @app.route('/dashboard/users/<string:user_id>/role', methods=['POST'])
        @login_required
        def ubah_role_user(user_id):
            user = current_user
            if user.role.value != 'admin':
                return redirect(url_for('dashboard_view'))
            
            new_role = request.form.get('role')
            session = SessionLocal()
            user = session.query(User).filter_by(id=user_id).first()
            if user and user.id != user.role.value:
                user.role.value = new_role
                session.commit()
                flash('Role pengguna berhasil diubah.', 'success')
            session.close()
            return redirect(url_for('dashboard_users'))


        @app.route('/dashboard/users/<string:user_id>/hapus', methods=['POST'])
        @login_required
        def hapus_user(user_id):
            if current_user.role.value != 'admin':
                return redirect(url_for('dashboard_view'))
            
            session = SessionLocal()
            user = session.query(User).filter_by(id=user_id).first()
            if user and user.id != current_user.id:
                session.delete(user)
                session.commit()
                flash('Pengguna berhasil dihapus.', 'success')
            session.close()
            return redirect(url_for('dashboard_users'))
        
        @app.route("/pengaturan", methods=["GET", "POST"])
        @login_required
        def dashboard_pengaturan():
            sidebar_items = DASHBOARD_UI_LIST[current_user.role.value]
            session = SessionLocal()

            if request.method == "POST":
                new_username = request.form["username"]
                new_email = request.form["email"]
                new_password = request.form["password"]

                current_user.username = new_username
                current_user.email = new_email

                if new_password:
                    current_user.set_password(new_password)

                session.add(current_user)
                session.commit()
                flash("Profil berhasil diperbarui.", "success")
                return redirect(url_for("profile"))

            method = PaymentMethodController()

            detail_id = request.args.get("detail")
            detail = None
            if detail_id:
                detail = method.GetDetailPaymentMethod(detail_id)

            return render_template(
                "dashboard_pengaturan.html",
                sidebar_items=sidebar_items,
                methods=method.GetMyPaymentMehtod(),
                detail=detail
            )


        
        @app.route('/organizer/dashboard')
        @login_required
        def organizer_dashboard():
            if current_user.role.value != 'organizer':
                return redirect(url_for('dashboard_view'))
            
            sidebar_items = DASHBOARD_UI_LIST[current_user.role.value]

            session = SessionLocal()

            organizer_events = session.query(Event).filter_by(user_id=current_user.id).all()
            event_ids = [event.id for event in organizer_events]

            bookings = session.query(Booking, Customer).join(Customer, Customer.id == Booking.customer_id).filter(Booking.event_id.in_(event_ids)).all()

            payment_ids = [b.payment_id for b, c in bookings if b.payment_id is not None]
            payments = session.query(PaymentInfo).filter(PaymentInfo.id.in_(payment_ids)).all()

            session.close()

            return render_template('dashboard_organizer.html', 
                                sidebar_items=sidebar_items,
                                events=organizer_events,
                                bookings=bookings,
                                payment_info=payments)

        @app.route("/my-events")
        @login_required
        def my_events():
            session = SessionLocal()
            try:
                sidebar_items = DASHBOARD_UI_LIST[current_user.role.value]
                events = session.query(Event).filter_by(user_id=current_user.id).all()

                event_data = []
                for event in events:
                    tickets = session.query(Ticket).filter_by(event_id=event.id).all()
                    bookings = session.query(Booking).filter_by(event_id=event.id).all()
                    booking_ids = [b.id for b in bookings]
                    payment_ids = [b.payment_id for b in bookings if b.payment_id is not None]
                    payments = session.query(PaymentInfo).filter(PaymentInfo.id.in_(payment_ids)).all()
                    payments = []
                    if payment_ids:
                        payments = session.query(PaymentInfo).filter(PaymentInfo.id.in_(payment_ids)).all()
                    
                    total_income = sum(p.amount for p in payments)
                    tickets_sold = len(payment_ids)

                    started_at_str = event.started_at.strftime("%Y-%m-%d %H:%M") if event.started_at else ""
                    ended_at_str = event.ended_at.strftime("%Y-%m-%d %H:%M") if event.ended_at else ""

                    event_data.append({
                        'id': event.id,
                        'name': event.name,
                        'started_at': started_at_str,
                        'ended_at': ended_at_str,
                        'price': event.price,
                        'tickets_sold': tickets_sold,
                        'total_income': total_income,
                        'date': event.started_at,

                    })

                return render_template("my_events.html", sidebar_items=sidebar_items, events=event_data)
            finally:
                session.close()
        
        @app.route("/add-event", methods=["GET"])
        @login_required
        def show_add_event_form():
            sidebar_items = DASHBOARD_UI_LIST[current_user.role.value]
            return render_template("add_event.html", sidebar_items=sidebar_items)


        @app.route("/add-event", methods=["POST"])
        @login_required
        def add_event():
            if not request.is_json:
                return {"message": "Expected JSON data"}, 400
            
            data = request.get_json()

            required_fields = ['name', 'description', 'venue_address', 'started_at', 'ended_at', 'price', 'capacity']
            for field in required_fields:
                if field not in data:
                    return {"message": f"Field '{field}' wajib diisi"}, 400

            try:
                started_at = datetime.strptime(data['started_at'], "%Y-%m-%d %H:%M:%S")
                ended_at = datetime.strptime(data['ended_at'], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return {"message": "Format tanggal salah, harus yyyy-mm-dd HH:MM:SS"}, 400

            event_id = str(uuid.uuid4())[:12] 

            new_event = Event(
                id=event_id,
                name=data['name'],
                description=data['description'],
                capacity=int(data['capacity']),
                current_capacity=0,
                tikets_count=0,
                started_at=started_at,
                ended_at=ended_at,
                price=float(data['price']),
                venue_address=data['venue_address'],
                is_fullybooked=False,
                user_id=current_user.id
            )

            session = SessionLocal()
            try:
                session.add(new_event)
                session.commit()
            except Exception as e:
                session.rollback()
                return {"message": f"Gagal menyimpan event: {str(e)}"}, 500
            finally:
                session.close()

            return {"message": "Event berhasil ditambahkan", "event_id": event_id}



        @app.route("/edit-event/<string:event_id>", methods=["GET", "POST"])
        @login_required
        def edit_event(event_id):
            session = SessionLocal()
            try:
                event = session.query(Event).filter_by(id=event_id).first()
                sidebar_items = DASHBOARD_UI_LIST[current_user.role.value]

                if not event:
                    flash("Event tidak ditemukan.", "danger")
                    return redirect(url_for("my_events"))

                if event.user_id != current_user.id:
                    flash("Anda tidak memiliki izin untuk mengedit event ini.", "danger")
                    return redirect(url_for("my_events"))

                if request.method == "POST":
                    event.name = request.form.get("name")
                    event.started_at = request.form.get("date")
                    event.ended_at = request.form.get("date")
                    event.price = float(request.form.get("price"))

                    session.commit()
                    flash("Event berhasil diperbarui.", "success")
                    return redirect(url_for("my_events"))

                return render_template("add_event.html", sidebar_items=sidebar_items, event=event)
            finally:
                session.close()

        @app.route("/delete-event/<string:event_id>", methods=["POST"])
        @login_required
        def delete_event(event_id):
            session = SessionLocal()
            try:
                event = session.query(Event).filter_by(id=event_id).first()

                if not event:
                    flash("Event tidak ditemukan.", "danger")
                    return redirect(url_for("my_events"))

                if event.user_id != current_user.id:
                    flash("Anda tidak memiliki izin untuk menghapus event ini.", "danger")
                    return redirect(url_for("my_events"))

                session.delete(event)
                session.commit()
                flash("Event berhasil dihapus.", "success")
                return redirect(url_for("my_events"))
            finally:
                session.close()
        
        @app.route("/laporan")
        @login_required
        def laporan():
            session = SessionLocal()
            user_events = session.query(Event).filter_by(user_id=current_user.id).all()

            laporan_data = []
            user = current_user
            sidebar_items = DASHBOARD_UI_LIST[user.role.value]

            for event in user_events:
                bookings = session.query(Booking).filter_by(event_id=event.id).all()
                user_ids = list(set(b.user_id for b in bookings))
                tickets = session.query(Ticket).filter_by(event_id=event.id).all()

                payment_ids = [b.payment_id for b in bookings if b.payment_id is not None]
               
                payments = []
                if payment_ids:
                    payments = session.query(PaymentInfo).filter(PaymentInfo.id.in_(payment_ids)).all()
                
                total_income = sum(p.amount for p in payments)
                tickets_sold = len(payment_ids)

                customers = session.query(Customer).filter(Customer.user_id.in_(user_ids)).all()

                laporan_data.append({
                    'id': event.id,
                    'name': event.name,
                    'tickets_sold': tickets_sold,
                    'total_income': total_income,
                    'customers': customers
                })

            session.close()
            return render_template("laporan.html", sidebar_items=sidebar_items, events=laporan_data)

        @app.route("/download-laporan/<string:event_id>")
        @login_required
        def download_laporan(event_id):
            session = SessionLocal()

            event = session.query(Event).filter_by(id=event_id).first()
            if not event:
                abort(404, description="Event tidak ditemukan")

            if event.user_id != current_user.id:
                abort(403, description="Anda tidak memiliki akses ke laporan ini")

            bookings = session.query(Booking).filter_by(event_id=event.id).all()

            payment_ids = [b.payment_id for b in bookings if b.payment_id is not None]

            payments = []
            if payment_ids:
                payments = session.query(PaymentInfo).filter(PaymentInfo.id.in_(payment_ids)).all()

            total_income = sum(p.amount for p in payments)

            tickets_sold = len(payment_ids) 

            event_data = {
                'id': event.id,
                'name': event.name,
                'started_at': event.started_at,
                'ended_at': event.ended_at,
                'venue_address': event.venue_address,
                'tickets_sold': tickets_sold,
                'total_income': total_income
            }

            rendered = render_template("event_pdf.html", event=event_data)

            pdf = pdfkit.from_string(rendered, False)

            response = make_response(pdf)
            response.headers["Content-Type"] = "application/pdf"
            response.headers["Content-Disposition"] = f"attachment; filename=laporan_{event.id}.pdf"

            session.close()
            return response

        @app.route("/download-customers/<string:event_id>")
        @login_required
        def download_customers(event_id):
            session = SessionLocal()

   
            event = session.query(Event).filter_by(id=event_id).first()
            if not event:
                abort(404, description="Event tidak ditemukan")

            if event.user_id != current_user.id:
                abort(403, description="Anda tidak memiliki akses ke laporan ini")

            customers = session.query(Customer).join(Booking).filter(Booking.event_id == event.id).all()

            event_data = {
                'id': event.id,
                'name': event.name,
                'started_at': event.started_at,
                'ended_at': event.ended_at,
                'venue_address': event.venue_address
            }

            rendered = render_template("customer_pdf.html", event=event_data, customers=customers)
            pdf = pdfkit.from_string(rendered, False)

            response = make_response(pdf)
            response.headers["Content-Type"] = "application/pdf"
            response.headers["Content-Disposition"] = f"attachment; filename=daftar_customer_{event.id}.pdf"
            return response
        
        @app.route('/event/detail/<string:event_id>', methods=["GET"])
        @login_required
        def event_detail(event_id):
            session = SessionLocal()
            try:
                event = session.query(Event).filter_by(id=event_id).first()
                image_index = request.args.get('img', '4803')  
                if not event:
                    abort(404)
                return render_template('events_detail.html', event=event, image_index=image_index)
            finally:
                session.close()

        
        @app.route('/tambah-metode-pembayaran', methods=["GET"])
        def tambah_metode_pembayaran():
            user = current_user
            sidebar_items = DASHBOARD_UI_LIST[user.role.value]

            if not current_user.is_authenticated:
                return render_template("404.html")

            return render_template('tambah_metode_pembayaran.html', sidebar_items=sidebar_items, card_type=CARD_TYPE, banks=BANK_LIST)
        
        @app.route('/events/<event_id>/book', methods=["GET"])
        def event_book(event_id):
            event = EventController()
            event_data = event.GetDetails(event_id)
            return render_template('customers_form.html', event=event_data)

        @app.route('/events/<event_id>/customer', methods=['POST'])
        @login_required
        def submit_customer(event_id):
            session = SessionLocal()
            try:
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                phone = request.form.get('phone')
                email = request.form.get('email')
                address = request.form.get('address')
                gov_id = request.form.get('gov_id')

                if not all([first_name, last_name, phone, email, address, gov_id]):
                    abort(400, "Data customer tidak lengkap")

                customer_id = str(uuid.uuid4())[:12]
                new_customer = Customer(
                    id=customer_id,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    email=email,
                    address=address,
                    gov_id=gov_id,
                    user_id=current_user.id
                )
                session.add(new_customer)
                session.commit()

                booking = session.query(Booking).filter_by(
                    customer_id=customer_id,
                    event_id=event_id
                ).first()

                if not booking:
                    abort(404, "Booking tidak ditemukan setelah membuat customer.")

                return redirect(f'/event/pay/{event_id}/{booking.id}')
            except Exception as e:
                session.rollback()
                abort(500, f"Terjadi kesalahan: {str(e)}")
            finally:
                session.close()

        @app.route('/event/pay/<event_id>/<booking_id>', methods=["GET"])
        def event_payment(event_id, booking_id):
            event = EventController()
            event_data = event.GetDetails(event_id)
            if event_data == None:
                return render_template('404.html')

            method = PaymentMethodController()

            return render_template('events_booking.html', event=event_data, method=method.GetMyPaymentMehtod())

        @app.route('/events/<event_id>/book/<customer_id>', methods=['POST'])
        @login_required
        def book_event(event_id, customer_id):
            session = SessionLocal()
            try:
                amount = float(request.form.get('amount'))
                tax = float(request.form.get('tax'))
                payment_method_type = request.form.get('payment_method')
                bank_name = request.form.get('bank_name')
                card_number = request.form.get('card_number')

                if not payment_method_type or not card_number:
                    flash("Metode pembayaran dan nomor kartu/rekening wajib diisi", "danger")
                    return redirect(request.referrer)

                payment_id = str(uuid.uuid4())[:12]
                booking_id = str(uuid.uuid4())[:12]

                payment_info = PaymentInfo(
                    id=payment_id,
                    amount=amount,
                    tax=tax,
                    status=PaymentStatusEnum.PENDING,
                    user_id=current_user.id,
                    createdAt=datetime.now(),
                    payment_method_id=None  
                )
                session.add(payment_info)
                session.flush()

                booking = Booking(
                    id=booking_id,
                    customer_id=customer_id,
                    event_id=event_id,
                    payment_status=PaymentStatusEnum.PENDING,
                    payment_id=payment_id,
                    user_id=current_user.id
                )
                session.add(booking)
                session.commit()

                return redirect(url_for('payment_success', payment_id=payment_id))
            except Exception as e:
                session.rollback()
                flash(f"Terjadi kesalahan saat booking: {str(e)}", "danger")
                return redirect(request.referrer)
            finally:
                session.close()
                
        @app.route('/payment-success/<payment_id>', methods=['GET'])
        def payment_success(payment_id):
            session = SessionLocal()
            try:
                payment = session.query(PaymentInfo).filter_by(id=payment_id).first()
                if not payment:
                    return render_template('404.html'), 404

                if payment.status == PaymentStatusEnum.PENDING:
                    payment.status = PaymentStatusEnum.SUCCESS
                    booking = session.query(Booking).filter_by(payment_id=payment.id).first()
                    if booking and booking.payment_status == PaymentStatusEnum.PENDING:
                        booking.payment_status = PaymentStatusEnum.SUCCESS
                    session.commit()

                return render_template('payment-success.html', payment_data=payment)
            finally:
                session.close()

        @app.route('/payment-failed', methods=["GET"])
        def payment_failure():
            return render_template('payment-failed.html')

        
        @app.template_filter('formatdatetime')
        def format_datetime(value, format='%d %B %Y, %H:%M'):
            if value is None:
                return ""
            return value.strftime(format)



    def run(self):
        self.app.run(debug=True, port=5555)
 
if __name__ == "__main__":
    eventWebsite = EventWebsite()
    eventWebsite.run()
