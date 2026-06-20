-- StudioBookMusic – Schema + Demo Data for InfinityFree MySQL
-- Import this file in phpMyAdmin on InfinityFree.
-- Generated: 2026-05-07

SET NAMES utf8mb4;
SET time_zone = '+00:00';
SET FOREIGN_KEY_CHECKS = 0;

-- =============================================
-- Drop existing tables (clean start)
-- =============================================
DROP TABLE IF EXISTS `comments`;
DROP TABLE IF EXISTS `forum_posts`;
DROP TABLE IF EXISTS `bookings`;
DROP TABLE IF EXISTS `schedules`;
DROP TABLE IF EXISTS `studios`;
DROP TABLE IF EXISTS `sessions`;
DROP TABLE IF EXISTS `cache`;
DROP TABLE IF EXISTS `cache_locks`;
DROP TABLE IF EXISTS `jobs`;
DROP TABLE IF EXISTS `job_batches`;
DROP TABLE IF EXISTS `failed_jobs`;
DROP TABLE IF EXISTS `password_reset_tokens`;
DROP TABLE IF EXISTS `migrations`;
DROP TABLE IF EXISTS `users`;

-- =============================================
-- Schema
-- =============================================

CREATE TABLE `users` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `email_verified_at` TIMESTAMP NULL DEFAULT NULL,
  `password` VARCHAR(255) NOT NULL,
  `remember_token` VARCHAR(100) DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT NULL,
  `updated_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_email_unique` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `password_reset_tokens` (
  `email` VARCHAR(255) NOT NULL,
  `token` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `sessions` (
  `id` VARCHAR(255) NOT NULL,
  `user_id` BIGINT UNSIGNED NULL,
  `ip_address` VARCHAR(45) DEFAULT NULL,
  `user_agent` LONGTEXT DEFAULT NULL,
  `payload` LONGTEXT NOT NULL,
  `last_activity` INT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sessions_user_id_index` (`user_id`),
  KEY `sessions_last_activity_index` (`last_activity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `cache` (
  `key` VARCHAR(255) NOT NULL,
  `value` MEDIUMTEXT NOT NULL,
  `expiration` INT NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `cache_locks` (
  `key` VARCHAR(255) NOT NULL,
  `owner` VARCHAR(255) NOT NULL,
  `expiration` INT NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `jobs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `queue` VARCHAR(255) NOT NULL,
  `payload` LONGTEXT NOT NULL,
  `attempts` TINYINT UNSIGNED NOT NULL,
  `reserved_at` INT UNSIGNED NULL,
  `available_at` INT UNSIGNED NOT NULL,
  `created_at` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  KEY `jobs_queue_index` (`queue`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `job_batches` (
  `id` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `total_jobs` INT NOT NULL,
  `pending_jobs` INT NOT NULL,
  `failed_jobs` INT NOT NULL,
  `failed_job_ids` LONGTEXT NOT NULL,
  `options` MEDIUMTEXT NULL,
  `cancelled_at` INT NULL,
  `created_at` INT NOT NULL,
  `finished_at` INT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `failed_jobs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `uuid` VARCHAR(255) NOT NULL,
  `connection` TEXT NOT NULL,
  `queue` TEXT NOT NULL,
  `payload` LONGTEXT NOT NULL,
  `exception` LONGTEXT NOT NULL,
  `failed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `failed_jobs_uuid_unique` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `studios` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT UNSIGNED NULL,
  `name` VARCHAR(255) NOT NULL,
  `slug` VARCHAR(255) NOT NULL,
  `type` VARCHAR(255) NOT NULL,
  `description` TEXT NOT NULL,
  `location` VARCHAR(255) NOT NULL,
  `price_per_hour` DECIMAL(12,2) NOT NULL,
  `image_url` VARCHAR(255) DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT NULL,
  `updated_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `studios_slug_unique` (`slug`),
  KEY `studios_user_id_foreign` (`user_id`),
  CONSTRAINT `studios_user_id_foreign`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `schedules` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `studio_id` BIGINT UNSIGNED NOT NULL,
  `schedule_date` DATE NOT NULL,
  `start_time` TIME NOT NULL,
  `end_time` TIME NOT NULL,
  `is_available` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP NULL DEFAULT NULL,
  `updated_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `studio_schedule_unique` (`studio_id`, `schedule_date`, `start_time`, `end_time`),
  KEY `schedules_schedule_date_idx` (`schedule_date`),
  KEY `schedules_studio_id_foreign` (`studio_id`),
  CONSTRAINT `schedules_studio_id_foreign`
    FOREIGN KEY (`studio_id`) REFERENCES `studios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `bookings` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT UNSIGNED NOT NULL,
  `studio_id` BIGINT UNSIGNED NOT NULL,
  `schedule_id` BIGINT UNSIGNED NOT NULL,
  `booking_date` DATE NOT NULL,
  `booking_status` ENUM('pending','paid','confirmed') NOT NULL DEFAULT 'pending',
  `payment_status` ENUM('unpaid','paid') NOT NULL DEFAULT 'unpaid',
  `total_amount` DECIMAL(12,2) NOT NULL,
  `notes` TEXT DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT NULL,
  `updated_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `booking_schedule_unique` (`schedule_id`),
  KEY `bookings_booking_status_idx` (`booking_status`),
  KEY `bookings_payment_status_idx` (`payment_status`),
  KEY `bookings_user_id_foreign` (`user_id`),
  KEY `bookings_studio_id_foreign` (`studio_id`),
  CONSTRAINT `bookings_user_id_foreign`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `bookings_studio_id_foreign`
    FOREIGN KEY (`studio_id`) REFERENCES `studios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `bookings_schedule_id_foreign`
    FOREIGN KEY (`schedule_id`) REFERENCES `schedules` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `forum_posts` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT UNSIGNED NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` TIMESTAMP NULL DEFAULT NULL,
  `updated_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_posts_user_id_foreign` (`user_id`),
  CONSTRAINT `forum_posts_user_id_foreign`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `comments` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `forum_post_id` BIGINT UNSIGNED NOT NULL,
  `user_id` BIGINT UNSIGNED NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` TIMESTAMP NULL DEFAULT NULL,
  `updated_at` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comments_forum_post_id_foreign` (`forum_post_id`),
  KEY `comments_user_id_foreign` (`user_id`),
  CONSTRAINT `comments_forum_post_id_foreign`
    FOREIGN KEY (`forum_post_id`) REFERENCES `forum_posts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `comments_user_id_foreign`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `migrations` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `migration` VARCHAR(255) NOT NULL,
  `batch` INT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- Demo Data (Seeder)
-- =============================================

-- Test User: test@example.com / password
INSERT INTO `users` (`id`, `name`, `email`, `email_verified_at`, `password`, `created_at`, `updated_at`) VALUES
(1, 'Test User', 'test@example.com', NOW(), '$2y$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', NOW(), NOW());

-- Studios
INSERT INTO `studios` (`id`, `user_id`, `name`, `slug`, `type`, `description`, `location`, `price_per_hour`, `image_url`, `created_at`, `updated_at`) VALUES
(1, 1, 'Studio Harmoni', 'studio-harmoni', 'Rehearsal', 'Studio latihan band dengan akustik bersih, drum set lengkap, dan ruang nyaman.', 'Bandung', 120000.00, NULL, NOW(), NOW()),
(2, 1, 'Studio Resonansi', 'studio-resonansi', 'Recording', 'Studio rekaman sederhana untuk demo lagu, podcast, dan produksi konten musik.', 'Jakarta', 180000.00, NULL, NOW(), NOW()),
(3, 1, 'Studio Nada Biru', 'studio-nada-biru', 'Rehearsal', 'Ruangan latihan dengan sound system modern, cocok untuk komunitas dan band indie.', 'Yogyakarta', 150000.00, NULL, NOW(), NOW());

-- Schedules (future dates relative to May 2026)
INSERT INTO `schedules` (`id`, `studio_id`, `schedule_date`, `start_time`, `end_time`, `is_available`, `created_at`, `updated_at`) VALUES
(1,  1, '2026-05-10', '10:00:00', '12:00:00', 1, NOW(), NOW()),
(2,  1, '2026-05-10', '13:00:00', '15:00:00', 1, NOW(), NOW()),
(3,  1, '2026-05-11', '10:00:00', '12:00:00', 1, NOW(), NOW()),
(4,  1, '2026-05-11', '13:00:00', '15:00:00', 1, NOW(), NOW()),
(5,  1, '2026-05-12', '10:00:00', '12:00:00', 1, NOW(), NOW()),
(6,  1, '2026-05-12', '13:00:00', '15:00:00', 1, NOW(), NOW()),
(7,  2, '2026-05-10', '10:00:00', '12:00:00', 1, NOW(), NOW()),
(8,  2, '2026-05-10', '13:00:00', '15:00:00', 1, NOW(), NOW()),
(9,  2, '2026-05-11', '10:00:00', '12:00:00', 1, NOW(), NOW()),
(10, 2, '2026-05-11', '13:00:00', '15:00:00', 1, NOW(), NOW()),
(11, 2, '2026-05-12', '10:00:00', '12:00:00', 1, NOW(), NOW()),
(12, 2, '2026-05-12', '13:00:00', '15:00:00', 1, NOW(), NOW()),
(13, 3, '2026-05-10', '10:00:00', '12:00:00', 1, NOW(), NOW()),
(14, 3, '2026-05-10', '13:00:00', '15:00:00', 1, NOW(), NOW()),
(15, 3, '2026-05-11', '10:00:00', '12:00:00', 1, NOW(), NOW()),
(16, 3, '2026-05-11', '13:00:00', '15:00:00', 1, NOW(), NOW()),
(17, 3, '2026-05-12', '10:00:00', '12:00:00', 1, NOW(), NOW()),
(18, 3, '2026-05-12', '13:00:00', '15:00:00', 1, NOW(), NOW());

-- Migrations record (so Laravel thinks migrations have run)
INSERT INTO `migrations` (`migration`, `batch`) VALUES
('0001_01_01_000000_create_users_table', 1),
('0001_01_01_000001_create_cache_table', 1),
('0001_01_01_000002_create_jobs_table', 1),
('2026_04_23_000001_create_studios_table', 1),
('2026_04_23_000002_create_schedules_table', 1),
('2026_04_23_000003_create_bookings_table', 1),
('2026_04_23_000004_create_forum_posts_table', 1),
('2026_04_23_000005_create_comments_table', 1),
('2026_04_23_120001_add_phase1_query_indexes', 1),
('2026_04_23_130001_add_owner_to_studios_table', 1);

SET FOREIGN_KEY_CHECKS = 1;
