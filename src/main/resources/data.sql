-- Insert sample products
INSERT INTO products (name, brand, category, description, specs, price, stock_quantity, image_url, is_active) VALUES
('Acer Aspire 5', 'Acer', 'laptop', '15.6 inch Full HD display laptop with AMD Ryzen 5 processor, 16GB RAM, 512GB SSD, quiet cooling fan, long battery life perfect for students and professionals', 'Ryzen 5 5500U, 16GB DDR4, 512GB NVMe SSD, WiFi 6, Windows 11', 54990.00, 15, null, true),
('HP Pavilion 14', 'HP', 'laptop', 'Lightweight 14 inch ultrabook with Intel Core i5 processor, excellent keyboard, all-day battery life', 'Intel i5-1235U, 8GB RAM, 256GB SSD, Iris Xe Graphics, B&O Audio', 61990.00, 10, null, true),
('Dell Inspiron 15 3000', 'Dell', 'laptop', 'Budget-friendly 15.6 inch laptop for everyday computing, web browsing, and office work', 'Intel i3-1115G4, 8GB RAM, 256GB SSD, HD Webcam, Ubuntu/Windows', 42990.00, 20, null, true),
('Lenovo IdeaPad Gaming 3', 'Lenovo', 'laptop', 'Entry-level gaming laptop with dedicated NVIDIA graphics, 120Hz display for smooth gaming', 'Ryzen 5 6600H, 16GB RAM, 512GB SSD, RTX 3050, 120Hz FHD', 74990.00, 8, null, true),
('ASUS VivoBook 15', 'ASUS', 'laptop', 'Stylish and portable 15.6 inch laptop with NanoEdge display, ErgoLift hinge', 'Intel i5-1135G7, 8GB RAM, 512GB SSD, Fingerprint, Windows 11', 49990.00, 12, null, true),
('Samsung Galaxy S23', 'Samsung', 'smartphone', 'Flagship Android smartphone with triple camera system, 120Hz AMOLED display', 'Snapdragon 8 Gen 2, 8GB RAM, 256GB storage, 50MP camera, 5G', 74999.00, 25, null, true),
('iPhone 14', 'Apple', 'smartphone', 'Premium iOS smartphone with dual camera system, Ceramic Shield front', 'A15 Bionic, 6GB RAM, 128GB storage, Dual 12MP cameras, 5G', 79900.00, 30, null, true),
('OnePlus 11R', 'OnePlus', 'smartphone', 'Fast charging flagship killer with 100W SUPERVOOC charging', 'Snapdragon 8+ Gen 1, 8GB RAM, 128GB UFS 3.1, 50MP IMX890', 39999.00, 18, null, true),
('iPad Air', 'Apple', 'tablet', 'Powerful tablet with M1 chip, 10.9 inch Liquid Retina display', 'M1 chip, 64GB storage, WiFi 6, 12MP cameras, USB-C', 59900.00, 15, null, true),
('Samsung Galaxy Tab S8', 'Samsung', 'tablet', 'Premium Android tablet with S Pen included, 120Hz display', 'Snapdragon 8 Gen 1, 8GB RAM, 128GB storage, 11 inch LCD', 55999.00, 10, null, true),
('Sony WH-1000XM5', 'Sony', 'headphones', 'Industry-leading noise canceling headphones with exceptional sound quality', 'ANC, Bluetooth 5.2, LDAC, 30hr battery, Multipoint', 29990.00, 20, null, true),
('AirPods Pro 2', 'Apple', 'earbuds', 'Premium wireless earbuds with active noise cancellation', 'H2 chip, ANC, 6hr + 30hr with case, IPX4, MagSafe', 24900.00, 35, null, true),
('Kindle Paperwhite', 'Amazon', 'e-reader', 'Waterproof e-reader with 6.8 inch glare-free display', '6.8 inch E-Ink, 300 ppi, IPX8, 8GB, USB-C, 10 weeks battery', 13999.00, 25, null, true);

-- Insert sample user (password is 'password123' hashed with bcrypt)
INSERT INTO users (email, password, first_name, last_name, phone_number, role, is_enabled) VALUES
('admin@smartcart.com', '$2a$10$TLb2gKJZ2UTmqSlKlTx9a.bSD0KeQDPsWCYMmRz2xQsQzRQIVNKgq', 'Admin', 'User', '1234567890', 'ADMIN', true),
('john@example.com', '$2a$10$TLb2gKJZ2UTmqSlKlTx9a.bSD0KeQDPsWCYMmRz2xQsQzRQIVNKgq', 'John', 'Doe', '9876543210', 'CUSTOMER', true);