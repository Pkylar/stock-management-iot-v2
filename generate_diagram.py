import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(1, 1, figsize=(14, 20))
ax.set_xlim(0, 14)
ax.set_ylim(0, 20)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# Title
ax.text(7, 19.5, 'Activity Diagram - Scan QR Code (Stok Masuk/Keluar)', 
        ha='center', va='center', fontsize=14, fontweight='bold')

# Helper functions
def draw_start(ax, x, y):
    circle = plt.Circle((x, y), 0.25, color='black', fill=True)
    ax.add_patch(circle)

def draw_end(ax, x, y):
    circle1 = plt.Circle((x, y), 0.3, color='black', fill=False, linewidth=2)
    circle2 = plt.Circle((x, y), 0.2, color='black', fill=True)
    ax.add_patch(circle1)
    ax.add_patch(circle2)

def draw_action(ax, x, y, text, color='#4A90D9'):
    box = FancyBboxPatch((x-2.5, y-0.3), 5, 0.6, boxstyle="round,pad=0.1", 
                          facecolor=color, edgecolor='#2C3E50', linewidth=1.5, alpha=0.9)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=8, color='white', fontweight='bold')

def draw_decision(ax, x, y, text):
    diamond = plt.Polygon([[x, y+0.4], [x+1.5, y], [x, y-0.4], [x-1.5, y]], 
                           facecolor='#F5A623', edgecolor='#2C3E50', linewidth=1.5)
    ax.add_patch(diamond)
    ax.text(x, y, text, ha='center', va='center', fontsize=7, fontweight='bold')

def draw_arrow(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.2, my, label, fontsize=7, color='#666666', fontstyle='italic')

# Draw diagram
draw_start(ax, 7, 19)

draw_arrow(ax, 7, 18.75, 7, 18.4)
draw_action(ax, 7, 18.1, 'User tempelkan QR Code ke kamera ESP32', '#3498DB')

draw_arrow(ax, 7, 17.8, 7, 17.4)
draw_action(ax, 7, 17.1, 'ESP32 capture gambar JPEG', '#27AE60')

draw_arrow(ax, 7, 16.8, 7, 16.4)
draw_action(ax, 7, 16.1, 'Python Scanner ambil gambar via HTTP', '#8E44AD')

draw_arrow(ax, 7, 15.8, 7, 15.4)
draw_decision(ax, 7, 15.0, 'QR terdeteksi?')

# No branch - loop back
draw_arrow(ax, 5.5, 15.0, 4, 15.0, 'Tidak')
ax.annotate('', xy=(4, 16.1), xytext=(4, 15.0),
            arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))
ax.annotate('', xy=(4.5, 16.1), xytext=(4, 16.1),
            arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))
ax.text(3.5, 15.5, 'Tunggu 2s', fontsize=7, color='#E74C3C', fontstyle='italic')

# Yes branch
draw_arrow(ax, 7, 14.6, 7, 14.2, 'Ya')
draw_action(ax, 7, 13.9, 'Parse QR: kode_barang_jumlah_tipe', '#2980B9')

draw_arrow(ax, 7, 13.6, 7, 13.2)
draw_decision(ax, 7, 12.8, 'Format valid?')

# Invalid format
ax.annotate('', xy=(10.5, 12.8), xytext=(8.5, 12.8),
            arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))
ax.text(9.2, 13.0, 'Tidak', fontsize=7, color='#666666', fontstyle='italic')
ax.text(10.7, 12.8, 'Log warning', fontsize=7, color='#E74C3C', ha='left')

# Valid - continue
draw_arrow(ax, 7, 12.4, 7, 12.0, 'Ya')
draw_action(ax, 7, 11.7, 'Kirim data ke Laravel Backend (POST API)', '#E67E22')

draw_arrow(ax, 7, 11.4, 7, 11.0)
draw_decision(ax, 7, 10.6, 'Tipe?')

# Masuk branch
draw_arrow(ax, 5.5, 10.6, 4, 10.6, 'Masuk')
ax.annotate('', xy=(4, 10.0), xytext=(4, 10.6),
            arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))

draw_decision(ax, 4, 9.5, 'Barang ada?')

# Barang ada - tambah stok
ax.annotate('', xy=(2.5, 9.5), xytext=(2.5, 9.5),
            arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))
