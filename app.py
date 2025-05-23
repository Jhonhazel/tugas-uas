# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# from config import Config
#
# class BaseUser(UserMixin):
#     def __init__(self, id, username, role):
#         self.id = id
#         self.username = username
#         self.role = role
#
#     def get_role(self):
#         return "User"
#
# class AdminUser(BaseUser):
#     def get_role(self):
#         return "Admin"
#
# class RegularUser(BaseUser):
#     def get_role(self):
#         return "User"
#
# class EventWebsite:
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.app.secret_key = 'super_secret_key'
#         self.con = Config()
#         self.login_manager = LoginManager()
#         self.login_manager.init_app(self.app)
#         self.login_manager.login_view = 'login'
#         self.routes()
#         self.setup_login()
#
#     def setup_login(self):
#         @self.login_manager.user_loader
#         def load_user(user_id):
#             cur = self.con.mysql.cursor()
#             cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#             user = cur.fetchone()
#             cur.close()
#             if user:
#                 if user['role'] == 'admin':
#                     return AdminUser(user['id'], user['username'], user['role'])
#                 else:
#                     return RegularUser(user['id'], user['username'], user['role'])
#             return None
#
#     def routes(self):
#         app = self.app
#
#         @app.route('/register', methods=['GET', 'POST'])
#         def register():
#             error = None
#             success = None
#             if request.method == 'POST':
#                 username = request.form['username']
#                 password = request.form['password']
#
#                 cur = self.con.mysql.cursor()
#                 cur.execute("SELECT * FROM users WHERE username = %s", (username,))
#                 user = cur.fetchone()
#
#                 if user:
#                     error = "Username sudah terdaftar"
#                 else:
#                     hashed_pw = generate_password_hash(password)
#                     cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
#                                 (username, hashed_pw, 'user'))
#                     self.con.mysql.commit()
#                     success = "Registrasi berhasil. Silakan login."
#
#                 cur.close()
#             return render_template('registrasi.html', error=error, success=success)
#
#         @app.route('/', methods=['GET', 'POST'])
#         def login():
#             if request.method == 'POST':
#                 username = request.form['username']
#                 password = request.form['password']
#
#                 cur = self.con.mysql.cursor()
#                 cur.execute("SELECT * FROM users WHERE username = %s", (username,))
#                 user = cur.fetchone()
#                 cur.close()
#
#                 if user and check_password_hash(user['password'], password):
#                     user_obj = AdminUser(user['id'], user['username'], user['role']) if user['role'] == 'admin' else RegularUser(user['id'], user['username'], user['role'])
#                     login_user(user_obj)
#                     return redirect(url_for('home'))
#                 flash("Login gagal!", "error")
#             return render_template('login.html')
#
#         @app.route('/logout')
#         @login_required
#         def logout():
#             logout_user()
#             return redirect(url_for('login'))
#
#         @app.route('/home')
#         @login_required
#         def home():
#             cur = self.con.mysql.cursor()
#             cur.execute("SELECT * FROM events")
#             events = cur.fetchall()
#             cur.close()
#             return render_template('home.html', username=current_user.username, role=current_user.get_role(), events=events)
#
#         @app.route('/daftar/<int:event_id>', methods=['GET', 'POST'])
#         @login_required
#         def daftar_event(event_id):
#             cur = self.con.mysql.cursor()
#             cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
#             event = cur.fetchone()
#
#             if not event:
#                 flash("Event tidak ditemukan", "error")
#                 return redirect(url_for('home'))
#
#             if request.method == 'POST':
#                 jumlah = int(request.form['jumlah'])
#                 if event['kapasitas'] >= jumlah:
#                     sisa = event['kapasitas'] - jumlah
#                     cur.execute("UPDATE events SET kapasitas = %s WHERE id = %s", (sisa, event_id))
#                     cur.execute("INSERT INTO bookings (user_id, event_id, jumlah) VALUES (%s, %s, %s)",
#                                 (current_user.id, event_id, jumlah))
#                     self.con.mysql.commit()
#                     flash("Pendaftaran berhasil", "success")
#                     cur.close()
#                     return redirect(url_for('lihat_pendaftaran'))
#                 flash("Tiket tidak cukup tersedia", "error")
#             cur.close()
#             return render_template('daftar.html', event=event)
#
#         @app.route('/pendaftaran')
#         @login_required
#         def lihat_pendaftaran():
#             cur = self.con.mysql.cursor()
#             cur.execute("""
#                 SELECT e.nama AS event_nama, b.jumlah
#                 FROM bookings b
#                 JOIN events e ON b.event_id = e.id
#                 WHERE b.user_id = %s
#             """, (current_user.id,))
#             data = cur.fetchall()
#             cur.close()
#             return render_template('list_pendaftaran.html', bookings=data)
#
#         @app.route('/kelola_event')
#         @login_required
#         def kelola_event():
#             if current_user.get_role() != "Admin":
#                 flash("Akses ditolak", "error")
#                 return redirect(url_for('home'))
#             cur = self.con.mysql.cursor()
#             cur.execute("SELECT * FROM events")
#             events = cur.fetchall()
#             cur.close()
#             return render_template('kelola_event.html', events=events)
#
#     def run(self):
#         self.app.run(debug=True, port=5000)
#
# if __name__ == '__main__':
#     eventWeb = EventWebsite()
#     eventWeb.run()



from flask import Flask
from controllers.Controller import Controller
from controllers.CreateUserController import CreateUserController
from db.db import engine
from models.UsersModel import Base

class EventWebsite:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'super_secret_key'
        self.routes()
        Base.metadata.create_all(bind=engine)


    def routes(self):
        app = self.app
        @app.route("/api/user/create", methods=["POST"])
        def register_user():
            controller = CreateUserController()
            return controller.CreateUser()

    def run(self):
        self.app.run(debug=True, port=5555)


if __name__ == '__main__':
    eventWeb = EventWebsite()
    eventWeb.run()