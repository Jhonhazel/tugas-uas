from controllers.Controllers import Controller
from flask import jsonify
from models.UsersModel import User

class UserController(Controller):
    def __init__(self):
        super().__init__()

    def Create(self):
        new_user = User(
            nama=self.data['nama'],
            email=self.data['email'],
            username=self.data['username'],
            password=hash(self.data['password']),
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
        return jsonify({
            "msg": "User Found",
            "code": 200
        }), 200
