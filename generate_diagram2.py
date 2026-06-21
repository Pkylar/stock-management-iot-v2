import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(1, 1, figsize=(16, 22))
ax.set_xlim(0, 16)
ax.set_ylim(0, 22)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# Title
ax.text(8, 21.5, 'Activity Diagram - Keseluruhan Sistem Manajemen Stok IoT', 
        ha='center', va='center', fontsize=14, fontweight='bold')

# Swimlane headers
lanes = [
    (2, 'ESP32-S3\n(IoT Device)', '#27AE60'),
    (6, 'Python Scanner\n(Service)', '#8E44AD'),
    (10, 'Laravel\n(Backend)', '#E67E22'),
    (14, 'Next.js\n(Frontend)', '#3498DB')
]

for x, label, color in lanes:
    box = FancyBboxPatch((x-1.8, 20.5), 3.6, 0.8, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor='#2C3E50', linewidth=2, alpha=0.9)
    ax.add_patch(box)
    ax.text(x, 20.9, label, ha='center', va='center', fontsize=9, color='white', fontweight='bold')

# Vertical lane lines
for x, _, _ in lanes:
    ax.plot([x-1.8, x-1.8], [0.5, 20.5], '--', color='#BDC3C7', linewidth=0.8)
    ax.plot([x+1.8, x+1.8], [0.5, 20.5], '--', color='#BDC3C7', linewidth=0.8)

def draw_action(ax, x, y, text, color='#4A90D9', w=3.2):
    box = FancyBboxPatch((x-w/2, y-0.3), w, 0.6, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor='#2C3E50', linewidth=1.5, alpha=0.9)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')

def draw_decision(ax, x, y, text):
    diamond = plt.Polygon([[x, y+0.35], [x+1.2, y], [x, y-0.35], [x-1.2, y]],
                           facecolor='#F5A623', edgecolor='#2C3E50', linewidth=1.5)
    ax.add_patch(diamond)
    ax.text(x, y, text, ha='center', va='center', fontsize=7, fontweight='bold')

def arrow(ax, x1, y1, x2, y2, label='', color='#2C3E50'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my+0.15, label, fontsize=6.5, color='#666', ha='center', fontstyle='italic')

def draw_start(ax, x, y):
    circle = plt.Circle((x, y), 0.2, color='black', fill=True)
    ax.add_patch(circle)

def draw_end(ax, x, y):
    circle1 = plt.Circle((x, y), 0.25, color='black', fill=False, linewidth=2)
    circle2 = plt.Circle((x, y), 0.15, color='black', fill=True)
    ax.add_patch(circle1)
    ax.add_patch(circle2)

# === START ===
draw_start(ax, 8, 20)

# === Phase 1: Startup (row 19) ===
ax.text(8, 19.5, '── FASE 1: STARTUP SISTEM ──', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='#2C3E50')

arrow(ax, 8, 19.8, 2, 19.2)
arrow(ax, 8, 19.8, 10, 19.2)
arrow(ax, 8, 19.8, 14, 19.2)

# ESP32 startup
draw_action(ax, 2, 18.9, 'Power ON\n(colok USB)', '#27AE60')
arrow(ax, 2, 18.6, 2, 18.2)
draw_action(ax, 2, 17.9, 'Init Kamera\nQVGA 320x240', '#27AE60')
arrow(ax, 2, 17.6, 2, 17.2)
draw_decision(ax, 2, 16.8, 'WiFi OK?')
arrow(ax, 2, 16.45, 2, 16.1, 'Ya')
draw_action(ax, 2, 15.8, 'HTTP Server\naktif di /capture', '#27AE60')

# Retry WiFi
ax.annotate('', xy=(0.5, 16.8), xytext=(0.8, 16.8),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.2))
ax.text(0.3, 17.1, 'Retry\n(max 40x)', fontsize=6, color='#E74C3C', ha='center')
ax.plot([0.5, 0.5], [16.8, 17.9], '-', color='#E74C3C', linewidth=1)
ax.annotate('', xy=(0.8, 17.9), xytext=(0.5, 17.9),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.2))

# Laravel startup
draw_action(ax, 10, 18.9, 'php artisan\nserve', '#E67E22')
arrow(ax, 10, 18.6, 10, 18.2)
draw_action(ax, 10, 17.9, 'API Ready\nport 8000', '#E67E22')

# Frontend startup
draw_action(ax, 14, 18.9, 'npm run dev', '#3498DB')
arrow(ax, 14, 18.6, 14, 18.2)
draw_action(ax, 14, 17.9, 'Web Ready\nport 3000', '#3498DB')

# === Phase 2: Scanning Loop ===
ax.text(8, 15.2, '── FASE 2: SCANNING LOOP ──', ha='center', va='center',
        fontsize=9, fontweight='bold', color='#2C3E50')

