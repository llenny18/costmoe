-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 27, 2025 at 01:10 PM
-- Server version: 11.7.2-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `costmoe_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `ai_recommendations`
--

CREATE TABLE `ai_recommendations` (
  `recommendation_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `searched_product` varchar(255) DEFAULT NULL,
  `recommended_product` varchar(255) DEFAULT NULL,
  `confidence_level` decimal(5,2) DEFAULT NULL,
  `reason` text DEFAULT NULL,
  `generated_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `extracted_quotation_data`
--

CREATE TABLE `extracted_quotation_data` (
  `extracted_id` int(11) NOT NULL,
  `quotation_id` int(11) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `specifications` text DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `supplier_details` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `market_reports`
--

CREATE TABLE `market_reports` (
  `report_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `report_file` varchar(255) DEFAULT NULL,
  `report_path` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `notification_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `status` enum('unread','read') DEFAULT 'unread',
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `brand` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `rating` decimal(3,2) DEFAULT NULL,
  `availability` enum('in_stock','out_of_stock') DEFAULT NULL,
  `source_website` enum('Shopee','Lazada','Zalora','Carousell','TikTok Shop','PhilGEPS','Citimart','Amazon','eBay','AliExpress','Rakuten','Temu','Galleon','BeautyMNL') DEFAULT NULL,
  `source_url` text DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `product_name`, `description`, `category`, `brand`, `price`, `currency`, `rating`, `availability`, `source_website`, `source_url`, `last_updated`) VALUES
(1, 'Samsung Galaxy S23 Ultra', '256GB, Phantom Black, 6.8\" Dynamic AMOLED Display, 200MP Camera', 'Electronics', 'Samsung', 1199.99, 'USD', 4.70, 'in_stock', 'Amazon', 'https://www.amazon.com/Samsung-Galaxy-S23-Ultra', '2025-02-15 00:30:00'),
(2, 'Sony WH-1000XM5', 'Wireless Noise Cancelling Headphones with Auto Noise Cancelling Optimizer', 'Electronics', 'Sony', 349.99, 'USD', 4.80, 'in_stock', 'Amazon', 'https://www.amazon.com/Sony-WH-1000XM5', '2025-02-16 01:45:00'),
(3, 'Logitech MX Master 3S', 'Advanced Wireless Mouse, Ultra-fast Scrolling, 8K DPI', 'Electronics', 'Logitech', 99.99, 'USD', 4.50, 'in_stock', 'Amazon', 'https://www.amazon.com/Logitech-MX-Master-3S', '2025-02-10 06:20:00'),
(4, 'Apple MacBook Pro M2', '13-inch, 16GB RAM, 512GB SSD, Space Gray', 'Electronics', 'Apple', 1799.99, 'USD', 4.90, 'in_stock', 'Amazon', 'https://www.amazon.com/Apple-MacBook-Pro-M2', '2025-02-18 03:15:00'),
(5, 'Nike Air Zoom Pegasus 40', 'Men\'s Running Shoes, Black/White, Size 10', 'Footwear', 'Nike', 130.00, 'USD', 4.60, 'in_stock', 'Zalora', 'https://www.zalora.com/nike-air-zoom-pegasus-40', '2025-02-14 08:30:00'),
(6, 'Adidas Ultraboost 23', 'Women\'s Running Shoes, Pink, Size 8', 'Footwear', 'Adidas', 190.00, 'USD', 4.70, 'in_stock', 'Zalora', 'https://www.zalora.com/adidas-ultraboost-23', '2025-02-12 05:45:00'),
(7, 'Lego Star Wars Millennium Falcon', 'Building Kit, 1353 Pieces, Ages 9+', 'Toys', 'Lego', 169.99, 'USD', 4.80, 'in_stock', 'Amazon', 'https://www.amazon.com/Lego-Star-Wars-Millennium-Falcon', '2025-02-11 02:20:00'),
(8, 'KitchenAid Stand Mixer', '5 Quart, Tilt-Head, Empire Red', 'Home & Kitchen', 'KitchenAid', 379.99, 'USD', 4.90, 'in_stock', 'Amazon', 'https://www.amazon.com/KitchenAid-Stand-Mixer', '2025-02-13 01:10:00'),
(9, 'Neutrogena Hydro Boost Water Gel', 'Facial Moisturizer, 1.7 oz', 'Beauty', 'Neutrogena', 19.99, 'USD', 4.50, 'in_stock', 'BeautyMNL', 'https://www.beautymnl.com/neutrogena-hydro-boost', '2025-02-17 07:25:00'),
(10, 'Instant Pot Duo 7-in-1', 'Electric Pressure Cooker, 6 Quart', 'Home & Kitchen', 'Instant Pot', 89.99, 'USD', 4.70, 'in_stock', 'Amazon', 'https://www.amazon.com/Instant-Pot-Duo-7-in-1', '2025-02-09 04:30:00'),
(11, 'Dyson V11 Absolute', 'Cordless Vacuum Cleaner, Blue', 'Home Appliances', 'Dyson', 599.99, 'USD', 4.60, 'in_stock', 'Amazon', 'https://www.amazon.com/Dyson-V11-Absolute', '2025-02-14 06:50:00'),
(12, 'The Ordinary Niacinamide 10% + Zinc 1%', 'Facial Serum, 30ml', 'Beauty', 'The Ordinary', 6.99, 'USD', 4.70, 'in_stock', 'BeautyMNL', 'https://www.beautymnl.com/the-ordinary-niacinamide', '2025-02-15 03:20:00'),
(13, 'Bose QuietComfort Earbuds II', 'Noise Cancelling Wireless Earbuds, Triple Black', 'Electronics', 'Bose', 279.99, 'USD', 4.60, 'in_stock', 'Amazon', 'https://www.amazon.com/Bose-QuietComfort-Earbuds-II', '2025-02-16 02:15:00'),
(14, 'Lululemon Align Leggings', 'High-Rise Pant 25\", Black, Size 6', 'Apparel', 'Lululemon', 98.00, 'USD', 4.80, 'in_stock', 'Zalora', 'https://www.zalora.com/lululemon-align-leggings', '2025-02-10 01:30:00'),
(15, 'Kindle Paperwhite', '8GB, 6.8\" Display, Waterproof, Black', 'Electronics', 'Amazon', 139.99, 'USD', 4.70, 'in_stock', 'Amazon', 'https://www.amazon.com/Kindle-Paperwhite', '2025-02-13 08:45:00'),
(16, 'La Roche-Posay Anthelios Sunscreen', 'SPF 50 Mineral Sunscreen, 1.7 fl oz', 'Beauty', 'La Roche-Posay', 34.99, 'USD', 4.60, 'in_stock', 'BeautyMNL', 'https://www.beautymnl.com/la-roche-posay-anthelios', '2025-02-17 05:20:00'),
(17, 'Sennheiser HD 660 S', 'Open Back Audiophile Headphones', 'Electronics', 'Sennheiser', 499.99, 'USD', 4.80, 'in_stock', 'Amazon', 'https://www.amazon.com/Sennheiser-HD-660-S', '2025-02-18 07:10:00'),
(18, 'Crocs Classic Clog', 'Unisex, Navy, Size 9', 'Footwear', 'Crocs', 49.99, 'USD', 4.40, 'in_stock', 'Zalora', 'https://www.zalora.com/crocs-classic-clog', '2025-02-11 06:30:00'),
(19, 'Nintendo Switch OLED Model', 'White Joy-Con, 64GB', 'Electronics', 'Nintendo', 349.99, 'USD', 4.80, 'in_stock', 'Amazon', 'https://www.amazon.com/Nintendo-Switch-OLED-Model', '2025-02-15 02:45:00'),
(20, 'Patagonia Better Sweater Fleece Jacket', 'Men\'s, Black, Size L', 'Apparel', 'Patagonia', 159.00, 'USD', 4.70, 'in_stock', 'Zalora', 'https://www.zalora.com/patagonia-better-sweater', '2025-02-16 04:20:00'),
(21, 'Shark Robot Vacuum', 'Self-Empty Base, Mapping, Wi-Fi, AV2501', 'Home Appliances', 'Shark', 499.99, 'USD', 4.50, 'in_stock', 'Amazon', 'https://www.amazon.com/Shark-Robot-Vacuum', '2025-02-09 01:15:00'),
(22, 'Cerave Hydrating Facial Cleanser', 'Normal to Dry Skin, 16 oz', 'Beauty', 'Cerave', 14.99, 'USD', 4.60, 'in_stock', 'BeautyMNL', 'https://www.beautymnl.com/cerave-hydrating-cleanser', '2025-02-14 05:40:00'),
(23, 'Sony PlayStation 5', 'Digital Edition, White, 825GB SSD', 'Electronics', 'Sony', 399.99, 'USD', 4.80, 'out_of_stock', 'Amazon', 'https://www.amazon.com/Sony-PlayStation-5', '2025-02-12 08:30:00'),
(24, 'Asus ROG Strix Gaming Laptop', '15.6\", Intel i7, 16GB RAM, 1TB SSD, RTX 3070', 'Electronics', 'Asus', 1699.99, 'USD', 4.50, 'in_stock', 'Amazon', 'https://www.amazon.com/Asus-ROG-Strix-Gaming-Laptop', '2025-02-10 07:20:00'),
(25, 'Hydro Flask Water Bottle', '32 oz, Wide Mouth, Pacific Blue', 'Sports & Outdoors', 'Hydro Flask', 44.95, 'USD', 4.70, 'in_stock', 'Amazon', 'https://www.amazon.com/Hydro-Flask-Water-Bottle', '2025-02-13 03:45:00'),
(26, 'Xiaomi Redmi Note 12 Pro', '8GB RAM, 256GB, Glacier Blue, 108MP Camera', 'Electronics', 'Xiaomi', 349.99, 'USD', 4.40, 'in_stock', 'Lazada', 'https://www.lazada.com/xiaomi-redmi-note-12-pro', '2025-02-15 06:10:00'),
(27, 'Uniqlo Heattech Turtleneck', 'Women\'s, Black, Size M', 'Apparel', 'Uniqlo', 19.90, 'USD', 4.60, 'in_stock', 'Zalora', 'https://www.zalora.com/uniqlo-heattech-turtleneck', '2025-02-17 02:30:00'),
(28, 'Airpods Pro 2nd Generation', 'Active Noise Cancellation, Transparency Mode', 'Electronics', 'Apple', 249.99, 'USD', 4.70, 'in_stock', 'Amazon', 'https://www.amazon.com/Airpods-Pro-2nd-Generation', '2025-02-16 05:15:00'),
(29, 'Fjallraven Kanken Backpack', 'Classic, Frost Green, 16L', 'Bags & Accessories', 'Fjallraven', 79.95, 'USD', 4.60, 'in_stock', 'Zalora', 'https://www.zalora.com/fjallraven-kanken-backpack', '2025-02-11 01:45:00'),
(30, 'Philips Sonicare DiamondClean', 'Smart Electric Toothbrush, White', 'Health & Personal Care', 'Philips', 229.99, 'USD', 4.50, 'in_stock', 'Amazon', 'https://www.amazon.com/Philips-Sonicare-DiamondClean', '2025-02-12 07:20:00'),
(31, 'Calvin Klein Cotton Stretch Boxer Briefs', 'Men\'s, Black, Pack of 3, Size M', 'Apparel', 'Calvin Klein', 39.99, 'USD', 4.60, 'in_stock', 'Zalora', 'https://www.zalora.com/calvin-klein-cotton-stretch', '2025-02-14 03:30:00'),
(32, 'Waterpik Water Flosser', 'Cordless Advanced, White', 'Health & Personal Care', 'Waterpik', 99.99, 'USD', 4.50, 'in_stock', 'Amazon', 'https://www.amazon.com/Waterpik-Water-Flosser', '2025-02-18 06:20:00'),
(33, 'Fitbit Charge 5', 'Advanced Fitness Tracker, Black/Graphite', 'Electronics', 'Fitbit', 149.95, 'USD', 4.30, 'in_stock', 'Amazon', 'https://www.amazon.com/Fitbit-Charge-5', '2025-02-15 04:45:00'),
(34, 'Under Armour Tech 2.0 T-Shirt', 'Men\'s, Gray, Size L', 'Apparel', 'Under Armour', 25.00, 'USD', 4.40, 'in_stock', 'Zalora', 'https://www.zalora.com/under-armour-tech-2.0', '2025-02-13 07:30:00'),
(35, 'JBL Flip 6', 'Portable Bluetooth Speaker, Black', 'Electronics', 'JBL', 129.99, 'USD', 4.60, 'in_stock', 'Amazon', 'https://www.amazon.com/JBL-Flip-6', '2025-02-11 05:10:00'),
(36, 'Anker PowerCore 26800', 'Portable Charger, 26800mAh', 'Electronics', 'Anker', 69.99, 'USD', 4.70, 'in_stock', 'Amazon', 'https://www.amazon.com/Anker-PowerCore-26800', '2025-02-16 03:25:00'),
(37, 'Razer DeathAdder V3 Pro', 'Wireless Gaming Mouse, White', 'Electronics', 'Razer', 149.99, 'USD', 4.60, 'in_stock', 'Amazon', 'https://www.amazon.com/Razer-DeathAdder-V3-Pro', '2025-02-17 08:40:00'),
(38, 'Ray-Ban Aviator Sunglasses', 'Classic Gold Frame, Green G-15 Lens', 'Eyewear', 'Ray-Ban', 169.00, 'USD', 4.70, 'in_stock', 'Zalora', 'https://www.zalora.com/ray-ban-aviator-sunglasses', '2025-02-10 02:15:00'),
(39, 'Nespresso Vertuo Coffee Machine', 'Matte Black, with Aeroccino Milk Frother', 'Home & Kitchen', 'Nespresso', 249.99, 'USD', 4.60, 'in_stock', 'Amazon', 'https://www.amazon.com/Nespresso-Vertuo-Coffee-Machine', '2025-02-12 06:30:00'),
(40, 'S\'well Stainless Steel Water Bottle', '17 oz, Teakwood', 'Sports & Outdoors', 'S\'well', 35.00, 'USD', 4.40, 'in_stock', 'Amazon', 'https://www.amazon.com/Swell-Stainless-Steel-Water-Bottle', '2025-02-15 01:50:00'),
(41, 'SKIMS Soft Lounge Slip Dress', 'Women\'s, Onyx, Size S', 'Apparel', 'SKIMS', 78.00, 'USD', 4.60, 'out_of_stock', 'Zalora', 'https://www.zalora.com/skims-soft-lounge-slip-dress', '2025-02-18 02:35:00'),
(42, 'Supergoop! Unseen Sunscreen', 'SPF 40, 1.7 fl oz', 'Beauty', 'Supergoop!', 36.00, 'USD', 4.70, 'in_stock', 'BeautyMNL', 'https://www.beautymnl.com/supergoop-unseen-sunscreen', '2025-02-11 07:40:00'),
(43, 'ASUS ROG Swift Gaming Monitor', '27\", 165Hz, 1ms, QHD, G-SYNC', 'Electronics', 'ASUS', 599.99, 'USD', 4.60, 'in_stock', 'Amazon', 'https://www.amazon.com/ASUS-ROG-Swift-Gaming-Monitor', '2025-02-13 05:20:00'),
(44, 'Anthropologie Gleaming Primrose Mirror', '5\' x 7\', Gold', 'Home Decor', 'Anthropologie', 548.00, 'USD', 4.80, 'in_stock', 'Amazon', 'https://www.amazon.com/Anthropologie-Gleaming-Primrose-Mirror', '2025-02-16 07:10:00'),
(45, 'Vans Old Skool Classic', 'Unisex, Black/White, Size 8', 'Footwear', 'Vans', 69.95, 'USD', 4.70, 'in_stock', 'Zalora', 'https://www.zalora.com/vans-old-skool-classic', '2025-02-14 01:25:00'),
(46, 'De\'Longhi Magnifica Automatic Coffee Machine', 'ESAM3300, Silver', 'Home & Kitchen', 'De\'Longhi', 799.99, 'USD', 4.60, 'in_stock', 'Amazon', 'https://www.amazon.com/DeLonghi-Magnifica-Automatic-Coffee-Machine', '2025-02-09 06:50:00'),
(47, 'Stanley Quencher H2.0 FlowState Tumbler', '40 oz, Cream', 'Sports & Outdoors', 'Stanley', 45.00, 'USD', 4.90, 'out_of_stock', 'Amazon', 'https://www.amazon.com/Stanley-Quencher-H2.0-FlowState-Tumbler', '2025-02-17 03:15:00'),
(48, 'COSRX Advanced Snail 96 Mucin Power Essence', '100ml', 'Beauty', 'COSRX', 25.00, 'USD', 4.80, 'in_stock', 'BeautyMNL', 'https://www.beautymnl.com/cosrx-advanced-snail-96', '2025-02-10 08:30:00'),
(49, 'Keychron K2 Mechanical Keyboard', 'Wireless, Hot-swappable, RGB, Brown Switches', 'Electronics', 'Keychron', 99.00, 'USD', 4.70, 'in_stock', 'Amazon', 'https://www.amazon.com/Keychron-K2-Mechanical-Keyboard', '2025-02-15 05:40:00'),
(50, 'Oura Ring Gen 3', 'Fitness Tracker, Silver, Size 10', 'Electronics', 'Oura', 299.00, 'USD', 4.50, 'in_stock', 'Amazon', 'https://www.amazon.com/Oura-Ring-Gen-3', '2025-02-18 04:15:00');

-- --------------------------------------------------------

--
-- Table structure for table `product_history`
--

CREATE TABLE `product_history` (
  `history_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `availability` enum('in_stock','out_of_stock') DEFAULT NULL,
  `recorded_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `product_price_by_source`
-- (See below for the actual view)
--
CREATE TABLE `product_price_by_source` (
`id` bigint(21)
,`source_website` enum('Shopee','Lazada','Zalora','Carousell','TikTok Shop','PhilGEPS','Citimart','Amazon','eBay','AliExpress','Rakuten','Temu','Galleon','BeautyMNL')
,`category` varchar(100)
,`last_updated` timestamp
,`brand` varchar(100)
,`product_count` bigint(21)
,`avg_price` decimal(14,6)
,`min_price` decimal(10,2)
,`max_price` decimal(10,2)
,`avg_rating` decimal(7,6)
);

-- --------------------------------------------------------

--
-- Table structure for table `quotations`
--

CREATE TABLE `quotations` (
  `quotation_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `file_path` text DEFAULT NULL,
  `uploaded_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `system_logs`
--

CREATE TABLE `system_logs` (
  `log_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `action` text DEFAULT NULL,
  `log_time` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','analyst','business_owner') NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure for view `product_price_by_source`
