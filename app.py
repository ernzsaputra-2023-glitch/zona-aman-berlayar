from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

# 1 knot = 0.514444 m/s
KNOT_TO_MS = 0.514444

# ==================== FUNGSI KEANGGOTAAN KECEPATAN ANGIN (knot) ====================
# KAPAL NELAYAN - Tabel 4.2: 0-8, 7-11, 9-15, >14
def angin_nelayan_sr(x):
    if x <= 7:
        return 1
    elif 7 < x <= 8:
        return (8 - x) / (8 - 7)
    else:
        return 0

def angin_nelayan_r(x):
    if x <= 7:
        return 0
    elif 7 < x <= 8:
        return (x - 7) / (8 - 7)
    elif 8 <= x <= 9:
        return 1
    elif 9 < x <= 11:
        return (11 - x) / (11 - 9)
    else:
        return 0

def angin_nelayan_s(x):
    if x <= 9:
        return 0
    elif 9 < x <= 11:
        return (x - 9) / (11 - 9)
    elif 11 <= x <= 14:
        return 1
    elif 14 < x <= 15:
        return (15 - x) / (15 - 14)
    else:
        return 0

def angin_nelayan_t(x):
    if x <= 14:
        return 0
    elif 14 < x <= 15:
        return (x - 14) / (15 - 14)
    else:
        return 1


# KAPAL FERRY - (DISAMAKAN KE FILE WORD kamu): 0-12, 11-16, 14-21, >20
def angin_ferry_sr(x):
    if x <= 11:
        return 1
    elif 11 < x <= 12:
        return (12 - x) / (12 - 11)
    else:
        return 0

def angin_ferry_r(x):
    if x <= 11:
        return 0
    elif 11 < x <= 12:
        return (x - 11) / (12 - 11)
    elif 12 <= x <= 14:
        return 1
    elif 14 < x <= 16:
        return (16 - x) / (16 - 14)
    else:
        return 0

def angin_ferry_s(x):
    if x <= 14:
        return 0
    elif 14 < x <= 16:
        return (x - 14) / (16 - 14)
    elif 16 <= x <= 20:
        return 1
    elif 20 < x <= 21:
        return (21 - x) / (21 - 20)
    else:
        return 0

def angin_ferry_t(x):
    if x <= 20:
        return 0
    elif 20 < x <= 21:
        return (x - 20) / (21 - 20)
    else:
        return 1


# ==================== FUNGSI KEANGGOTAAN TINGGI GELOMBANG (meter) ====================
# KAPAL NELAYAN - Tabel 4.6: 0-0.6, 0.5-1.1, 0.9-1.25, >1.15
def gelombang_nelayan_sr(x):
    if x <= 0.5:
        return 1
    elif 0.5 < x <= 0.6:
        return (0.6 - x) / (0.6 - 0.5)
    else:
        return 0

def gelombang_nelayan_r(x):
    if x <= 0.5:
        return 0
    elif 0.5 < x <= 0.6:
        return (x - 0.5) / (0.6 - 0.5)
    elif 0.6 <= x <= 0.9:
        return 1
    elif 0.9 < x <= 1.1:
        return (1.1 - x) / (1.1 - 0.9)
    else:
        return 0

def gelombang_nelayan_s(x):
    if x <= 0.9:
        return 0
    elif 0.9 < x <= 1.1:
        return (x - 0.9) / (1.1 - 0.9)
    elif 1.1 <= x <= 1.15:
        return 1
    elif 1.15 < x <= 1.25:
        return (1.25 - x) / (1.25 - 1.15)
    else:
        return 0

def gelombang_nelayan_t(x):
    if x <= 1.15:
        return 0
    elif 1.15 < x <= 1.25:
        return (x - 1.15) / (1.25 - 1.15)
    else:
        return 1


# KAPAL FERRY - (DISAMAKAN KE FILE WORD kamu): 0-1.3, 1.25-2.05, 1.95-2.25, >2.2
def gelombang_ferry_sr(x):
    if x <= 1.25:
        return 1
    elif 1.25 < x <= 1.3:
        return (1.3 - x) / (1.3 - 1.25)
    else:
        return 0

def gelombang_ferry_r(x):
    if x <= 1.25:
        return 0
    elif 1.25 < x <= 1.3:
        return (x - 1.25) / (1.3 - 1.25)
    elif 1.3 <= x <= 1.95:
        return 1
    elif 1.95 < x <= 2.05:
        return (2.05 - x) / (2.05 - 1.95)
    else:
        return 0

