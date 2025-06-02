from flask_login import LoginManager, login_required, current_user
from controllers.LoginController import LoginController
from models.UsersModel import User
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


        # view route

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
