from controllers.Controllers import Controller
from flask import jsonify

from lib.comparePass import hash_password
from lib.string_func import generate_random_string
from models.Users import User

class UserController(Controller):
    def __init__(self):
        super().__init__()

    def Create(self):
        user = self._db.query(User).filter(User.username == self.data['username']).first()

        if user:
            return jsonify({'msg': 'User Already Exists', "code": 400}), 400

        new_user = User(
            id=generate_random_string(),
            email=self.data['email'],
            username=self.data['username'],
            password=hash_password(self.data['password']),
        )
        self._db.add(new_user)
        self._db.commit()
        self._db.refresh(new_user)
        self._db.close()

        return jsonify({
            "msg": "User Created",
            "id": new_user.id,
            "code": 201
        }), 201

    def Get(self):
        try:
            users = self._db.query(User).all()
            result = [
                { "id", u.id, "nama", u.nama, "email", u.email, "uname", u.username }
                for u in users
            ]

            if result:
                return jsonify({
                    "data": result,
                    "code": 200
                }), 200
            else:
                return jsonify({
                    "msg": "User not found",
                    "code": 404
                }), 404

        finally:
            self._db.close()