def gelombang_ferry_s(x):
    if x <= 1.95:
        return 0
    elif 1.95 < x <= 2.05:
        return (x - 1.95) / (2.05 - 1.95)
    elif 2.05 <= x <= 2.2:
        return 1
    elif 2.2 < x <= 2.25:
        return (2.25 - x) / (2.25 - 2.2)
    else:
        return 0

def gelombang_ferry_t(x):
    if x <= 2.2:
        return 0
    elif 2.2 < x <= 2.25:
        return (x - 2.2) / (2.25 - 2.2)
    else:
        return 1


# ==================== FUNGSI KEANGGOTAAN KECEPATAN ARUS (m/s) ====================
# KAPAL NELAYAN - Tabel 4.10: 0-0.3, 0.25-0.55, 0.45-1, >0.95
def arus_nelayan_sr(x):
    if x <= 0.25:
        return 1
    elif 0.25 < x <= 0.3:
        return (0.3 - x) / (0.3 - 0.25)
    else:
        return 0

def arus_nelayan_r(x):
    if x <= 0.25:
        return 0
    elif 0.25 < x <= 0.3:
        return (x - 0.25) / (0.3 - 0.25)
    elif 0.3 <= x <= 0.45:
        return 1
    elif 0.45 < x <= 0.55:
        return (0.55 - x) / (0.55 - 0.45)
    else:
        return 0

def arus_nelayan_s(x):
    if x <= 0.45:
        return 0
    elif 0.45 < x <= 0.55:
        return (x - 0.45) / (0.55 - 0.45)
    elif 0.55 <= x <= 0.95:
        return 1
    elif 0.95 < x <= 1:
        return (1 - x) / (1 - 0.95)
    else:
        return 0

def arus_nelayan_t(x):
    if x <= 0.95:
        return 0
    elif 0.95 < x <= 1:
        return (x - 0.95) / (1 - 0.95)
    else:
        return 1


# KAPAL FERRY - (DISAMAKAN KE FILE WORD kamu): sama dengan Nelayan
def arus_ferry_sr(x):
    return arus_nelayan_sr(x)

def arus_ferry_r(x):
    return arus_nelayan_r(x)

def arus_ferry_s(x):
    return arus_nelayan_s(x)

def arus_ferry_t(x):
    return arus_nelayan_t(x)


# ==================== FUNGSI OUTPUT TSUKAMOTO ====================
def output_aman(alpha):
    return 57.5 - (alpha * 57.5)

def output_waspada(alpha):
    return 57.5 + (alpha * 27.5)

def output_berbahaya(alpha):
    return 85 + (alpha * 15)


