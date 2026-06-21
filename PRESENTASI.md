# Rangkuman Presentasi - Sistem Manajemen Stok Berbasis IoT

## 1. Gambaran Umum Sistem

Sistem manajemen stok gudang yang menggunakan **ESP32-S3 Camera** untuk scan QR Code secara otomatis. Ketika QR Code di-scan, data stok langsung masuk ke aplikasi web secara realtime.

### Alur Kerja Sistem:
```
QR Code → ESP32-S3 Camera → Python Scanner Service → Laravel Backend → Web Dashboard
```

**Penjelasan:**
1. QR Code ditempelkan/ditunjukkan ke kamera ESP32-S3
2. ESP32-S3 mengambil gambar (JPEG) dan mengirim via WiFi
3. Python Scanner Service menerima gambar, decode QR Code menggunakan OpenCV
4. Data hasil decode dikirim ke Laravel Backend via REST API
5. Data tersimpan di MySQL dan tampil di Web Dashboard (Next.js)

---

## 2. Teknologi yang Digunakan

| Komponen | Teknologi | Fungsi |
|----------|-----------|--------|
| Frontend | Next.js (React + TypeScript) | Dashboard web untuk monitoring stok |
| Backend | Laravel (PHP 8.4) | REST API, logic bisnis, database |
| Database | MySQL | Penyimpanan data barang & riwayat |
| IoT Device | ESP32-S3 WROOM N16R8 | Kamera untuk capture gambar QR |
| Scanner Service | Python + OpenCV | Decode QR Code dari gambar kamera |
| QR Code | Format custom | Identifikasi barang masuk/keluar |

---

## 3. Format QR Code

Format: `kode_barang_jumlah_tipe`

**Contoh:**
- `BRG001_5_masuk` → Barang BRG001, jumlah 5, stok masuk
- `BRG002_3_keluar` → Barang BRG002, jumlah 3, stok keluar
- `B1_10_masuk` → Barang B1, jumlah 10, stok masuk

**Tipe yang tersedia:**
- `masuk` → Menambah stok barang
- `keluar` → Mengurangi stok barang

---

## 4. Komponen Sistem

### 4.1 ESP32-S3 Camera (IoT Device)
- **Board:** ESP32-S3 WROOM N16R8
- **Fungsi:** Mengambil gambar JPEG dan menyediakan via HTTP endpoint
- **Endpoint:** `http://[IP_ESP32]/capture` → Mengembalikan gambar JPEG
- **Resolusi:** QVGA (320x240 pixel)
- **Koneksi:** WiFi
- **Fitur:** Auto-restart setiap 30 menit untuk menjaga performa

### 4.2 Python Scanner Service
- **Fungsi:** Polling gambar dari ESP32, decode QR Code, kirim ke backend
- **Library:** OpenCV (QRCodeDetector), Requests
- **Interval scan:** Setiap 2 detik
- **Cooldown:** 3 detik setelah berhasil scan (mencegah duplikasi)
- **Timeout:** 30 detik (menyesuaikan kecepatan WiFi ESP32)

### 4.3 Laravel Backend (REST API)
- **Endpoint utama:** `POST /api/scan-barcode`
- **Input:** `{ kode_barang, jumlah, tipe }`
- **Logic:**
  - Jika barang belum ada & tipe "masuk" → buat barang baru
  - Jika barang sudah ada & tipe "masuk" → tambah stok
  - Jika barang sudah ada & tipe "keluar" → kurangi stok
  - Jika stok tidak cukup → tolak dengan error

### 4.4 Web Dashboard (Next.js)
**Halaman:**
- **Dashboard** → Ringkasan stok, statistik, aktivitas terbaru
- **Stok Barang** → CRUD barang, stok keluar manual
- **Riwayat** → Log semua pergerakan stok (filter masuk/keluar)
- **Login/Register** → Autentikasi pengguna

**Fitur Web:**
- Statistik total barang, total stok, stok rendah
- Aktivitas realtime (live indicator)
- Filter riwayat berdasarkan tipe (masuk/keluar)
- Tambah/Edit/Hapus barang manual
- Stok keluar manual dengan alamat pengiriman

---

## 5. Arsitektur Sistem

