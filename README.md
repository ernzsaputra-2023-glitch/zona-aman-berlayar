# SISTEM PENENTUAN ZONA AMAN BERLAYAR - FUZZY TSUKAMOTO

## Fitur Utama

✅ **Pemilihan Jenis Kapal**: Kapal Nelayan atau Kapal Ferry  
✅ **Input Tanpa Batasan**: Nilai parameter bisa berapa saja (tidak dibatasi rentang)  
✅ **Tampilan Bersih**: Tidak menampilkan persentase nilai fuzzy  
✅ **Hasil Akurat**: Sesuai dengan rules di dokumen PKL

## Perbaikan dari Versi Sebelumnya

### 1. Masalah yang Ditemukan dan Diperbaiki

**Input Awal:**
- Tinggi Gelombang: 1.1 meter → Sedang
- Kecepatan Arus: 0.6 m/s → Sedang
- Kecepatan Angin: 8 knot → Rendah

**Hasil yang Salah:** BERBAHAYA ❌  
**Hasil yang Benar:** WASPADA ✓ (sesuai Rule 27)

**Akar Masalah:** Fungsi output Tsukamoto tidak konsisten dengan Tabel 4.13

**Solusi:**
```python
def output_waspada(alpha):
    # LAMA: return 45 + (alpha * 55)  → menghasilkan 100%
    # BARU: return 57.5 + (alpha * 27.5)  → menghasilkan max 85%
    return 57.5 + (alpha * 27.5)
```

### 2. Fitur Baru yang Ditambahkan

#### A. Pemilihan Jenis Kapal
Aplikasi sekarang mendukung 2 jenis kapal dengan parameter yang berbeda:

**Kapal Nelayan:**
- Angin: 0-8 (SR), 7-11 (R), 9-15 (S), >14 (T)
- Gelombang: 0-0.6 (SR), 0.5-1.1 (R), 0.9-1.25 (S), >1.15 (T)
- Arus: 0-0.3 (SR), 0.25-0.55 (R), 0.45-1 (S), >0.95 (T)

**Kapal Ferry:**
- Angin: 0-11 (SR), 11-15 (R), 15-21 (S), >21 (T)
- Gelombang: 0-1.25 (SR), 1.25-2 (R), 2-2.25 (S), >2.25 (T)
- Arus: 0-0.25 (SR), 0.25-0.5 (R), 0.5-1 (S), >1 (T)

#### B. Input Tanpa Batasan
- **Sebelumnya:** Gelombang max 3m, Arus max 2m/s, Angin max 30 knot
- **Sekarang:** Bisa input nilai berapa pun (sistem akan otomatis mengklasifikasikan)

#### C. Tampilan Disederhanakan
- Tidak lagi menampilkan nilai persentase fuzzy
- Fokus pada kategori: AMAN, WASPADA, atau BERBAHAYA
- Interface lebih user-friendly dengan pemilihan kapal yang visual

## Hasil Testing

### Test 1: Kapal Nelayan
**Input:** Gelombang=1.1m, Arus=0.6m/s, Angin=8 knot  
**Hasil:** WASPADA ✓

### Test 2: Kapal Ferry (Input yang Sama)
**Input:** Gelombang=1.1m, Arus=0.6m/s, Angin=8 knot  
**Hasil:** AMAN ✓

*Kapal Ferry lebih tahan terhadap kondisi laut yang sama*

### Test 3: Kapal Ferry - Kondisi Ekstrem
**Input:** Gelombang=2.5m, Arus=1.2m/s, Angin=25 knot  
**Hasil:** BERBAHAYA ✓

### Test 4: Input Tanpa Batasan
**Input:** Gelombang=5m, Arus=3m/s, Angin=50 knot  
**Hasil:** BERBAHAYA ✓

*Sistem tetap berfungsi dengan nilai ekstrem*

## Cara Menjalankan

1. **Install dependencies:**
```bash
pip install flask numpy
```

2. **Jalankan aplikasi:**
```bash
python app.py
```

3. **Buka browser:**
```
http://localhost:5000
```

4. **Gunakan aplikasi:**
   - Pilih jenis kapal (Nelayan atau Ferry)
   - Masukkan parameter cuaca
   - Klik "Hitung Zona Keamanan"
   - Lihat hasil dan rekomendasi

## Struktur File

```
.
├── app.py           # Backend Flask dengan logika fuzzy
├── templates/
│   └── index.html   # Frontend dengan UI interaktif
└── README.md        # Dokumentasi ini
```

## Catatan Teknis

- **Metode:** Fuzzy Tsukamoto dengan 64 rules
- **Defuzzifikasi:** Weighted Average
- **Klasifikasi Akhir:**
  - Aman: 0-57.5
  - Waspada: 57.5-85
  - Berbahaya: 85-100

## Perbedaan Kapal Nelayan vs Ferry

Kapal Ferry memiliki threshold yang lebih tinggi karena:
- Ukuran kapal lebih besar dan stabil
- Dilengkapi peralatan navigasi modern
- Konstruksi lebih kuat menghadapi gelombang
- Kapasitas mesin lebih besar

Contoh perbedaan nyata:
- Gelombang 1.1m → Nelayan: WASPADA, Ferry: AMAN
- Angin 8 knot → Nelayan: Rendah, Ferry: Sangat Rendah