# ==================== FUNGSI UTAMA FUZZY TSUKAMOTO ====================
def hitung_fuzzy_tsukamoto(tinggi_gelombang, kecepatan_arus, kecepatan_angin, jenis_kapal):
    # Pilih fungsi keanggotaan berdasarkan jenis kapal
    if jenis_kapal == 'nelayan':
        ang_sr = angin_nelayan_sr(kecepatan_angin)
        ang_r = angin_nelayan_r(kecepatan_angin)
        ang_s = angin_nelayan_s(kecepatan_angin)
        ang_t = angin_nelayan_t(kecepatan_angin)

        gel_sr = gelombang_nelayan_sr(tinggi_gelombang)
        gel_r = gelombang_nelayan_r(tinggi_gelombang)
        gel_s = gelombang_nelayan_s(tinggi_gelombang)
        gel_t = gelombang_nelayan_t(tinggi_gelombang)

        ar_sr = arus_nelayan_sr(kecepatan_arus)
        ar_r = arus_nelayan_r(kecepatan_arus)
        ar_s = arus_nelayan_s(kecepatan_arus)
        ar_t = arus_nelayan_t(kecepatan_arus)
    else:  # ferry
        ang_sr = angin_ferry_sr(kecepatan_angin)
        ang_r = angin_ferry_r(kecepatan_angin)
        ang_s = angin_ferry_s(kecepatan_angin)
        ang_t = angin_ferry_t(kecepatan_angin)

        gel_sr = gelombang_ferry_sr(tinggi_gelombang)
        gel_r = gelombang_ferry_r(tinggi_gelombang)
        gel_s = gelombang_ferry_s(tinggi_gelombang)
        gel_t = gelombang_ferry_t(tinggi_gelombang)

        ar_sr = arus_ferry_sr(kecepatan_arus)
        ar_r = arus_ferry_r(kecepatan_arus)
        ar_s = arus_ferry_s(kecepatan_arus)
        ar_t = arus_ferry_t(kecepatan_arus)

    # Rules - 64 aturan sesuai Tabel 4.11
    rules = []

    # R1-16: Angin Sangat Rendah
    rules.append(('AMAN', min(ang_sr, gel_sr, ar_sr)))
    rules.append(('AMAN', min(ang_sr, gel_sr, ar_r)))
    rules.append(('AMAN', min(ang_sr, gel_sr, ar_s)))
    rules.append(('WASPADA', min(ang_sr, gel_sr, ar_t)))
    rules.append(('AMAN', min(ang_sr, gel_r, ar_sr)))
    rules.append(('AMAN', min(ang_sr, gel_r, ar_r)))
    rules.append(('WASPADA', min(ang_sr, gel_r, ar_s)))
    rules.append(('WASPADA', min(ang_sr, gel_r, ar_t)))
    rules.append(('WASPADA', min(ang_sr, gel_s, ar_sr)))
    rules.append(('WASPADA', min(ang_sr, gel_s, ar_r)))
    rules.append(('WASPADA', min(ang_sr, gel_s, ar_s)))
    rules.append(('BERBAHAYA', min(ang_sr, gel_s, ar_t)))
    rules.append(('WASPADA', min(ang_sr, gel_t, ar_sr)))
    rules.append(('WASPADA', min(ang_sr, gel_t, ar_r)))
    rules.append(('BERBAHAYA', min(ang_sr, gel_t, ar_s)))
    rules.append(('BERBAHAYA', min(ang_sr, gel_t, ar_t)))

    # R17-32: Angin Rendah
    rules.append(('AMAN', min(ang_r, gel_sr, ar_sr)))
    rules.append(('AMAN', min(ang_r, gel_sr, ar_r)))
    rules.append(('AMAN', min(ang_r, gel_sr, ar_s)))
    rules.append(('WASPADA', min(ang_r, gel_sr, ar_t)))
    rules.append(('AMAN', min(ang_r, gel_r, ar_sr)))
    rules.append(('AMAN', min(ang_r, gel_r, ar_r)))
    rules.append(('WASPADA', min(ang_r, gel_r, ar_s)))
    rules.append(('WASPADA', min(ang_r, gel_r, ar_t)))
    rules.append(('WASPADA', min(ang_r, gel_s, ar_sr)))
    rules.append(('WASPADA', min(ang_r, gel_s, ar_r)))
    rules.append(('WASPADA', min(ang_r, gel_s, ar_s)))
    rules.append(('BERBAHAYA', min(ang_r, gel_s, ar_t)))
    rules.append(('WASPADA', min(ang_r, gel_t, ar_sr)))
    rules.append(('WASPADA', min(ang_r, gel_t, ar_r)))
    rules.append(('BERBAHAYA', min(ang_r, gel_t, ar_s)))
    rules.append(('BERBAHAYA', min(ang_r, gel_t, ar_t)))

    # R33-48: Angin Sedang
    rules.append(('WASPADA', min(ang_s, gel_sr, ar_sr)))
    rules.append(('WASPADA', min(ang_s, gel_sr, ar_r)))
    rules.append(('WASPADA', min(ang_s, gel_sr, ar_s)))
    rules.append(('BERBAHAYA', min(ang_s, gel_sr, ar_t)))
    rules.append(('WASPADA', min(ang_s, gel_r, ar_sr)))
    rules.append(('WASPADA', min(ang_s, gel_r, ar_r)))
    rules.append(('WASPADA', min(ang_s, gel_r, ar_s)))
    rules.append(('BERBAHAYA', min(ang_s, gel_r, ar_t)))
    rules.append(('WASPADA', min(ang_s, gel_s, ar_sr)))
    rules.append(('WASPADA', min(ang_s, gel_s, ar_r)))
    rules.append(('BERBAHAYA', min(ang_s, gel_s, ar_s)))
    rules.append(('BERBAHAYA', min(ang_s, gel_s, ar_t)))
    rules.append(('BERBAHAYA', min(ang_s, gel_t, ar_sr)))
    rules.append(('BERBAHAYA', min(ang_s, gel_t, ar_r)))
    rules.append(('BERBAHAYA', min(ang_s, gel_t, ar_s)))
    rules.append(('BERBAHAYA', min(ang_s, gel_t, ar_t)))

    # R49-64: Angin Tinggi
    rules.append(('WASPADA', min(ang_t, gel_sr, ar_sr)))
    rules.append(('WASPADA', min(ang_t, gel_sr, ar_r)))
    rules.append(('BERBAHAYA', min(ang_t, gel_sr, ar_s)))
    rules.append(('BERBAHAYA', min(ang_t, gel_sr, ar_t)))
    rules.append(('WASPADA', min(ang_t, gel_r, ar_sr)))
    rules.append(('WASPADA', min(ang_t, gel_r, ar_r)))
    rules.append(('BERBAHAYA', min(ang_t, gel_r, ar_s)))
    rules.append(('BERBAHAYA', min(ang_t, gel_r, ar_t)))
    rules.append(('BERBAHAYA', min(ang_t, gel_s, ar_sr)))
    rules.append(('BERBAHAYA', min(ang_t, gel_s, ar_r)))
    rules.append(('BERBAHAYA', min(ang_t, gel_s, ar_s)))
    rules.append(('BERBAHAYA', min(ang_t, gel_s, ar_t)))
    rules.append(('BERBAHAYA', min(ang_t, gel_t, ar_sr)))
    rules.append(('BERBAHAYA', min(ang_t, gel_t, ar_r)))
    rules.append(('BERBAHAYA', min(ang_t, gel_t, ar_s)))
    rules.append(('BERBAHAYA', min(ang_t, gel_t, ar_t)))

    # Inferensi dan Defuzzifikasi
    hasil_rules = []
    for status, alpha in rules:
        if alpha > 0:
            if status == 'AMAN':
                z = output_aman(alpha)
            elif status == 'WASPADA':
                z = output_waspada(alpha)
            else:
                z = output_berbahaya(alpha)
            hasil_rules.append((status, alpha, z))

    # Defuzzifikasi dengan Weighted Average
    if not hasil_rules:
        nilai_fuzzy = 50
    else:
        numerator = sum(alpha * z for _, alpha, z in hasil_rules)
        denominator = sum(alpha for _, alpha, z in hasil_rules)
        nilai_fuzzy = numerator / denominator

    # Tentukan kategori
    if nilai_fuzzy <= 57.5:
        kategori = "AMAN"
        warna = "success"
        rekomendasi = "Kondisi laut aman untuk berlayar. Tetap waspada terhadap perubahan cuaca."
    elif nilai_fuzzy <= 85:
        kategori = "WASPADA"
        warna = "warning"
        rekomendasi = "Berlayar dengan hati-hati. Pantau kondisi cuaca secara berkala dan siapkan peralatan keselamatan."
    else:
        kategori = "BERBAHAYA"
        warna = "danger"
        rekomendasi = "TIDAK DISARANKAN untuk berlayar. Kondisi laut sangat berbahaya. Tunggu hingga kondisi membaik."

    return {
        'jenis_kapal': jenis_kapal.capitalize(),
        'tinggi_gelombang': tinggi_gelombang,
        'kecepatan_arus': kecepatan_arus,
        'kecepatan_angin': kecepatan_angin,
        'nilai_fuzzy': round(nilai_fuzzy, 2),
        'kategori': kategori,
        'warna': warna,
        'rekomendasi': rekomendasi,
        'fuzzifikasi': {
            'angin': {
                'sangat_rendah': round(ang_sr, 3),
                'rendah': round(ang_r, 3),
                'sedang': round(ang_s, 3),
                'tinggi': round(ang_t, 3)
            },
            'gelombang': {
                'sangat_rendah': round(gel_sr, 3),
                'rendah': round(gel_r, 3),
                'sedang': round(gel_s, 3),
                'tinggi': round(gel_t, 3)
            },
            'arus': {
                'sangat_rendah': round(ar_sr, 3),
                'rendah': round(ar_r, 3),
                'sedang': round(ar_s, 3),
                'tinggi': round(ar_t, 3)
            }
        },
        'rules_fired': len(hasil_rules)
    }


# app.py (CUMA TAMBAH/UBAH ROUTE INI, YANG LAIN BIARIN)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


@app.route('/hitung', methods=['POST'])
def hitung():
    try:
        data = request.get_json()
        tinggi_gelombang = float(data['tinggi_gelombang'])

        # input arus sekarang dalam KNOT -> konversi ke m/s
        kecepatan_arus_knot = float(data['kecepatan_arus'])
        kecepatan_arus = kecepatan_arus_knot * KNOT_TO_MS

        kecepatan_angin = float(data['kecepatan_angin'])
        jenis_kapal = data['jenis_kapal']

        hasil = hitung_fuzzy_tsukamoto(tinggi_gelombang, kecepatan_arus, kecepatan_angin, jenis_kapal)

        # simpan juga nilai knot asli biar bisa ditampilkan di frontend
        hasil['kecepatan_arus_knot'] = kecepatan_arus_knot

        return jsonify(hasil)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
