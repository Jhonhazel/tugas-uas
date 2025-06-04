from flask import jsonify
from flask_login import current_user

from controllers.Controllers import Controller
from models.Users import User


class AdminController(Controller):
    def __init__(self):
        super().__init__()

    def check_admin_status(self):
        if current_user.is_anonymous:
            return False

        user = self._db.query(User).filter(User.id == current_user.id).first()
        return user.role.value == 'admin'

    def CreateAdmin(self):
        if not self.check_admin_status():
            return jsonify({"msg": "Unauthorized"}), 401


        return jsonify({"msg": "Admin created"}), 201