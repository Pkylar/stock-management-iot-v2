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
        'status_terakhir'
    ];

    public function stockHistories()
    {
        return $this->hasMany(StockHistory::class, 'barang_id');
    }

    public function latestHistory()
    {
        return $this->hasOne(StockHistory::class, 'barang_id')->latestOfMany();
    }
}
