#!/usr/bin/env python3
"""
QR Scanner Service
Polls ESP32 camera, decodes QR codes, sends data to Laravel backend.
Run this on the same machine as Laravel.

Install: pip install opencv-python-headless requests
Usage:   python qr_scanner_service.py

Config: Edit ESP32_IP and BACKEND_URL below.
"""
import time
import sys
import requests
import cv2
import numpy as np

# ============ CONFIG ============
ESP32_IP = "10.236.60.215"
BACKEND_URL = "http://127.0.0.1:8000/api/scan-barcode"
SCAN_INTERVAL = 2  # seconds between scans
COOLDOWN = 3       # seconds before same QR can be scanned again
# ================================

ESP32_CAPTURE = f"http://{ESP32_IP}/capture"
detector = cv2.QRCodeDetector()
last_payload = ""
last_time = 0

def parse_qr(payload):
    """Parse QR format: kode_barang_jumlah_tipe"""
    parts = payload.rsplit('_', 2)
    if len(parts) != 3:
        return None
    kode, jumlah_str, tipe = parts
    if tipe not in ('masuk', 'keluar'):
        return None
    try:
        jumlah = int(jumlah_str)
        if jumlah <= 0:
            return None
    except ValueError:
        return None
    return {"kode_barang": kode, "jumlah": jumlah, "tipe": tipe}

def send_to_backend(data):
    """Send parsed QR data to Laravel backend"""
    try:
        r = requests.post(BACKEND_URL, json=data, headers={"Accept": "application/json"}, timeout=5)
        return r.status_code, r.json() if r.status_code == 200 else r.text
    except Exception as e:
        return 0, str(e)

print(f"=== QR Scanner Service ===")
print(f"ESP32: {ESP32_CAPTURE}")
print(f"Backend: {BACKEND_URL}")
print(f"Scanning every {SCAN_INTERVAL}s...")
print()

while True:
    try:
        resp = requests.get(ESP32_CAPTURE, timeout=30)
        if resp.status_code != 200:
            time.sleep(SCAN_INTERVAL)
            continue

        img_array = np.frombuffer(resp.content, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            time.sleep(SCAN_INTERVAL)
            continue

        val, _, _ = detector.detectAndDecode(img)
        if val and (val != last_payload or time.time() - last_time > COOLDOWN):
            data = parse_qr(val)
            if data:
                status, result = send_to_backend(data)
                print(f"[OK] {val} -> HTTP {status}")
                if status == 200:
                    last_payload = val
                    last_time = time.time()
                else:
                    print(f"     Response: {result}")
            else:
                print(f"[WARN] Invalid QR format: {val}")

    except requests.exceptions.ConnectionError:
        print("[ERR] Cannot connect to ESP32 - check WiFi")
    except requests.exceptions.Timeout:
        pass  # normal when ESP32 is busy
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(0)
    except Exception as e:
        print(f"[ERR] {e}")

    time.sleep(SCAN_INTERVAL)
