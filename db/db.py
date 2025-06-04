from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.Users import User, RoleUser
from lib.comparePass import hash_password  # pastikan path sesuai
import uuid
from db.base import Base 

DB_USER = 'root'
DB_PASS = ''
DB_HOST = '127.0.0.1:3306'
DB_NAME = 'tiket_event'

# 1. Koneksi awal untuk create DB
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}')
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
    conn.commit()

# 2. Koneksi ke DB yang sudah jadi
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Buat semua tabel
Base.metadata.create_all(bind=engine)

# 4. Fungsi buat ID unik pendek
def generate_id():
    return str(uuid.uuid4())[:12]

# 5. Seed akun admin dan organizer
def seed_users():
    session = SessionLocal()
    
    # Cek apakah user 'admin' sudah ada
    admin_exists = session.query(User).filter_by(username='admin').first()
    if not admin_exists:
        admin_user = User(
            id=generate_id(),
            email='admin@gmail.com',
            username='admin',
            password=hash_password('admin123'),
            role=RoleUser.admin
        )
        session.add(admin_user)

    organizer_exists = session.query(User).filter_by(username='organizer').first()
    if not organizer_exists:
        organizer_user = User(
            id=generate_id(),
            email='organizer@gmail.com',
            username='organizer',
            password=hash_password('organizer123'),
            role=RoleUser.organizer
        )
        session.add(organizer_user)
    
    session.commit()
    session.close()

seed_users()

