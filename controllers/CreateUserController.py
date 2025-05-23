from controllers.Controller import Controller
from db.db import SessionLocal
from flask import request, jsonify

from models.UsersModel import User

class CreateUserController(Controller):
    def __init__(self):
        self.__db = SessionLocal()
        self.data = request.json

    def CreateUser(self):
        new_user = User(
            nama=self.data['nama'],
            email=self.data['email'],
            username=self.data['username'],
            password=hash(self.data['password']),
        )
        self.__db.add(new_user)
        self.__db.commit()
        self.__db.refresh(new_user)
        self.__db.close()

        return jsonify({
            "msg": "User Created",
            "id": new_user.id,
            "code": 201
        }, 201)

    def GetUser(self):
        return jsonify({
            "msg": "User Found",
            "code": 200
        })