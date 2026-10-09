-- -------------------------------------------------------------
-- Student Registration Management System
-- Comprehensive Database Schema for MySQL
-- -------------------------------------------------------------

CREATE DATABASE IF NOT EXISTS `student_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `student_db`;

DROP TABLE IF EXISTS `attendance`;
DROP TABLE IF EXISTS `grades`;
DROP TABLE IF EXISTS `students`;

-- 1. Students Table
CREATE TABLE `students` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` VARCHAR(20) NOT NULL UNIQUE,
    `full_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `phone` VARCHAR(20) NOT NULL,
    `course` VARCHAR(80) NOT NULL,
    `gender` VARCHAR(20) NOT NULL,
    `dob` DATE NOT NULL,
    `address` TEXT DEFAULT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'Active',
    `profile_image` VARCHAR(255) DEFAULT NULL,
    `total_fee` DOUBLE DEFAULT 50000.0,
    `paid_fee` DOUBLE DEFAULT 0.0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_student_id` (`student_id`),
    INDEX `idx_course` (`course`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Grades Table
CREATE TABLE `grades` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `subject_name` VARCHAR(100) NOT NULL,
    `semester` VARCHAR(30) NOT NULL DEFAULT 'Semester 1',
    `marks_obtained` DOUBLE NOT NULL,
    `max_marks` DOUBLE NOT NULL DEFAULT 100.0,
    `grade_letter` VARCHAR(5) NOT NULL DEFAULT 'A',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Attendance Table
CREATE TABLE `attendance` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `attendance_date` DATE NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'Present',
    `remarks` VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
