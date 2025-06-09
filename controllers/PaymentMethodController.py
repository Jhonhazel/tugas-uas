from flask import jsonify, render_template, request
from flask_login import current_user

from controllers.Controllers import Controller
from lib.encrypt_decrypt_card import encrypt_card_number, decrypt_card_number
from lib.model_to_dicts import model_to_dict
from lib.string_func import generate_random_string
from models.PaymentMethod import PaymentMethod


class PaymentMethodController(Controller):
    def __init__(self):
        super().__init__()

    def CreatePaymentMethod(self):
        if not current_user.is_authenticated:
            return jsonify({"msg": "unauthorized user"}), 403

        payment_method = {
            "id": generate_random_string(),
            "card_number": encrypt_card_number(self.data['card_number']),
            "bank_name": self.data['bank_name'],
            "card_type": self.data['card_type'],
            "expired_month": self.data['expired_month'],
            "expired_year": self.data['expired_year'],
            "placeholder_name": self.data['placeholder_name'],
            "user_id": current_user.id,
        }
        try:
            payment = PaymentMethod(**payment_method)
            self._db.add(payment)
            self._db.commit()
            self._db.refresh(payment)
        except Exception as e:
            self._db.rollback()
            print(e)
            return jsonify({"msg": str(e)}), 500
        finally:
            self._db.close()

        return jsonify({"msg": "kartu baru berhasil di tambahkan" }), 201

    def GetMyPaymentMehtod(self):
        try:
            payment = self._db.query(PaymentMethod).filter(PaymentMethod.user_id == current_user.id).all()

            if not payment:
                return []

            data = [model_to_dict(payment) for payment in payment]

            for d in data:
                decrypted_card_number = decrypt_card_number(d['card_number'])
                d['card_number'] = f"**** **** {decrypted_card_number[-4:]}"

            return data

        except Exception as e:
            return None
        finally:
            self._db.close()

    def GetDetailPaymentMethod(self, id):
        try:
            details = self._db.query(PaymentMethod).filter(PaymentMethod.id == id).first()

            if not details:
                return render_template("404.html"), 404

            data = model_to_dict(details)

            data['card_number'] = f"**** **** {decrypt_card_number(data['card_number'])[-4:]}"

            return data
        except Exception as e:
            print(e)
            return None

        finally:
            self._db.close()

    def DeletePaymentMethod(self):
        card_id = request.args.get('id')

        if not card_id:
            return jsonify({"msg": "id kartu tidak ditemukan"}), 403

        try:
            card = self._db.query(PaymentMethod).filter(PaymentMethod.id == card_id).first()
            if not card:
                return render_template("404.html"), 404

            if card:
                self._db.delete(card)
                self._db.commit()

            return jsonify({"msg": "Kartu berhasil dihapus"})

        except Exception as e:
            print(e)
            self._db.rollback()
            return jsonify({"msg": str(e)}), 500
        finally:
            self._db.close()
