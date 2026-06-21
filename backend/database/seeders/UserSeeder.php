<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;
use App\Models\User;

class UserSeeder extends Seeder
{
    public function run(): void
    {
        User::create([
            'id' => 1,
            'name' => 'System ESP32',
            'email' => 'system@esp32.local',
            'password' => Hash::make('esp32system'),
            'role' => 'staff',
        ]);
    }
}