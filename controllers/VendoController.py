from lib.model_to_dicts import model_to_dict
from models.Vendors import Vendor
from lib.string_func import generate_random_string
from controllers.Controllers import Controller
from flask import jsonify, request

class VendoController(Controller):
    def __init__(self):
        super().__init__()

    def CreateVendor(self):
        data = {
            "id": generate_random_string(),
            "name": self.data['name'],
            "brand": self.data['brand'],
            "address": self.data['address'],
            "support_type": self.data['support_type']
        }

        vendor = Vendor(**data)
        self._db.add(vendor)
        self._db.commit()
        self._db.refresh(vendor)
        self._db.close()

        return jsonify({ "msg": "Vendor Created", "id": data["id"] }), 201

    def GetAllVendor(self):
        vendors = self._db.query(Vendor).all()
        vendor_data = [model_to_dict(v) for v in vendors]

        return jsonify({
                "data": vendor_data,
                "code": 200
            }), 200