draw_arrow(ax, 4, 9.1, 4, 8.6, 'Ya')
box1 = FancyBboxPatch((2.5, 8.2), 3, 0.5, boxstyle="round,pad=0.1",
                       facecolor='#27AE60', edgecolor='#2C3E50', linewidth=1.5, alpha=0.9)
ax.add_patch(box1)
ax.text(4, 8.45, 'Tambah stok', ha='center', va='center', fontsize=8, color='white', fontweight='bold')

# Barang tidak ada - buat baru
ax.annotate('', xy=(2, 9.5), xytext=(2.5, 9.5),
            arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))
ax.text(1.5, 9.7, 'Tidak', fontsize=7, color='#666666', fontstyle='italic')
box_new = FancyBboxPatch((0.3, 8.9), 2.2, 0.5, boxstyle="round,pad=0.1",
                          facecolor='#16A085', edgecolor='#2C3E50', linewidth=1.5, alpha=0.9)
ax.add_patch(box_new)
ax.text(1.4, 9.15, 'Buat barang\nbaru', ha='center', va='center', fontsize=7, color='white', fontweight='bold')

# Keluar branch
draw_arrow(ax, 8.5, 10.6, 10, 10.6, 'Keluar')
ax.annotate('', xy=(10, 10.0), xytext=(10, 10.6),
            arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))

draw_decision(ax, 10, 9.5, 'Stok cukup?')

draw_arrow(ax, 10, 9.1, 10, 8.6, 'Ya')
box2 = FancyBboxPatch((8.5, 8.2), 3, 0.5, boxstyle="round,pad=0.1",
                       facecolor='#E74C3C', edgecolor='#2C3E50', linewidth=1.5, alpha=0.9)
ax.add_patch(box2)
ax.text(10, 8.45, 'Kurangi stok', ha='center', va='center', fontsize=8, color='white', fontweight='bold')

# Stok tidak cukup
ax.annotate('', xy=(12, 9.5), xytext=(11.5, 9.5),
            arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))
ax.text(11.6, 9.7, 'Tidak', fontsize=7, color='#666666', fontstyle='italic')
box_err = FancyBboxPatch((11.8, 9.2), 2, 0.5, boxstyle="round,pad=0.1",
                          facecolor='#C0392B', edgecolor='#2C3E50', linewidth=1.5, alpha=0.9)
ax.add_patch(box_err)
ax.text(12.8, 9.45, 'Tolak: error', ha='center', va='center', fontsize=7, color='white', fontweight='bold')

# Merge ke simpan riwayat
draw_arrow(ax, 4, 8.2, 7, 7.5)
draw_arrow(ax, 10, 8.2, 7, 7.5)

draw_action(ax, 7, 7.2, 'Simpan riwayat ke stock_histories', '#2C3E50')

draw_arrow(ax, 7, 6.9, 7, 6.5)
draw_action(ax, 7, 6.2, 'Response sukses → Data muncul di Web', '#27AE60')

draw_arrow(ax, 7, 5.9, 7, 5.5)
draw_action(ax, 7, 5.2, 'Cooldown 3 detik', '#95A5A6')

draw_arrow(ax, 7, 4.9, 7, 4.5)
draw_end(ax, 7, 4.2)

# Legend
ax.text(0.5, 3.5, 'Keterangan:', fontsize=9, fontweight='bold')
box_l1 = FancyBboxPatch((0.5, 2.9), 1.5, 0.4, boxstyle="round,pad=0.05",
                         facecolor='#3498DB', edgecolor='#2C3E50', linewidth=1, alpha=0.9)
ax.add_patch(box_l1)
ax.text(2.2, 3.1, '= Aksi/Proses', fontsize=8, va='center')

diamond_l = plt.Polygon([[5, 3.3], [5.5, 3.1], [5, 2.9], [4.5, 3.1]],
                         facecolor='#F5A623', edgecolor='#2C3E50', linewidth=1)
ax.add_patch(diamond_l)
ax.text(5.7, 3.1, '= Keputusan/Kondisi', fontsize=8, va='center')

circle_l = plt.Circle((9, 3.1), 0.15, color='black', fill=True)
ax.add_patch(circle_l)
ax.text(9.3, 3.1, '= Start/End', fontsize=8, va='center')

plt.tight_layout()
plt.savefig('/Users/apple/stock-management-iot/activity_diagram_scan_qr.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Done: activity_diagram_scan_qr.png")