```
┌─────────────────┐     WiFi/HTTP      ┌──────────────────────┐
│   ESP32-S3      │ ──────────────────→ │  Python Scanner      │
│   Camera        │   GET /capture      │  Service (OpenCV)    │
│   (IoT Device)  │   (JPEG image)      │                      │
└─────────────────┘                     └──────────┬───────────┘
                                                   │
                                          POST /api/scan-barcode
                                          {kode_barang, jumlah, tipe}
                                                   │
                                                   ▼
┌─────────────────┐     HTTP API        ┌──────────────────────┐
│   Next.js       │ ◄────────────────── │  Laravel Backend     │
│   Frontend      │                     │  (REST API)          │
│   (Dashboard)   │ ──────────────────→ │                      │
└─────────────────┘                     └──────────┬───────────┘
                                                   │
                                                   ▼
                                        ┌──────────────────────┐
                                        │   MySQL Database     │
                                        │   - items            │
                                        │   - stock_histories  │
                                        └──────────────────────┘
```

---

## 6. Database Structure

### Tabel `items` (Barang)
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | INT | Primary key |
| nama_barang | VARCHAR | Nama barang |
| kode_barang | VARCHAR | Kode unik barang |
| jumlah_stok | INT | Jumlah stok saat ini |
| status_terakhir | VARCHAR | masuk/keluar |

### Tabel `stock_histories` (Riwayat)
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | INT | Primary key |
| barang_id | INT | Foreign key ke items |
| tipe | VARCHAR | masuk/keluar |
| jumlah | INT | Jumlah perubahan |
| keterangan | TEXT | Catatan |
| sumber | VARCHAR | esp32_cam / manual |
| created_at | TIMESTAMP | Waktu transaksi |

---

## 7. Cara Menjalankan Sistem

### Prasyarat:
- PHP 8.4 + Composer
- Node.js + npm
- MySQL
- Python 3 + pip
- ESP32-S3 + kabel USB

### Langkah:
1. **Database:** Buat database `stock_management` di MySQL
2. **Backend:**
   ```bash
   cd backend
   composer install
   cp .env.example .env
   php artisan key:generate
   # Edit .env (set DB_CONNECTION=mysql, DB_DATABASE=stock_management)
   php artisan migrate
   php artisan serve
   ```
3. **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
4. **ESP32:** Upload sketch `esp32-cam/qr_scanner/qr_scanner.ino` via Arduino IDE
5. **Scanner Service:**
   ```bash
   cd esp32-cam
   pip install opencv-python-headless requests
   # Edit ESP32_IP di qr_scanner_service.py sesuai IP ESP32
   python qr_scanner_service.py
   ```

---

## 8. Keunggulan Sistem

1. **Otomatis** — Scan QR Code langsung update stok tanpa input manual
2. **Realtime** — Data langsung muncul di dashboard web
3. **IoT-based** — Menggunakan ESP32-S3 sebagai perangkat edge
4. **Robust decoding** — OpenCV lebih tahan terhadap blur/noise dibanding library on-device
5. **Auto-recovery** — ESP32 auto-restart tiap 30 menit untuk menjaga stabilitas
6. **Dual input** — Bisa scan QR (otomatis) atau input manual via web
7. **Riwayat lengkap** — Semua pergerakan stok tercatat dengan sumber (ESP32/Manual)

---

## 9. Kendala & Solusi

| Kendala | Solusi |
|---------|--------|
| Kamera ESP32 blur (out of focus) | Pindah decoding ke server (Python + OpenCV) yang lebih robust |
| WiFi ESP32 lambat (~10 detik/transfer) | Set timeout 30 detik, gunakan resolusi QVGA |
| ESP32 single-threaded | Hanya 1 client yang boleh akses (scanner ATAU browser, bukan keduanya) |
| Memory leak setelah banyak request | Auto-restart ESP32 setiap 30 menit |
| AP Isolation di hotspot | Gunakan hotspot yang tidak memblokir komunikasi antar device |

---

## 10. Demo Flow

1. Nyalakan ESP32 (colok USB) → tunggu LED kedip 3x (WiFi connected)
2. Jalankan `php artisan serve` (backend)
3. Jalankan `npm run dev` (frontend)
4. Jalankan `python qr_scanner_service.py` (scanner)
5. Tunjukkan QR Code ke kamera ESP32
6. Tunggu ~10 detik → data muncul di web dashboard
7. Buka halaman Riwayat → terlihat log "Scan QR ESP32"
