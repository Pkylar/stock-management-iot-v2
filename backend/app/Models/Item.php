<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Item extends Model
{
    use HasFactory;

    protected $fillable = [
        'nama_barang',
        'kode_barang',
        'jumlah_stok',
        'status_terakhir',
        'created_by',
        'updated_by'
    ];

    public function creator()
    {
        return $this->belongsTo(User::class, 'created_by');
    }

    public function updater()
    {
        return $this->belongsTo(User::class, 'updated_by');
    }

    public function stockHistories()
    {
        return $this->hasMany(StockHistory::class, 'barang_id');
    }

    public function latestHistory()
    {
        return $this->hasOne(StockHistory::class, 'barang_id')->latestOfMany();
    }
}
