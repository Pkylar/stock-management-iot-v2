-- Database: stock_management_iot
CREATE DATABASE IF NOT EXISTS stock_management_iot;
USE stock_management_iot;

-- Tabel users
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabel items (barang)
CREATE TABLE items (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nama_barang VARCHAR(255) NOT NULL,
    nomor_seri VARCHAR(255) UNIQUE NOT NULL,
    mac_address VARCHAR(17) NOT NULL,
    jumlah_stok INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabel stock_histories (riwayat stok)
CREATE TABLE stock_histories (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    barang_id BIGINT UNSIGNED NOT NULL,
    tipe ENUM('masuk', 'keluar') NOT NULL,
    jumlah INT NOT NULL,
    keterangan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (barang_id) REFERENCES items(id) ON DELETE CASCADE
);

-- Insert sample data
INSERT INTO users (name, email, password) VALUES 
('Admin', 'admin@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi');

INSERT INTO items (nama_barang, nomor_seri, mac_address, jumlah_stok) VALUES 
('Laptop Dell', 'DL001', '00:1B:44:11:3A:B7', 5),
('Mouse Wireless', 'MW002', '00:1B:44:11:3A:B8', 10),
('Keyboard Mechanical', 'KM003', '00:1B:44:11:3A:B9', 8);