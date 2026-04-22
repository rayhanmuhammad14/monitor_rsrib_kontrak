from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from backend.conn import mitra_collection, client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    try:
        client.admin.command('ping')
        koneksi_sukses = True
        
        # Ambil semua data dari MongoDB
        semua_mitra = list(mitra_collection.find().sort("_id", -1))
        
        # --- LOGIKA PERHITUNGAN EXPIRE DI PYTHON ---
        hari_ini = datetime.now().date()
        
        for mitra in semua_mitra:
            # Pastikan tipe datanya adalah datetime
            if isinstance(mitra.get('kontrak'), datetime):
                tanggal_kontrak = mitra['kontrak'].date()
                sisa = (tanggal_kontrak - hari_ini).days
                
                # Format Teks & Warna yang akan dikirim ke HTML
                if sisa < 0:
                    mitra['status_teks'] = f"Expired ({abs(sisa)} hari lalu)"
                    mitra['status_warna'] = "danger"
                elif sisa <= 30:
                    mitra['status_teks'] = f"Expire dalam {sisa} Hari"
                    mitra['status_warna'] = "warning text-dark"
                else:
                    mitra['status_teks'] = f"Expire dalam {sisa} Hari"
                    mitra['status_warna'] = "success"
            else:
                mitra['status_teks'] = "Format Tanggal Salah"
                mitra['status_warna'] = "secondary"
                
    except Exception as e:
        print(f"Error Database: {e}")
        koneksi_sukses = False
        semua_mitra = []
        
    return render_template('index.html', sukses=koneksi_sukses, data=semua_mitra)

@app.route('/tambah_mitra', methods=['POST'])
def tambah_mitra():
    nama_mitra = request.form.get('nama_mitra')
    jenis = request.form.get('jenis')
    kontrak_str = request.form.get('kontrak') 
    
    if nama_mitra and jenis and kontrak_str:
        kontrak_date = datetime.strptime(kontrak_str, '%Y-%m-%d')
        
        mitra_collection.insert_one({
            "nama_mitra": nama_mitra,
            "jenis": jenis,
            "kontrak": kontrak_date,
            "input_at": datetime.now()
        })
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)