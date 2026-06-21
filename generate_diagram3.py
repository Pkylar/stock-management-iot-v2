import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(1, 1, figsize=(12, 18))
ax.set_xlim(0, 12)
ax.set_ylim(0, 18)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# Title
ax.text(6, 17.5, 'Activity Diagram - Alur Sistem Manajemen Stok IoT', 
        ha='center', va='center', fontsize=13, fontweight='bold')
ax.text(6, 17.1, 'Dari scan QR Code sampai data tampil di web', 
        ha='center', va='center', fontsize=9, color='#666')

def draw_start(ax, x, y):
    circle = plt.Circle((x, y), 0.25, color='black', fill=True)
    ax.add_patch(circle)

def draw_end(ax, x, y):
    circle1 = plt.Circle((x, y), 0.3, color='black', fill=False, linewidth=2.5)
    circle2 = plt.Circle((x, y), 0.18, color='black', fill=True)
    ax.add_patch(circle1)
    ax.add_patch(circle2)

def draw_action(ax, x, y, text, color='#3498DB', subtext=''):
    box = FancyBboxPatch((x-2.8, y-0.35), 5.6, 0.7, boxstyle="round,pad=0.12",
                          facecolor=color, edgecolor='#2C3E50', linewidth=1.8, alpha=0.92)
    ax.add_patch(box)
    ax.text(x, y+0.05, text, ha='center', va='center', fontsize=9, color='white', fontweight='bold')
    if subtext:
        ax.text(x, y-0.18, subtext, ha='center', va='center', fontsize=7, color='#ffffffcc')

def draw_decision(ax, x, y, text):
    diamond = plt.Polygon([[x, y+0.45], [x+1.8, y], [x, y-0.45], [x-1.8, y]],
                           facecolor='#F39C12', edgecolor='#2C3E50', linewidth=1.8)
    ax.add_patch(diamond)
    ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')

def arrow(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=2))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        offset = 0.15 if x1 == x2 else 0.2
        ax.text(mx+0.3, my, label, fontsize=7.5, color='#555', fontstyle='italic')

# Step numbers
def step_num(ax, x, y, num):
    circle = plt.Circle((x, y), 0.22, color='#2C3E50', fill=True)
    ax.add_patch(circle)
    ax.text(x, y, str(num), ha='center', va='center', fontsize=8, color='white', fontweight='bold')

# === DIAGRAM ===

# Start
draw_start(ax, 6, 16.5)
arrow(ax, 6, 16.25, 6, 15.9)

# Step 1
step_num(ax, 3, 15.55, 1)
draw_action(ax, 6, 15.55, 'User tempelkan QR Code ke kamera', '#2ECC71', 'Format: kode_barang_jumlah_tipe')

arrow(ax, 6, 15.2, 6, 14.7)

# Step 2
step_num(ax, 3, 14.35, 2)
draw_action(ax, 6, 14.35, 'ESP32-S3 ambil foto (JPEG)', '#27AE60', 'Resolusi 320x240, ~7KB')

arrow(ax, 6, 14.0, 6, 13.5)

# Step 3
step_num(ax, 3, 13.15, 3)
draw_action(ax, 6, 13.15, 'Gambar dikirim via WiFi ke komputer', '#8E44AD', 'HTTP GET /capture (~7-10 detik)')

arrow(ax, 6, 12.8, 6, 12.3)

# Step 4
step_num(ax, 3, 11.95, 4)
draw_action(ax, 6, 11.95, 'Python + OpenCV decode QR Code', '#9B59B6', 'Baca isi QR dari gambar')

arrow(ax, 6, 11.6, 6, 11.1)

# Decision: QR valid?
draw_decision(ax, 6, 10.65, 'QR terbaca?')

# No - loop back
ax.annotate('', xy=(9.5, 10.65), xytext=(7.8, 10.65),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.5))
ax.text(8.5, 10.85, 'Tidak', fontsize=7.5, color='#E74C3C')
box_retry = FancyBboxPatch((9.2, 10.35), 2.2, 0.6, boxstyle="round,pad=0.08",
                            facecolor='#E74C3C', edgecolor='#2C3E50', linewidth=1.2, alpha=0.85)
