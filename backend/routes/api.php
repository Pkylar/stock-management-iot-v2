<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\ItemController;
use App\Http\Controllers\StockHistoryController;
use App\Http\Controllers\ScanBarcodeController;

// Auth routes
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);

// ESP32-CAM routes (tidak perlu auth)
Route::post('/scan-qr', [ItemController::class, 'scanQr']);
Route::post('/scan-barcode', [ScanBarcodeController::class, 'scan']);

// Protected routes
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/user', function (Request $request) {
        return $request->user();
    });

    // Items routes
    Route::apiResource('items', ItemController::class);
    Route::post('/items/{id}/keluar', [ItemController::class, 'stokKeluar']);

    // Stock history routes
    Route::get('/stock-histories', [StockHistoryController::class, 'index']);
    Route::get('/stock-histories/masuk', [StockHistoryController::class, 'masuk']);
    Route::get('/stock-histories/keluar', [StockHistoryController::class, 'keluar']);
});
