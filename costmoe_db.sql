-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 15, 2025 at 09:56 AM
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
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add ai recommendations', 7, 'add_airecommendations'),
(26, 'Can change ai recommendations', 7, 'change_airecommendations'),
(27, 'Can delete ai recommendations', 7, 'delete_airecommendations'),
(28, 'Can view ai recommendations', 7, 'view_airecommendations'),
(29, 'Can add extracted quotation data', 8, 'add_extractedquotationdata'),
(30, 'Can change extracted quotation data', 8, 'change_extractedquotationdata'),
(31, 'Can delete extracted quotation data', 8, 'delete_extractedquotationdata'),
(32, 'Can view extracted quotation data', 8, 'view_extractedquotationdata'),
(33, 'Can add market reports', 9, 'add_marketreports'),
(34, 'Can change market reports', 9, 'change_marketreports'),
(35, 'Can delete market reports', 9, 'delete_marketreports'),
(36, 'Can view market reports', 9, 'view_marketreports'),
(37, 'Can add notifications', 10, 'add_notifications'),
(38, 'Can change notifications', 10, 'change_notifications'),
(39, 'Can delete notifications', 10, 'delete_notifications'),
(40, 'Can view notifications', 10, 'view_notifications'),
(41, 'Can add product history', 11, 'add_producthistory'),
(42, 'Can change product history', 11, 'change_producthistory'),
(43, 'Can delete product history', 11, 'delete_producthistory'),
(44, 'Can view product history', 11, 'view_producthistory'),
(45, 'Can add product price by source', 12, 'add_productpricebysource'),
(46, 'Can change product price by source', 12, 'change_productpricebysource'),
(47, 'Can delete product price by source', 12, 'delete_productpricebysource'),
(48, 'Can view product price by source', 12, 'view_productpricebysource'),
(49, 'Can add products', 13, 'add_products'),
(50, 'Can change products', 13, 'change_products'),
(51, 'Can delete products', 13, 'delete_products'),
(52, 'Can view products', 13, 'view_products'),
(53, 'Can add quotations', 14, 'add_quotations'),
(54, 'Can change quotations', 14, 'change_quotations'),
(55, 'Can delete quotations', 14, 'delete_quotations'),
(56, 'Can view quotations', 14, 'view_quotations'),
(57, 'Can add system logs', 15, 'add_systemlogs'),
(58, 'Can change system logs', 15, 'change_systemlogs'),
(59, 'Can delete system logs', 15, 'delete_systemlogs'),
(60, 'Can view system logs', 15, 'view_systemlogs'),
(61, 'Can add users', 16, 'add_users'),
(62, 'Can change users', 16, 'change_users'),
(63, 'Can delete users', 16, 'delete_users'),
(64, 'Can view users', 16, 'view_users');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'costmoeapp', 'airecommendations'),
(8, 'costmoeapp', 'extractedquotationdata'),
(9, 'costmoeapp', 'marketreports'),
(10, 'costmoeapp', 'notifications'),
(11, 'costmoeapp', 'producthistory'),
(12, 'costmoeapp', 'productpricebysource'),
(13, 'costmoeapp', 'products'),
(14, 'costmoeapp', 'quotations'),
(15, 'costmoeapp', 'systemlogs'),
(16, 'costmoeapp', 'users'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-04-14 03:08:07.637870'),
(2, 'auth', '0001_initial', '2025-04-14 03:08:07.957414'),
(3, 'admin', '0001_initial', '2025-04-14 03:08:08.034523'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-04-14 03:08:08.043670'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-04-14 03:08:08.058025'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-04-14 03:08:08.116052'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-04-14 03:08:08.213530'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-04-14 03:08:08.248033'),
(9, 'auth', '0004_alter_user_username_opts', '2025-04-14 03:08:08.259466'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-04-14 03:08:08.298430'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-04-14 03:08:08.301036'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-04-14 03:08:08.321430'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-04-14 03:08:08.352603'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-04-14 03:08:08.381137'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-04-14 03:08:08.408603'),
(16, 'auth', '0011_update_proxy_permissions', '2025-04-14 03:08:08.417121'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-04-14 03:08:08.448609'),
(18, 'costmoeapp', '0001_initial', '2025-04-14 03:08:08.468064'),
(19, 'sessions', '0001_initial', '2025-04-14 03:08:08.517880');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
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
(26, 'Xiaomi Redmi Note 12 Pro', '8GB RAM, 256GB, Glacier Blue, 108MP Camera', 'Electronics', 'Xiaomi', 349.99, 'PHP', 4.40, 'in_stock', 'Lazada', 'https://www.lazada.com/xiaomi-redmi-note-12-pro', '2025-04-15 07:50:47'),
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
  `full_name` varchar(300) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','analyst','business_owner','costumer') NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `full_name`, `email`, `password_hash`, `role`, `created_at`) VALUES
(1, 'trynew', 'ehehe', 'email@email.com', 'trynewpass', 'costumer', '2025-04-14 02:45:50'),
(2, 'werwe', 'rwrwe', 'ramosalleneid01@gmail.com', 'password', 'costumer', '2025-04-14 18:21:30'),
(3, 'admin', 'costmoeadmin', 'admin@gmail.com', 'password', 'admin', '2025-04-14 18:21:30'),
(4, 'trynewuser', 'full name sample', 'email1@email.com', 'password', 'costumer', '2025-04-14 23:35:32');

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
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

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
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

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
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ai_recommendations`
--
ALTER TABLE `ai_recommendations`
  ADD CONSTRAINT `ai_recommendations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

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
