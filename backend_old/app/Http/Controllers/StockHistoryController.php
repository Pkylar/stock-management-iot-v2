<?php

namespace App\Http\Controllers;

use App\Models\StockHistory;
use Illuminate\Http\Request;

class StockHistoryController extends Controller
{
    public function index(Request $request)
    {
        $query = StockHistory::with('item');

        if ($request->has('tipe')) {
            $query->where('tipe', $request->tipe);
        }

        $histories = $query->orderBy('created_at', 'desc')->get();
        return response()->json($histories);
    }

    public function masuk()
    {
        $histories = StockHistory::with('item')
            ->where('tipe', 'masuk')
            ->orderBy('created_at', 'desc')
            ->get();
        return response()->json($histories);
    }

    public function keluar()
    {
        $histories = StockHistory::with('item')
            ->where('tipe', 'keluar')
            ->orderBy('created_at', 'desc')
            ->get();
        return response()->json($histories);
    }
}