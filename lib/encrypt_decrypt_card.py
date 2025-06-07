from cryptography.fernet import Fernet
import os

FERNET_KEY = os.getenv("CARD_ENCRYPTION_KEY", "_a9joo927-Ozc-NhgayIu7axejKB_uy8I3Xo8z-ScQw=")
cipher = Fernet(FERNET_KEY)


def encrypt_card_number(card_number: str) -> str:
    """
    Enkripsi nomor kartu menggunakan AES (Fernet).
    """
    if not isinstance(card_number, str):
        raise ValueError("Card number harus berupa string")

    encrypted = cipher.encrypt(card_number.encode())
    return encrypted.decode()


def decrypt_card_number(encrypted_card: str) -> str:
    """
    Dekripsi nomor kartu terenkripsi.
    """
    if not isinstance(encrypted_card, str):
        raise ValueError("Encrypted card harus berupa string")

    decrypted = cipher.decrypt(encrypted_card.encode())
    return decrypted.decode()


def mask_card_number(card_number: str) -> str:
    """
    Masking nomor kartu: tampilkan 4 digit terakhir saja.
    """
    return "**** **** **** " + card_number[-4:]
