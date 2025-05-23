DB_PASS
kalo ga ada password di hapus aja

controllers --> folder buat nyimpen semua kontroller rute
|__Controller.py (abstract)
|__CreateUserController.py (controller buat registrasi user)

db --> folder buat nyimpen konfigurasi db
|__db.py (konfigurasi database)

models --> folder buat nyimpen semua schema database
|__UsersModel.py (Struktur tabel user)

alembic --> folder automasi buat migrasi schema database

app.py --> main program
