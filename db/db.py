from sqlalchemy.orm import sessionmaker, declarative_base

from env_local import DB_USER, DB_PASS, DB_HOST, DB_NAME

# Format MySQL URL
from sqlalchemy import create_engine, text

# URL awal tanpa DB_NAME untuk membuat database
DATABASE_URL = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}'
engine = create_engine(DATABASE_URL)

# Buat database jika belum ada
with engine.connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))

# Setelah database dibuat, buat engine baru yang terhubung ke database tersebut
DATABASE_URL = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()