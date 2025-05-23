from flask import Flask
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