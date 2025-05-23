from db.db import SessionLocal
from flask import request, jsonify

class Controller:
    def __init__(self):
        self._db = SessionLocal()
        self.data = request.json