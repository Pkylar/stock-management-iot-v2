import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { stockHistories } from '../lib/api';

export default function History() {
  const [histories, setHistories] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchHistories();
  }, [filter]);

  const fetchHistories = async () => {
    try {
      let response;
      switch (filter) {
        case 'masuk':
          response = await stockHistories.getMasuk();
          break;
        case 'keluar':
          response = await stockHistories.getKeluar();
          break;
        default:
          response = await stockHistories.getAll();
      }
      setHistories(response.data);
    } catch (error) {
      console.error('Error fetching histories:', error);
    }
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-blue-600 rounded-2xl p-6 text-white relative overflow-hidden">
          <div className="absolute bottom-0 right-0 w-36 h-36 bg-white/5 rounded-full translate-y-12 translate-x-12"></div>
          <div className="absolute top-0 right-24 w-20 h-20 bg-white/5 rounded-full -translate-y-6"></div>
          <div className="relative z-10">
            <h1 className="text-2xl font-bold">Riwayat Stok 📊</h1>
            <p className="text-indigo-100 mt-1">Catatan semua pergerakan stok masuk dan keluar gudang</p>
            <div className="flex items-center space-x-4 mt-4">
              <div className="bg-white/15 backdrop-blur-sm px-4 py-2 rounded-lg">
                <p className="text-xs text-indigo-200">Total Aktivitas</p>
                <p className="text-xl font-bold">{histories.length}</p>
              </div>
              <div className="bg-white/15 backdrop-blur-sm px-4 py-2 rounded-lg">
                <p className="text-xs text-indigo-200">Masuk</p>
                <p className="text-xl font-bold text-green-300">{histories.filter((h: any) => h.tipe === 'masuk').length}</p>
              </div>
              <div className="bg-white/15 backdrop-blur-sm px-4 py-2 rounded-lg">
                <p className="text-xs text-indigo-200">Keluar</p>
                <p className="text-xl font-bold text-red-300">{histories.filter((h: any) => h.tipe === 'keluar').length}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filter Tabs */}
        <div className="flex items-center space-x-2 bg-white rounded-xl border border-gray-100 shadow-sm p-2">
          <button
            onClick={() => setFilter('all')}
            className={`flex items-center space-x-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-all ${
              filter === 'all'
                ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <span>📋</span>
            <span>Semua</span>
          </button>
          <button
            onClick={() => setFilter('masuk')}
            className={`flex items-center space-x-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-all ${
              filter === 'masuk'
                ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-md'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <span>↓</span>
            <span>Stok Masuk</span>
          </button>
          <button
            onClick={() => setFilter('keluar')}
            className={`flex items-center space-x-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-all ${
              filter === 'keluar'
                ? 'bg-gradient-to-r from-red-500 to-rose-600 text-white shadow-md'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <span>↑</span>
            <span>Stok Keluar</span>
          </button>
        </div>

        {/* History List */}
        {histories.length === 0 ? (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-12 text-center">
            <div className="w-20 h-20 bg-indigo-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">📋</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-700 mb-1">Belum ada riwayat</h3>
            <p className="text-sm text-gray-400">Riwayat akan muncul saat ada pergerakan stok</p>
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
            <table className="min-w-full">
              <thead>
                <tr className="bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-100">
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Barang</th>
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Tipe</th>
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Jumlah</th>
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Keterangan</th>
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Sumber</th>
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Dibuat oleh</th>
                  <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Waktu</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {histories.map((history: any) => (
                  <tr key={history.id} className={`hover:bg-opacity-50 transition-colors ${
                    history.tipe === 'masuk' ? 'hover:bg-green-50' : 'hover:bg-red-50'
                  }`}>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-3">
                        <div className={`w-9 h-9 rounded-lg flex items-center justify-center text-sm font-bold ${
                          history.tipe === 'masuk' 
                            ? 'bg-gradient-to-br from-green-100 to-emerald-100 text-green-600' 
                            : 'bg-gradient-to-br from-red-100 to-rose-100 text-red-600'
                        }`}>
                          {history.tipe === 'masuk' ? '↓' : '↑'}
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-gray-800">{history.item?.nama_barang}</p>
                          <p className="text-xs text-gray-400">ID: {history.barang_id}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold ${
                        history.tipe === 'masuk'
                          ? 'bg-green-100 text-green-700 border border-green-200'
                          : 'bg-red-100 text-red-700 border border-red-200'
                      }`}>
                        {history.tipe === 'masuk' ? '📥 Masuk' : '📤 Keluar'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`text-base font-bold ${
                        history.tipe === 'masuk' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {history.tipe === 'masuk' ? '+' : '-'}{history.jumlah}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-600 bg-gray-50 px-2.5 py-1 rounded-md">{history.keterangan || '-'}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                        history.sumber === 'esp32_cam'
                          ? 'bg-indigo-50 text-indigo-700 border border-indigo-200'
                          : 'bg-gray-50 text-gray-600 border border-gray-200'
                      }`}>
                        {history.sumber === 'esp32_cam' ? '📷 ESP32' : '✋ Manual'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div>
                        <span className="text-sm text-gray-700">{history.creator?.name || 'System'}</span>
                        <p className="text-xs text-gray-400 capitalize">
                          {history.creator?.role === 'kepala_gudang' ? 'Kepala Gudang' : 'Staff'}
                        </p>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-sm font-medium text-gray-700">
                          {new Date(history.created_at).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })}
                        </p>
                        <p className="text-xs text-gray-400">
                          {new Date(history.created_at).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })}
                        </p>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  );
}