ax.add_patch(box_retry)
ax.text(10.3, 10.65, 'Ulangi\nscan', ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')
# Arrow back up
ax.plot([10.3, 10.3], [10.95, 13.15], '-', color='#E74C3C', linewidth=1.2)
ax.annotate('', xy=(8.8, 13.15), xytext=(10.3, 13.15),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.2))

# Yes - continue
arrow(ax, 6, 10.2, 6, 9.7, 'Ya')

# Step 5
step_num(ax, 3, 9.35, 5)
draw_action(ax, 6, 9.35, 'Parse data: kode, jumlah, tipe', '#2980B9', 'Contoh: BRG001_5_masuk')

arrow(ax, 6, 9.0, 6, 8.5)

# Step 6
step_num(ax, 3, 8.15, 6)
draw_action(ax, 6, 8.15, 'Kirim ke Laravel Backend (API)', '#E67E22', 'POST /api/scan-barcode')

arrow(ax, 6, 7.8, 6, 7.3)

# Decision: Tipe
draw_decision(ax, 6, 6.85, 'Tipe?')

# Masuk
ax.annotate('', xy=(3.5, 6.2), xytext=(4.2, 6.85),
            arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))
ax.text(3.2, 6.6, 'Masuk', fontsize=7.5, color='#555', fontstyle='italic')
box_masuk = FancyBboxPatch((1.8, 5.9), 3.4, 0.6, boxstyle="round,pad=0.08",
                            facecolor='#27AE60', edgecolor='#2C3E50', linewidth=1.5, alpha=0.9)
ax.add_patch(box_masuk)
ax.text(3.5, 6.2, 'Tambah stok\nbarang', ha='center', va='center', fontsize=8, color='white', fontweight='bold')

# Keluar
ax.annotate('', xy=(8.5, 6.2), xytext=(7.8, 6.85),
            arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))
ax.text(8.3, 6.6, 'Keluar', fontsize=7.5, color='#555', fontstyle='italic')
box_keluar = FancyBboxPatch((6.8, 5.9), 3.4, 0.6, boxstyle="round,pad=0.08",
                             facecolor='#E74C3C', edgecolor='#2C3E50', linewidth=1.5, alpha=0.9)
ax.add_patch(box_keluar)
ax.text(8.5, 6.2, 'Kurangi stok\nbarang', ha='center', va='center', fontsize=8, color='white', fontweight='bold')

# Merge
arrow(ax, 3.5, 5.9, 6, 5.3)
arrow(ax, 8.5, 5.9, 6, 5.3)

# Step 7
step_num(ax, 3, 5.0, 7)
draw_action(ax, 6, 5.0, 'Simpan riwayat di database', '#E67E22', 'Tabel: stock_histories')

arrow(ax, 6, 4.65, 6, 4.15)

# Step 8
step_num(ax, 3, 3.8, 8)
draw_action(ax, 6, 3.8, 'Data muncul di Web Dashboard', '#3498DB', 'Realtime update di browser')

arrow(ax, 6, 3.45, 6, 3.0)

# Step 9
step_num(ax, 3, 2.65, 9)
draw_action(ax, 6, 2.65, 'Cooldown 3 detik → siap scan lagi', '#95A5A6', 'Mencegah duplikasi scan')

arrow(ax, 6, 2.3, 6, 1.9)

# End
draw_end(ax, 6, 1.6)

# Time annotation
ax.text(11, 15.55, '~0s', fontsize=7, color='#888')
ax.text(11, 14.35, '~1s', fontsize=7, color='#888')
ax.text(11, 13.15, '~7-10s', fontsize=7, color='#E74C3C', fontweight='bold')
ax.text(11, 11.95, '<0.1s', fontsize=7, color='#888')
ax.text(11, 8.15, '<0.1s', fontsize=7, color='#888')
ax.text(11, 3.8, 'TOTAL: ~10-12s', fontsize=7.5, color='#E74C3C', fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/apple/stock-management-iot/activity_diagram_alur_sistem.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Done: activity_diagram_alur_sistem.png")
