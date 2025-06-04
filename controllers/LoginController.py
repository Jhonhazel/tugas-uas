from datetime import datetime

from flask import request, jsonify, redirect, url_for
from flask_login import login_user, current_user, logout_user
from controllers.Controllers import Controller
from lib.comparePass import comparePass
from lib.string_func import generate_random_string
from models.Users import User
from models.LoginHistory import LoginHistory


class LoginController(Controller):
    def __init__(self):
        super().__init__()

    def Login(self):
        username = self.data['username']
        password = self.data['password']
        user = self._db.query(User).filter(User.username == username).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        if not comparePass(user.password, password):
            return jsonify({"message": "Incorrect password"}), 401

        # Simpan login history ke database dengan commit
        login_history = LoginHistory(
            id=generate_random_string(),
            user_id=user.id,
            device_id=generate_random_string()
        )
        self._db.add(login_history)
        self._db.commit()

        login_user(user)

        return jsonify({"message": "Login successful"}), 200

    def Logout(self):

        try:

            self._db.query(LoginHistory).filter_by(user_id=current_user.id, logout_date=None).update(
                {"logout_date": datetime.now()})
            self._db.commit()

            logout_user()
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            self._db.rollback()
            return jsonify({"message": "Logout failed"}), 401
