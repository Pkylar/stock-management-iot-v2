# Instruksi Menjalankan Sistem Manajemen Stok IoT

## Prerequisites
- PHP 8.0+
- Composer
- Node.js 16+
- MySQL/phpMyAdmin (XAMPP)
- Arduino IDE (untuk ESP32-CAM)

## 1. Setup Database

### Menggunakan XAMPP:
1. Download dan install XAMPP
2. Start Apache dan MySQL dari XAMPP Control Panel
3. Buka http://localhost/phpmyadmin
4. Import file `database/setup.sql`
5. Database `stock_management_iot` akan terbuat otomatis

### Manual MySQL:
```bash
mysql -u root -p
source ~/stock-management-iot/database/setup.sql
```

## 2. Setup Backend Laravel

```bash
cd ~/stock-management-iot/backend

# Install dependencies
composer install

# Generate app key
php artisan key:generate

# Setup database connection di .env
# DB_DATABASE=stock_management_iot
# DB_USERNAME=root
# DB_PASSWORD=

# Run migrations (opsional, sudah ada di setup.sql)
php artisan migrate

# Start Laravel server
php artisan serve
```

Backend akan berjalan di: http://localhost:8000

## 3. Setup Frontend Next.js

```bash
cd ~/stock-management-iot/frontend

# Install dependencies
npm install

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Start development server
npm run dev
```

Frontend akan berjalan di: http://localhost:3000

## 4. Setup ESP32-CAM

### Install Arduino IDE:
1. Download Arduino IDE dari arduino.cc
2. Install ESP32 board package
3. Install library dependencies (lihat esp32-cam/README.md)

### Upload Code:
1. Buka file `esp32-cam/qr_scanner.ino`
2. Ubah WiFi credentials:
   ```cpp
   const char* ssid = "YOUR_WIFI_SSID";
   const char* password = "YOUR_WIFI_PASSWORD";
   ```
3. Ubah IP address backend:
   ```cpp
   const char* apiUrl = "http://192.168.1.100:8000/api/scan-qr";
   ```
4. Select board: "AI Thinker ESP32-CAM"
5. Connect ESP32-CAM dengan jumper GPIO 0 ke GND
6. Upload code
7. Lepas jumper dan reset ESP32-CAM

## 5. Testing System

### Test Backend API:
```bash
# Test login
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password"}'

# Test QR scan endpoint
curl -X POST http://localhost:8000/api/scan-qr \
  -H "Content-Type: application/json" \
  -d '{"nama_barang":"Test Item","nomor_seri":"TEST001","mac_address":"00:1B:44:11:3A:B7"}'
```

### Test Frontend:
1. Buka http://localhost:3000
2. Login dengan: admin@example.com / password
3. Test semua fitur dashboard

### Test ESP32-CAM:
1. Buat QR Code dengan format: "nama_barang|nomor_seri|mac_address"
2. Contoh: "Laptop Dell|DL001|00:1B:44:11:3A:B7"
3. Scan QR Code dengan ESP32-CAM
4. Check serial monitor untuk log
5. Check dashboard untuk data baru

## 6. Troubleshooting

### Backend Issues:
- Pastikan MySQL running
- Check .env configuration
- Run `composer install` jika ada error dependencies

### Frontend Issues:
- Run `npm install` untuk install dependencies
- Check API URL di lib/api.ts
- Pastikan backend running di port 8000

### ESP32-CAM Issues:
- Check WiFi connection
- Verify API URL dan network connectivity
- Check serial monitor untuk error messages
- Pastikan QR code format benar

## 7. Default Login
- Email: admin@example.com
- Password: password

## 8. API Endpoints
- POST /api/login - Login user
- POST /api/register - Register user
- GET /api/items - Get all items
- POST /api/items - Create item
- PUT /api/items/{id} - Update item
- DELETE /api/items/{id} - Delete item
- GET /api/stock-histories - Get all histories
- POST /api/scan-qr - ESP32-CAM endpoint

## 9. QR Code Format
Format: "nama_barang|nomor_seri|mac_address"
Contoh: "Laptop Dell|DL001|00:1B:44:11:3A:B7"

Sistem siap digunakan untuk tugas akhir!