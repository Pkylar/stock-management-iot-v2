<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class StockHistory extends Model
{
    use HasFactory;

    protected $fillable = [
        'barang_id',
        'tipe',
        'jumlah',
        'keterangan'
    ];

    public function item()
    {
        return $this->belongsTo(Item::class, 'barang_id');
    }
}