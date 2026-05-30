<?php

namespace App\Http\Controllers;

use App\Models\Item;
use App\Models\StockHistory;
use Illuminate\Http\Request;

class ScanBarcodeController extends Controller
{
    public function scan(Request $request)
    {
        $request->validate([
            'kode_barang' => 'required|string',
            'jumlah' => 'required|integer|min:1',
            'tipe' => 'required|in:masuk,keluar',
        ]);

        $kodeBarang = $request->kode_barang;
        $jumlah = $request->jumlah;
        $tipe = $request->tipe;

        $item = Item::where('kode_barang', $kodeBarang)->first();

        if (!$item) {
            if ($tipe === 'keluar') {
                return response()->json([
                    'success' => false,
                    'message' => 'Barang tidak ditemukan',
                ], 404);
            }

            $item = Item::create([
                'nama_barang' => $kodeBarang,
                'kode_barang' => $kodeBarang,
                'jumlah_stok' => $jumlah,
                'status_terakhir' => 'masuk',
            ]);

            StockHistory::create([
                'barang_id' => $item->id,
                'tipe' => 'masuk',
                'jumlah' => $jumlah,
                'keterangan' => 'Barang baru dari scan ESP32',
                'sumber' => 'esp32_cam',
            ]);

            return response()->json([
                'success' => true,
                'message' => 'Barang baru ditambahkan',
                'data_barang' => $item,
            ]);
        }

        if ($tipe === 'masuk') {
            $item->jumlah_stok += $jumlah;
        } else {
            if ($item->jumlah_stok < $jumlah) {
                return response()->json([
                    'success' => false,
                    'message' => 'Stok tidak cukup',
                ], 400);
            }
            $item->jumlah_stok -= $jumlah;
        }

        $item->status_terakhir = $tipe;
        $item->save();

        StockHistory::create([
            'barang_id' => $item->id,
            'tipe' => $tipe,
            'jumlah' => $jumlah,
            'keterangan' => 'Scan QR ESP32',
            'sumber' => 'esp32_cam',
        ]);

        return response()->json([
            'success' => true,
            'message' => "Stok $tipe berhasil",
            'data_barang' => $item,
        ]);
    }
}