--
DROP TABLE IF EXISTS `product_price_by_source`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `product_price_by_source`  AS SELECT row_number() over ( order by `products`.`source_website`,`products`.`category`,avg(`products`.`price`) desc) AS `id`, `products`.`source_website` AS `source_website`, `products`.`category` AS `category`, `products`.`last_updated` AS `last_updated`, `products`.`brand` AS `brand`, count(0) AS `product_count`, avg(`products`.`price`) AS `avg_price`, min(`products`.`price`) AS `min_price`, max(`products`.`price`) AS `max_price`, avg(`products`.`rating`) AS `avg_rating` FROM `products` GROUP BY `products`.`source_website`, `products`.`category`, `products`.`brand` ORDER BY `products`.`source_website` ASC, `products`.`category` ASC, avg(`products`.`price`) DESC ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ai_recommendations`
--
ALTER TABLE `ai_recommendations`
  ADD PRIMARY KEY (`recommendation_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `extracted_quotation_data`
--
ALTER TABLE `extracted_quotation_data`
  ADD PRIMARY KEY (`extracted_id`),
  ADD KEY `quotation_id` (`quotation_id`);

--
-- Indexes for table `market_reports`
--
ALTER TABLE `market_reports`
  ADD PRIMARY KEY (`report_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`notification_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `product_history`
--
ALTER TABLE `product_history`
  ADD PRIMARY KEY (`history_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `quotations`
--
ALTER TABLE `quotations`
  ADD PRIMARY KEY (`quotation_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `system_logs`
--
ALTER TABLE `system_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ai_recommendations`
--
ALTER TABLE `ai_recommendations`
  MODIFY `recommendation_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `extracted_quotation_data`
--
ALTER TABLE `extracted_quotation_data`
  MODIFY `extracted_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `market_reports`
--
ALTER TABLE `market_reports`
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `notification_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `product_history`
--
ALTER TABLE `product_history`
  MODIFY `history_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `quotations`
--
ALTER TABLE `quotations`
  MODIFY `quotation_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `system_logs`
--
ALTER TABLE `system_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ai_recommendations`
--
ALTER TABLE `ai_recommendations`
  ADD CONSTRAINT `ai_recommendations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `extracted_quotation_data`
--
ALTER TABLE `extracted_quotation_data`
  ADD CONSTRAINT `extracted_quotation_data_ibfk_1` FOREIGN KEY (`quotation_id`) REFERENCES `quotations` (`quotation_id`) ON DELETE CASCADE;

--
-- Constraints for table `market_reports`
--
ALTER TABLE `market_reports`
  ADD CONSTRAINT `market_reports_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `product_history`
--
ALTER TABLE `product_history`
  ADD CONSTRAINT `product_history_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE;

--
-- Constraints for table `quotations`
--
ALTER TABLE `quotations`
  ADD CONSTRAINT `quotations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `system_logs`
--
ALTER TABLE `system_logs`
  ADD CONSTRAINT `system_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
