import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { items } from '../lib/api';

export default function Items() {
  const [itemsData, setItemsData] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [showKeluarModal, setShowKeluarModal] = useState(false);
  const [keluarItem, setKeluarItem] = useState<any>(null);
  const [keluarJumlah, setKeluarJumlah] = useState(1);
  const [keluarKeterangan, setKeluarKeterangan] = useState('');
  const [keluarAlamat, setKeluarAlamat] = useState('');
  const [editingItem, setEditingItem] = useState<any>(null);
  const [formData, setFormData] = useState({
    nama_barang: '',
    kode_barang: '',
    jumlah_stok: 0
  });

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const response = await items.getAll();
      setItemsData(response.data);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await items.update(editingItem.id, formData);
      } else {
        await items.create(formData);
      }
      setShowForm(false);
      setEditingItem(null);
      setFormData({ nama_barang: '', kode_barang: '', jumlah_stok: 0 });
      fetchItems();
    } catch (error) {
      console.error('Error saving item:', error);
    }
  };

  const handleEdit = (item: any) => {
    setEditingItem(item);
    setFormData(item);
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm('Yakin ingin menghapus item ini?')) {
      try {
        await items.delete(id);
        fetchItems();
      } catch (error) {
        console.error('Error deleting item:', error);
      }
    }
  };

  const handleKeluar = (item: any) => {
    setKeluarItem(item);
    setKeluarJumlah(1);
    setKeluarKeterangan('');
    setKeluarAlamat('');
    setShowKeluarModal(true);
  };

  const submitKeluar = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await items.stokKeluar(keluarItem.id, keluarJumlah, keluarKeterangan + (keluarAlamat ? ' | Alamat: ' + keluarAlamat : ''));
      setShowKeluarModal(false);
      setKeluarItem(null);
      fetchItems();
    } catch (error: any) {
      alert(error.response?.data?.message || 'Gagal mengeluarkan stok');
    }
  };

  const totalStok = itemsData.reduce((sum: number, i: any) => sum + i.jumlah_stok, 0);

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full -translate-y-8 translate-x-8"></div>
          <div className="relative z-10 flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold">Stok Barang 📦</h1>
              <p className="text-blue-100 mt-1">Kelola semua barang di gudang Anda</p>
            </div>
            <button
              onClick={() => setShowForm(true)}
              className="flex items-center space-x-2 bg-white text-blue-700 px-5 py-2.5 rounded-lg hover:bg-blue-50 transition-colors font-semibold shadow-sm"
            >
              <span className="text-lg">+</span>
              <span>Tambah Barang</span>
            </button>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 flex items-center space-x-3">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <span>📋</span>
            </div>
            <div>
              <p className="text-lg font-bold text-gray-800">{itemsData.length}</p>
              <p className="text-xs text-gray-500">Total Barang</p>
            </div>
          </div>
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 flex items-center space-x-3">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <span>✅</span>
            </div>
            <div>
              <p className="text-lg font-bold text-gray-800">{totalStok}</p>
              <p className="text-xs text-gray-500">Total Unit</p>
            </div>
          </div>
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 flex items-center space-x-3">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
              <span>⚠️</span>
            </div>
            <div>
              <p className="text-lg font-bold text-red-600">{itemsData.filter((i: any) => i.jumlah_stok < 5).length}</p>
              <p className="text-xs text-gray-500">Stok Rendah</p>
            </div>
          </div>
        </div>

        {/* Form Modal */}
        {showForm && (
          <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl shadow-xl w-full max-w-md border border-gray-100 overflow-hidden">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 flex items-center justify-between">
                <h2 className="text-lg font-bold text-white">
                  {editingItem ? '✏️ Edit Barang' : '📦 Tambah Barang Baru'}
                </h2>
                <button
                  onClick={() => {
                    setShowForm(false);
                    setEditingItem(null);
                    setFormData({ nama_barang: '', kode_barang: '', jumlah_stok: 0 });
                  }}
                  className="text-white/70 hover:text-white text-xl"
                >
                  ×
                </button>
              </div>
              <form onSubmit={handleSubmit} className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1.5">Nama Barang</label>
                  <input
                    type="text"
                    required
                    className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50"
                    placeholder="Contoh: Laptop Dell"
                    value={formData.nama_barang}
                    onChange={(e) => setFormData({...formData, nama_barang: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1.5">Kode Barang</label>
                  <input
                    type="text"
                    required
                    className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50"
                    placeholder="Contoh: BRG001"
                    value={formData.kode_barang}
                    onChange={(e) => setFormData({...formData, kode_barang: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1.5">Jumlah Stok</label>
                  <input
                    type="number"
                    required
                    min="0"
                    className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50"
                    value={formData.jumlah_stok}
                    onChange={(e) => setFormData({...formData, jumlah_stok: parseInt(e.target.value)})}
                  />
                </div>
                <div className="flex space-x-3 pt-2">
                  <button
                    type="submit"
                    className="flex-1 bg-blue-600 text-white py-2.5 rounded-lg hover:bg-blue-700 transition-colors font-medium shadow-sm"
                  >
                    {editingItem ? 'Update' : 'Simpan'}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowForm(false);
                      setEditingItem(null);
                      setFormData({ nama_barang: '', kode_barang: '', jumlah_stok: 0 });
                    }}
                    className="flex-1 bg-gray-100 text-gray-700 py-2.5 rounded-lg hover:bg-gray-200 transition-colors font-medium"
                  >
                    Batal
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Items Table */}
        {itemsData.length === 0 ? (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-12 text-center">
            <div className="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">📦</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-700 mb-1">Belum ada barang</h3>
            <p className="text-sm text-gray-400 mb-4">Tambah barang pertama atau scan QR Code via ESP32</p>
            <button
              onClick={() => setShowForm(true)}
              className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
            >
              + Tambah Barang Pertama
            </button>
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
            <table className="min-w-full">
              <thead>
                <tr className="bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-100">
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Barang</th>
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Kode Barang</th>
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Stok</th>
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Dibuat oleh</th>
                  <th className="px-6 py-3.5 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">Aksi</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {itemsData.map((item: any) => (
                  <tr key={item.id} className="hover:bg-blue-50/30 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-3">
                        <div className="w-9 h-9 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-lg flex items-center justify-center">
                          <span className="text-sm">📦</span>
                        </div>
                        <div>
                          <span className="text-sm font-semibold text-gray-800">{item.nama_barang}</span>
                          <p className="text-xs text-gray-400">ID: {item.id}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <code className="text-sm text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded-md font-medium">{item.kode_barang}</code>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <div className={`w-2 h-2 rounded-full ${item.jumlah_stok < 5 ? 'bg-red-400' : 'bg-green-400'}`}></div>
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold ${
                          item.jumlah_stok < 5
                            ? 'bg-red-50 text-red-700 border border-red-200'
                            : 'bg-green-50 text-green-700 border border-green-200'
                        }`}>
                          {item.jumlah_stok} unit
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold ${
                        item.status_terakhir === 'masuk'
                          ? 'bg-green-50 text-green-700 border border-green-200'
                          : item.status_terakhir === 'keluar'
                            ? 'bg-red-50 text-red-700 border border-red-200'
                            : 'bg-gray-50 text-gray-500 border border-gray-200'
                      }`}>
                        {item.status_terakhir === 'masuk' ? '📥 Di Gudang' : item.status_terakhir === 'keluar' ? '📤 Keluar' : '⏳ Belum scan'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div>
                        <span className="text-sm text-gray-700">{item.creator?.name || 'System'}</span>
                        <p className="text-xs text-gray-400">
                          {item.created_at ? new Date(item.created_at).toLocaleDateString('id-ID') : '-'}
                        </p>
                        {item.updated_by && (
                          <p className="text-xs text-orange-600 mt-0.5">
                            Diupdate oleh: {item.updater?.name}
                          </p>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end space-x-1">
                        <button
                          onClick={() => handleKeluar(item)}
                          className="text-sm text-orange-600 hover:text-orange-800 font-medium px-3 py-1.5 rounded-lg hover:bg-orange-50 transition-colors"
                        >
                          📤 Keluar
                        </button>
                        <button
                          onClick={() => handleEdit(item)}
                          className="text-sm text-blue-600 hover:text-blue-800 font-medium px-3 py-1.5 rounded-lg hover:bg-blue-50 transition-colors"
                        >
                          ✏️ Edit
                        </button>
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="text-sm text-red-600 hover:text-red-800 font-medium px-3 py-1.5 rounded-lg hover:bg-red-50 transition-colors"
                        >
                          🗑️ Hapus
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Modal Stok Keluar */}
        {showKeluarModal && keluarItem && (
          <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm border border-gray-100 overflow-hidden">
              <div className="bg-gradient-to-r from-orange-500 to-red-500 px-6 py-4 flex items-center justify-between">
                <h2 className="text-lg font-bold text-white">📤 Stok Keluar</h2>
                <button onClick={() => setShowKeluarModal(false)} className="text-white/70 hover:text-white text-xl">×</button>
              </div>
              <form onSubmit={submitKeluar} className="p-6 space-y-4">
                <div className="bg-gray-50 p-3 rounded-lg">
                  <p className="text-sm font-medium text-gray-800">{keluarItem.nama_barang}</p>
                  <p className="text-xs text-gray-500">Stok saat ini: {keluarItem.jumlah_stok} unit</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1.5">Jumlah Keluar</label>
                  <input
                    type="number"
                    required
                    min="1"
                    max={keluarItem.jumlah_stok}
                    className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-gray-900 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-gray-50"
                    value={keluarJumlah}
                    onChange={(e) => setKeluarJumlah(parseInt(e.target.value))}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1.5">Alamat Pengiriman</label>
                  <input
                    type="text"
                    required
                    className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-gray-900 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-gray-50"
                    placeholder="Contoh: Jl. Merdeka No. 10, Jakarta"
                    value={keluarAlamat}
                    onChange={(e) => setKeluarAlamat(e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1.5">Keterangan (opsional)</label>
                  <input
                    type="text"
                    className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-gray-900 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-gray-50"
                    placeholder="Contoh: Dikirim ke cabang A"
                    value={keluarKeterangan}
                    onChange={(e) => setKeluarKeterangan(e.target.value)}
                  />
                </div>
                <div className="flex space-x-3 pt-2">
                  <button type="submit" className="flex-1 bg-orange-500 text-white py-2.5 rounded-lg hover:bg-orange-600 transition-colors font-medium">
                    Keluarkan Stok
                  </button>
                  <button type="button" onClick={() => setShowKeluarModal(false)} className="flex-1 bg-gray-100 text-gray-700 py-2.5 rounded-lg hover:bg-gray-200 transition-colors font-medium">
                    Batal
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
