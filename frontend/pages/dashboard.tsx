import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { items, stockHistories } from '../lib/api';

export default function Dashboard() {
  const [itemsData, setItemsData] = useState([]);
  const [recentHistory, setRecentHistory] = useState([]);
  const [stats, setStats] = useState({
    totalItems: 0,
    totalStock: 0,
    lowStock: 0,
    totalMasuk: 0,
    totalKeluar: 0
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [itemsRes, historyRes] = await Promise.all([
        items.getAll(),
        stockHistories.getAll()
      ]);

      const itemsData = itemsRes.data;
      const historyData = historyRes.data;
      setItemsData(itemsData);
      setRecentHistory(historyData.slice(0, 6));

      const totalStock = itemsData.reduce((sum: number, item: any) => sum + item.jumlah_stok, 0);
      const lowStock = itemsData.filter((item: any) => item.jumlah_stok < 5).length;
      const totalMasuk = historyData.filter((h: any) => h.tipe === 'masuk').length;
      const totalKeluar = historyData.filter((h: any) => h.tipe === 'keluar').length;

      setStats({ totalItems: itemsData.length, totalStock, lowStock, totalMasuk, totalKeluar });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Welcome Banner */}
        <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 rounded-2xl p-6 text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 w-40 h-40 bg-white/5 rounded-full -translate-y-10 translate-x-10"></div>
          <div className="absolute bottom-0 right-20 w-24 h-24 bg-white/5 rounded-full translate-y-8"></div>
          <div className="relative z-10">
            <h1 className="text-2xl font-bold">Selamat Datang! 👋</h1>
            <p className="text-blue-100 mt-1">Pantau stok gudang Anda secara realtime melalui dashboard ini.</p>
            <div className="flex items-center space-x-4 mt-4">
              <div className="bg-white/15 backdrop-blur-sm px-4 py-2 rounded-lg">
                <p className="text-xs text-blue-200">Total Barang</p>
                <p className="text-xl font-bold">{stats.totalItems}</p>
              </div>
              <div className="bg-white/15 backdrop-blur-sm px-4 py-2 rounded-lg">
                <p className="text-xs text-blue-200">Total Stok</p>
                <p className="text-xl font-bold">{stats.totalStock}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-3">
              <span className="text-lg">📦</span>
            </div>
            <p className="text-2xl font-bold text-gray-800">{stats.totalItems}</p>
            <p className="text-xs text-gray-500 mt-0.5">Jenis Barang</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mb-3">
              <span className="text-lg">↓</span>
            </div>
            <p className="text-2xl font-bold text-green-600">{stats.totalMasuk}</p>
            <p className="text-xs text-gray-500 mt-0.5">Stok Masuk</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
            <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center mb-3">
              <span className="text-lg">↑</span>
            </div>
            <p className="text-2xl font-bold text-orange-600">{stats.totalKeluar}</p>
            <p className="text-xs text-gray-500 mt-0.5">Stok Keluar</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center mb-3">
              <span className="text-lg">⚠️</span>
            </div>
            <p className="text-2xl font-bold text-red-600">{stats.lowStock}</p>
            <p className="text-xs text-gray-500 mt-0.5">Stok Rendah</p>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Activity */}
          <div className="lg:col-span-2 bg-white rounded-xl border border-gray-100 shadow-sm">
            <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                <h2 className="text-base font-semibold text-gray-800">Aktivitas Terbaru</h2>
              </div>
              <span className="text-xs text-gray-400 bg-gray-50 px-2.5 py-1 rounded-full border border-gray-100">Live</span>
            </div>
            <div className="p-5">
              {recentHistory.length === 0 ? (
                <div className="text-center py-10">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <span className="text-2xl">📋</span>
                  </div>
                  <p className="text-gray-500 font-medium">Belum ada aktivitas</p>
                  <p className="text-xs text-gray-400 mt-1">Scan QR Code atau tambah barang untuk memulai</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {recentHistory.map((history: any) => (
                    <div key={history.id} className={`flex items-center justify-between p-3.5 rounded-xl border transition-colors ${
                      history.tipe === 'masuk' 
                        ? 'bg-green-50/50 border-green-100 hover:bg-green-50' 
                        : 'bg-red-50/50 border-red-100 hover:bg-red-50'
                    }`}>
                      <div className="flex items-center space-x-3">
                        <div className={`w-9 h-9 rounded-lg flex items-center justify-center text-sm font-bold ${
                          history.tipe === 'masuk' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                        }`}>
                          {history.tipe === 'masuk' ? '↓' : '↑'}
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-800">{history.item?.nama_barang}</p>
                          <p className="text-xs text-gray-400">{history.keterangan}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className={`text-sm font-bold ${
                          history.tipe === 'masuk' ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {history.tipe === 'masuk' ? '+' : '-'}{history.jumlah}
                        </span>
                        <p className="text-xs text-gray-400">
                          {new Date(history.created_at).toLocaleDateString('id-ID', { day: 'numeric', month: 'short' })}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-5">
            {/* Daftar Barang + Status */}
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm">
              <div className="px-5 py-4 border-b border-gray-100">
                <h2 className="text-base font-semibold text-gray-800">Status Barang</h2>
              </div>
              <div className="p-4">
                {itemsData.length === 0 ? (
                  <p className="text-sm text-gray-400 text-center py-4">Belum ada barang</p>
                ) : (
                  <div className="space-y-2">
                    {itemsData.slice(0, 5).map((item: any) => (
                      <div key={item.id} className="flex items-center justify-between p-2.5 rounded-lg hover:bg-gray-50">
                        <div className="flex items-center space-x-2.5">
                          <div className="w-7 h-7 bg-blue-50 rounded-md flex items-center justify-center">
                            <span className="text-xs">📦</span>
                          </div>
                          <div>
                            <span className="text-sm text-gray-700 truncate block max-w-[120px]">{item.nama_barang}</span>
                            <span className="text-xs text-gray-400">Stok: {item.jumlah_stok}</span>
                          </div>
                        </div>
                        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                          item.status_terakhir === 'masuk' 
                            ? 'bg-green-100 text-green-700' 
                            : item.status_terakhir === 'keluar'
                              ? 'bg-red-100 text-red-700'
                              : 'bg-gray-100 text-gray-500'
                        }`}>
                          {item.status_terakhir || 'Belum scan'}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* IoT Status */}
            <div className="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-xl border border-indigo-100 p-5">
              <div className="flex items-center space-x-2 mb-3">
                <span className="text-lg">📷</span>
                <p className="text-sm font-semibold text-indigo-800">ESP32-CAM</p>
              </div>
              <p className="text-xs text-indigo-600 leading-relaxed">
                Perangkat IoT akan mengirim data otomatis saat QR Code di-scan. Pastikan ESP32-CAM terhubung ke jaringan yang sama.
              </p>
              <div className="mt-3 flex items-center space-x-1.5">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-xs text-indigo-500">API Endpoint aktif</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
