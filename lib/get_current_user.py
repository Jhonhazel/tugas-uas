from db.db import SessionLocal
from models.Users import User  # pastikan ini diimpor
from lib.model_to_dicts import model_to_dict  # pastikan fungsi ini ada
from flask_login import current_user  # jika pakai Flask

def get_current_user():
    # Validasi current_user
    if not hasattr(current_user, "id"):
        return None

    user_id = current_user.id
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        return model_to_dict(user)  # pastikan fungsi ini tersedia
    finally:
        session.close()

