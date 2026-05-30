#!/usr/bin/env python3
"""
QR Scanner - polls ESP32 camera, decodes QR, sends to Laravel backend.
Run on Mac/server: python3 qr_decoder.py
"""
import urllib.request
import json
import time
import cv2
import numpy as np

ESP32_URL = "http://10.236.60.215/capture"
BACKEND_URL = "http://10.236.60.169:8000/api/scan-barcode"
SCAN_INTERVAL = 2  # seconds

detector = cv2.QRCodeDetector()
last_payload = ""
last_time = 0

print("QR Scanner started. Polling ESP32...")

while True:
    try:
        resp = urllib.request.urlopen(ESP32_URL, timeout=5)
        img_array = np.frombuffer(resp.read(), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            continue

        val, _, _ = detector.detectAndDecode(img)
        if val and (val != last_payload or time.time() - last_time > 10):
            print(f"[QR] {val}")
            # Parse: kode_barang_jumlah_tipe
            parts_r = val.rsplit('_', 2)
            if len(parts_r) == 3:
                kode, jumlah, tipe = parts_r[0], int(parts_r[1]), parts_r[2]
                data = json.dumps({"kode_barang": kode, "jumlah": jumlah, "tipe": tipe}).encode()
                req = urllib.request.Request(BACKEND_URL, data=data, headers={"Content-Type": "application/json", "Accept": "application/json"})
                res = urllib.request.urlopen(req, timeout=5)
                print(f"[OK] {kode} qty={jumlah} tipe={tipe} -> HTTP {res.status}")
                last_payload = val
                last_time = time.time()
            else:
                print(f"[WARN] Invalid format: {val}")
    except Exception as e:
        print(f"[ERR] {e}")

    time.sleep(SCAN_INTERVAL)
