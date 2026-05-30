# Library Dependencies untuk ESP32-CAM QR Scanner

## Library yang dibutuhkan:
1. ESP32 Board Package
2. ArduinoJson (versi 6.x)
3. quirc library untuk QR code detection

## Cara Install:
1. Buka Arduino IDE
2. Go to Tools > Board > Boards Manager
3. Search "ESP32" dan install "ESP32 by Espressif Systems"
4. Go to Sketch > Include Library > Manage Libraries
5. Search dan install:
   - ArduinoJson by Benoit Blanchon
   - quirc library (manual install dari GitHub)

## Manual Install quirc:
1. Download dari: https://github.com/dlbeer/quirc
2. Extract ke folder libraries Arduino
3. Restart Arduino IDE

## Pin Configuration ESP32-CAM:
- Gunakan pin configuration yang sudah ada di kode
- Pastikan jumper GPIO 0 ke GND saat upload
- Lepas jumper setelah upload selesai

## Format QR Code:
Format data dalam QR Code harus: "nama_barang|nomor_seri|mac_address"
Contoh: "Laptop Dell|DL001|00:1B:44:11:3A:B7"