from flask_login import current_user

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
            "vendor_id": self.data['vendor_id']
        }

        event = Event(**data)
        self._db.add(event)
        self._db.commit()
        self._db.refresh(event)
        self._db.close()

        return jsonify({ "msg": "event created", "id": data["id"] }), 201

    def GetAll(self):
        event_id = request.args.get('id')

        if event_id is not None:
            event = self._db.query(Event).filter(Event.id == event_id).first()

            if not event:
                return jsonify({"msg": "Event not found"}), 404

            return jsonify({
                "data": event,
                "code": 200
            }), 200

        events = self._db.query(Event).all()
        event_data = [model_to_dict(e) for e in events]
        return jsonify({
                "data": event_data,
                "code": 200
            }), 200
