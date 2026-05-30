<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Item extends Model
{
    use HasFactory;

    protected $fillable = [
        'nama_barang',
        'nomor_seri',
        'mac_address',
        'jumlah_stok'
    ];

    public function stockHistories()
    {
        return $this->hasMany(StockHistory::class, 'barang_id');
    }
}