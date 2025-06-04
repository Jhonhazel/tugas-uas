from lib.model_to_dicts import model_to_dict
from models.Events import Event
from lib.string_func import generate_random_string
from controllers.Controllers import Controller
from flask import jsonify, request


class EventController(Controller):
    def __init__(self):
        super().__init__()

    def CreateEvent(self):
        data = {
            "id": generate_random_string(),
            "name": self.data['name'],
            "description": self.data['description'],
            "capacity": self.data['capacity'],
            "price": self.data['price'],
            "started_at": self.data['started_at'],
            "ended_at": self.data['ended_at'],
            "venue_address": self.data['venue_address'],
        }

        event = Event(**data)
        self._db.add(event)
        self._db.commit()
        self._db.refresh(event)
        self._db.close()

        return jsonify({ "msg": "event created", "id": data["id"] }), 201

    def GetAll(self):
        event = self._db.query(Event).all()

        if not event:
            return jsonify({"data": []}), 200

        return jsonify({ "data": [model_to_dict(e) for e in event] })