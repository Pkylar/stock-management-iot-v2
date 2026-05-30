<?php

namespace App\Http\Controllers;

use App\Models\Item;
use App\Models\StockHistory;
use Illuminate\Http\Request;

class ItemController extends Controller
{
    public function index()
    {
        $items = Item::all();
        return response()->json($items);
    }

    public function store(Request $request)
    {
        $request->validate([
            'nama_barang' => 'required|string|max:255',
            'nomor_seri' => 'required|string|unique:items',
            'mac_address' => 'required|string|max:17',
            'jumlah_stok' => 'required|integer|min:0'
        ]);

        $item = Item::create($request->all());

        // Catat riwayat stok masuk
        if ($request->jumlah_stok > 0) {
            StockHistory::create([
                'barang_id' => $item->id,
                'tipe' => 'masuk',
                'jumlah' => $request->jumlah_stok,
                'keterangan' => 'Stok awal'
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
            'nomor_seri' => 'required|string|unique:items,nomor_seri,' . $id,
            'mac_address' => 'required|string|max:17',
            'jumlah_stok' => 'required|integer|min:0'
        ]);

        $oldStock = $item->jumlah_stok;
        $item->update($request->all());

        // Catat perubahan stok
        $stockDiff = $request->jumlah_stok - $oldStock;
        if ($stockDiff != 0) {
            StockHistory::create([
                'barang_id' => $item->id,
                'tipe' => $stockDiff > 0 ? 'masuk' : 'keluar',
                'jumlah' => abs($stockDiff),
                'keterangan' => 'Update manual'
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

    // API untuk ESP32-CAM
    public function scanQr(Request $request)
    {
        $request->validate([
            'nama_barang' => 'required|string',
            'nomor_seri' => 'required|string',
            'mac_address' => 'required|string'
        ]);

        $item = Item::where('nomor_seri', $request->nomor_seri)->first();

        if ($item) {
            // Update stok masuk
            $item->increment('jumlah_stok');
            
            StockHistory::create([
                'barang_id' => $item->id,
                'tipe' => 'masuk',
                'jumlah' => 1,
                'keterangan' => 'Scan QR Code ESP32-CAM'
            ]);
        } else {
            // Buat item baru
            $item = Item::create([
                'nama_barang' => $request->nama_barang,
                'nomor_seri' => $request->nomor_seri,
                'mac_address' => $request->mac_address,
                'jumlah_stok' => 1
            ]);

            StockHistory::create([
                'barang_id' => $item->id,
                'tipe' => 'masuk',
                'jumlah' => 1,
                'keterangan' => 'Item baru dari ESP32-CAM'
            ]);
        }

        return response()->json([
            'message' => 'QR Code processed successfully',
            'item' => $item
        ]);
    }
}