# Python scanner start
draw_action(ax, 6, 14.7, 'python3\nqr_scanner_service.py', '#8E44AD')
arrow(ax, 6, 14.4, 6, 14.0)
draw_action(ax, 6, 13.7, 'Poll setiap 2 detik', '#8E44AD')

# Request to ESP32
arrow(ax, 4.4, 13.7, 3.6, 13.7, 'GET /capture')
draw_action(ax, 2, 13.7, 'Kirim JPEG\n(~7KB)', '#27AE60')
arrow(ax, 3.6, 13.4, 4.4, 13.0, 'Response JPEG')

# Decode
draw_action(ax, 6, 12.7, 'OpenCV decode\nQR Code', '#8E44AD')
arrow(ax, 6, 12.4, 6, 12.0)
draw_decision(ax, 6, 11.6, 'QR valid?')

# Not valid - loop
ax.annotate('', xy=(4.5, 11.6), xytext=(4.8, 11.6),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.2))
ax.text(4.2, 11.8, 'Tidak', fontsize=6.5, color='#E74C3C')
ax.plot([4.5, 4.5], [11.6, 13.7], '-', color='#E74C3C', linewidth=1)
ax.annotate('', xy=(4.8, 13.7), xytext=(4.5, 13.7),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.2))

# Valid - send to backend
arrow(ax, 6, 11.25, 6, 10.9, 'Ya')
draw_action(ax, 6, 10.6, 'Parse:\nkode_jumlah_tipe', '#8E44AD')
arrow(ax, 7.6, 10.6, 8.4, 10.6, 'POST API')

# Backend process
draw_action(ax, 10, 10.6, 'Validasi data', '#E67E22')
arrow(ax, 10, 10.3, 10, 9.9)
draw_decision(ax, 10, 9.5, 'Tipe?')

# Masuk
arrow(ax, 10, 9.15, 10, 8.7, 'Masuk')
draw_action(ax, 10, 8.4, 'Tambah stok\nbarang', '#27AE60', 2.8)

# Keluar
ax.annotate('', xy=(12, 9.5), xytext=(11.2, 9.5),
            arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.2))
ax.text(11.5, 9.7, 'Keluar', fontsize=6.5, color='#666', fontstyle='italic')
draw_action(ax, 13, 9.5, 'Kurangi\nstok', '#E74C3C', 2)
arrow(ax, 13, 9.2, 10, 8.7)

# Save history
arrow(ax, 10, 8.1, 10, 7.7)
draw_action(ax, 10, 7.4, 'Simpan ke\nstock_histories', '#E67E22')
arrow(ax, 10, 7.1, 10, 6.7)
draw_action(ax, 10, 6.4, 'Response\nJSON sukses', '#E67E22')

# Response back to scanner
arrow(ax, 8.4, 6.4, 7.6, 6.4, 'HTTP 200')
draw_action(ax, 6, 6.4, 'Log: [OK]\nCooldown 3s', '#8E44AD')

# Frontend shows data
arrow(ax, 11.6, 7.4, 12.4, 7.4, 'Data updated')
draw_action(ax, 14, 7.4, 'User buka\ndashboard', '#3498DB')
arrow(ax, 14, 7.1, 14, 6.7)
draw_action(ax, 14, 6.4, 'GET API\n/items, /histories', '#3498DB')
arrow(ax, 12.4, 6.4, 11.6, 6.4)
arrow(ax, 14, 6.1, 14, 5.7)
draw_action(ax, 14, 5.4, 'Tampilkan data\ndi dashboard', '#3498DB')

# === Phase 3: Auto restart ===
ax.text(8, 4.5, '── FASE 3: AUTO MAINTENANCE ──', ha='center', va='center',
        fontsize=9, fontweight='bold', color='#2C3E50')

draw_action(ax, 2, 3.8, 'Auto restart\nsetiap 30 menit', '#27AE60')
arrow(ax, 2, 3.5, 2, 3.1)
draw_action(ax, 2, 2.8, 'ESP.restart()\nMemory fresh', '#16A085')

# Loop back indicator
arrow(ax, 6, 6.1, 6, 5.7)
ax.text(6, 5.5, '↺ Loop scan berikutnya', ha='center', fontsize=7, color='#8E44AD', fontweight='bold')

# Legend
ax.text(5, 1.8, 'Waktu proses:', fontsize=8, fontweight='bold')
ax.text(5, 1.4, '• Capture + transfer WiFi: ~7-10 detik', fontsize=7, color='#555')
ax.text(5, 1.0, '• Decode QR + kirim API: < 1 detik', fontsize=7, color='#555')
ax.text(5, 0.6, '• Total scan → muncul di web: ~10-12 detik', fontsize=7, color='#555')

plt.tight_layout()
plt.savefig('/Users/apple/stock-management-iot/activity_diagram_keseluruhan.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Done: activity_diagram_keseluruhan.png")
