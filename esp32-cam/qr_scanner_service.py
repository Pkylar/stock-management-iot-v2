#!/usr/bin/env python3
import time
import sys
import requests
import cv2
import numpy as np

# ============ CONFIG ============
ESP32_IP = "10.246.250.179"
BACKEND_URL = "http://127.0.0.1:8000/api/scan-barcode"
SCAN_INTERVAL = 0.1
COOLDOWN = 3
# ================================

ESP32_CAPTURE = f"http://{ESP32_IP}/capture"
last_payload = ""
last_time = 0

try:
    detector = cv2.wechat_qrcode_WeChatQRCode()
    use_wechat = True
    print("Using WeChatQRCode detector")
except:
    detector = cv2.QRCodeDetector()
    use_wechat = False
    print("Using default QRCodeDetector")

def parse_qr(payload):
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
    try:
        r = requests.post(BACKEND_URL, json=data, headers={"Accept": "application/json"}, timeout=5)
        return r.status_code, r.json() if r.status_code == 200 else r.text
    except Exception as e:
        return 0, str(e)

def capture_image():
    try:
        resp = requests.get(ESP32_CAPTURE, timeout=3)
        if resp.status_code != 200 or len(resp.content) < 1000:
            return None
        img_array = np.frombuffer(resp.content, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            return None
        # Resize kecil biar decode lebih cepat
        img = cv2.resize(img, (320, 240))
        # Sharpen biar QR lebih mudah dibaca
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    except:
        return None

def decode_qr(img):
    if use_wechat:
        results, _ = detector.detectAndDecode(img)
        return results[0] if results else ""
    else:
        val, _, _ = detector.detectAndDecode(img)
        return val or ""

print(f"=== QR Scanner Service ===")
print(f"ESP32: {ESP32_CAPTURE}")
print(f"Backend: {BACKEND_URL}")
print(f"Scanning every {SCAN_INTERVAL}s...")
print()

while True:
    try:
        img = capture_image()
        if img is None:
            print("[ERR] Cannot connect to ESP32 - check WiFi")
            time.sleep(SCAN_INTERVAL)
            continue

        val = decode_qr(img)
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

    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(0)
    except Exception as e:
        print(f"[ERR] {e}")

    time.sleep(SCAN_INTERVAL)
