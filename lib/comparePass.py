import bcrypt

def comparePass(hashed_password: str, plain_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(plain_password: str) -> str:
    # Ubah ke bytes, hash, lalu decode ke string agar bisa disimpan di DB
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')  # simpan string ini ke kolom password di database
