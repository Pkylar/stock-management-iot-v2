<?php

namespace App\Http\Controllers;

use App\Models\Item;
use App\Models\StockHistory;
use Illuminate\Http\Request;

class ItemController extends Controller
{
    public function index()
    {
        $items = Item::with(['creator', 'updater'])->get();
        return response()->json($items);
    }

    public function store(Request $request)
    {
        $request->validate([
            'nama_barang' => 'required|string|max:255',
            'kode_barang' => 'required|string|unique:items',
            'jumlah_stok' => 'required|integer|min:0'
        ]);

        $item = Item::create([
            'nama_barang' => $request->nama_barang,
            'kode_barang' => $request->kode_barang,
            'jumlah_stok' => $request->jumlah_stok,
            'status_terakhir' => $request->jumlah_stok > 0 ? 'masuk' : null,
            'created_by' => auth()->id(),
        ]);

        if ($request->jumlah_stok > 0) {
            StockHistory::create([
                'barang_id' => $item->id,
                'tipe' => 'masuk',
                'jumlah' => $request->jumlah_stok,
                'keterangan' => 'Stok awal',
                'sumber' => 'manual',
                'created_by' => auth()->id(),
            ]);
        }

        return response()->json($item, 201);
    }

    public function show($id)
    {
        $item = Item::findOrFail($id);
        return response()->json($item);
    }

    public function update(Request $request, $id)
    {
        $item = Item::findOrFail($id);
        
        $request->validate([
            'nama_barang' => 'required|string|max:255',
            'kode_barang' => 'required|string|unique:items,kode_barang,' . $id,
            'jumlah_stok' => 'required|integer|min:0'
        ]);

        $oldStock = $item->jumlah_stok;
        $item->update(array_merge(
            $request->only(['nama_barang', 'kode_barang', 'jumlah_stok']),
            ['updated_by' => auth()->id()]
        ));

        $stockDiff = $request->jumlah_stok - $oldStock;
        if ($stockDiff != 0) {
            $tipe = $stockDiff > 0 ? 'masuk' : 'keluar';
            $item->update(['status_terakhir' => $tipe]);

            StockHistory::create([
                'barang_id' => $item->id,
                'tipe' => $tipe,
                'jumlah' => abs($stockDiff),
                'keterangan' => 'Update manual',
                'sumber' => 'manual',
                'created_by' => auth()->id(),
            ]);
        }

        return response()->json($item);
    }

    public function destroy($id)
    {
        $item = Item::findOrFail($id);
        $item->delete();
        return response()->json(['message' => 'Item deleted successfully']);
    }

    public function stokKeluar(Request $request, $id)
    {
        $item = Item::findOrFail($id);

        $request->validate([
            'jumlah' => 'required|integer|min:1',
            'keterangan' => 'nullable|string',
        ]);

        $jumlah = $request->jumlah;

        if ($item->jumlah_stok < $jumlah) {
            return response()->json(['message' => 'Stok tidak cukup'], 400);
        }

        $item->jumlah_stok -= $jumlah;
        $item->status_terakhir = 'keluar';
        $item->save();

        StockHistory::create([
            'barang_id' => $item->id,
            'tipe' => 'keluar',
            'jumlah' => $jumlah,
            'keterangan' => $request->keterangan ?? 'Stok keluar manual',
            'sumber' => 'manual',
            'created_by' => auth()->id(),
        ]);

        // Hapus barang dari stok jika stok 0
        if ($item->jumlah_stok <= 0) {
            $item->delete();
            return response()->json([
                'message' => 'Barang dikeluarkan dan dihapus dari stok',
            ]);
        }

        return response()->json([
            'message' => 'Stok berhasil dikeluarkan',
            'item' => $item,
        ]);
    }

    // API untuk ESP32-CAM
    public function scanQr(Request $request)
    {
        $request->validate([
            'kode_barang' => 'required|string',
            'jumlah' => 'required|integer|min:1',
            'tipe' => 'required|in:masuk,keluar',
        ]);

        $item = Item::where('kode_barang', $request->kode_barang)->first();

        if ($item) {
            if ($request->tipe === 'masuk') {
                $item->jumlah_stok += $request->jumlah;
            } else {
                $item->jumlah_stok -= $request->jumlah;
            }
            $item->status_terakhir = $request->tipe;
            $item->save();
        } else {
            $item = Item::create([
                'nama_barang' => $request->kode_barang,
                'kode_barang' => $request->kode_barang,
                'jumlah_stok' => $request->jumlah,
                'status_terakhir' => 'masuk',
                'created_by' => 1, // Default system user for ESP32
            ]);
        }

        StockHistory::create([
            'barang_id' => $item->id,
            'tipe' => $request->tipe,
            'jumlah' => $request->jumlah,
            'keterangan' => 'Scan QR ESP32',
            'sumber' => 'esp32_cam',
            'created_by' => 1, // Default system user for ESP32
        ]);

        return response()->json([
            'message' => 'QR processed',
            'item' => $item
        ]);
    }
}