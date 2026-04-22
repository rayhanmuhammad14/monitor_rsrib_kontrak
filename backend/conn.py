import os
from dotenv import load_dotenv
from pymongo import MongoClient

# 1. CARI LOKASI .ENV DARI FOLDER UTAMA
# Perintah ini memaksa Python mundur 1 folder (dari /backend ke folder utama)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')

# 2. BACA FILE .ENV SESUAI LOKASI TEPATNYA
load_dotenv(ENV_PATH)

# 3. AMBIL VARIABEL DARI .ENV
MONGO_URI = os.getenv('MONGO_URI')
NAMA_DB = os.getenv('MONGO_DB')
NAMA_KOLEKSI = os.getenv('MONGO_COLLECT')

# 4. PENGECEKAN (Pesan error dibuat lebih detail)
if not MONGO_URI or not NAMA_DB or not NAMA_KOLEKSI:
    raise ValueError(f"Gagal! File .env tidak ditemukan di jalur: {ENV_PATH}\nAtau ada variabel yang salah ketik/kosong di dalam .env!")

# 5. HUBUNGKAN KE MONGODB
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client[NAMA_DB] 
mitra_collection = db[NAMA_KOLEKSI]