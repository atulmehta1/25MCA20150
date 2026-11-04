-- SQL Schema for Face Recognition Attendance System
-- Database name: face_attendance_db (or as configured in .env)

CREATE DATABASE IF NOT EXISTS face_attendance_db;
USE face_attendance_db;

-- 1. Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Face Embeddings Table
CREATE TABLE IF NOT EXISTS face_embeddings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    embedding LONGBLOB NOT NULL, -- Serialized float array of 128 elements
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- 3. Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'Present',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);
