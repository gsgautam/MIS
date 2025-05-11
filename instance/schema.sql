create database office_mb_db
use office_mb_db
CREATE TABLE office (
    id INT PRIMARY KEY AUTO_INCREMENT,          -- Unique ID (Apne aap badhega)
    bank_name VARCHAR(255) NOT NULL,            -- Bank ka naam (Khali nahi ho sakta)
    property_details TEXT NOT NULL,             -- Property ki details (Lamba text ho sakta hai)
    received_date DATETIME,                     -- Lead kab mili (Date aur Time)
    deadline DATE,                              -- Report ki deadline (Sirf Date)
    site_engineer VARCHAR(255) NULL,            -- Site Engineer ka naam (Khali ho sakta hai)
    report_creator VARCHAR(255) NULL,           -- Report banane wale Employer ka naam (Khali ho sakta hai)
    status VARCHAR(50) NOT NULL DEFAULT 'New'   -- Lead ka current status (Default 'New')
);
-- MySQL Script to Add 'users' table and update 'office' table

-- Assume database 'office_mis_db' exists and is selected
-- USE office_mis_db;

-- 1. Create the 'users' table

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,       -- Login username (unique hona chahiye)
    password_hash VARCHAR(255) NOT NULL,        -- Hashed password (kabhi bhi plain text nahi)
    role VARCHAR(20) NOT NULL DEFAULT 'user'    -- User role ('admin' or 'user')
);

-- 2. Optional: Add columns to 'office' table for issues and review
-- Check if columns exist before adding (avoids errors on re-run)
-- Note: Syntax for checking column existence varies slightly across MySQL versions.
-- This is a common approach, adjust if needed for your specific MySQL version.

ALTER TABLE office
ADD COLUMN  report_issue_notes TEXT NULL AFTER status;
ALTER TABLE office ADD COLUMN  admin_review_status VARCHAR(50) NULL DEFAULT 'Pending Review' AFTER report_issue_notes;

-- Optional: Insert an initial Admin user (Password needs to be hashed first using Python)
-- Example (DO NOT RUN THIS SQL DIRECTLY - Hash the password in Python first):
-- INSERT INTO users (username, password_hash, role) VALUES ('admin', 'HASHED_PASSWORD_HERE', 'admin');

-- Check tables
-- DESCRIBE users;
-- DESCRIBE office;
CREATE TABLE admins (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,      -- Admin ka unique ID
    username VARCHAR(50) NOT NULL UNIQUE,         -- Admin ka login username (unique)
    password_hash VARCHAR(255) NOT NULL          -- Admin ka Hashed password
    -- Ismein 'role' column ki zaroorat nahi, kyonki is table ke sabhi users admin hi honge
);
ALTER TABLE office ADD COLUMN date_of_allocation DATE NULL;
ALTER TABLE office ADD COLUMN customer_name VARCHAR(255) NULL;
ALTER TABLE office ADD COLUMN application_number VARCHAR(100) NULL;
ALTER TABLE office ADD COLUMN location VARCHAR(500) NULL;
ALTER TABLE office ADD COLUMN contact_number VARCHAR(50) NULL;
ALTER TABLE office ADD COLUMN site_link VARCHAR(1024) NULL;
ALTER TABLE office ADD COLUMN visit_initiation_date DATE NULL;
ALTER TABLE office ADD COLUMN visit_completion_date DATE NULL;
ALTER TABLE office ADD COLUMN lead_completion_date DATE NULL; -- Assuming 'LIAD' was typo for LEAD
ALTER TABLE office ADD COLUMN appraiser_quotation_obs VARCHAR(255) NULL; -- Needs clarification, adjust type if needed
ALTER TABLE office ADD COLUMN distance DECIMAL(10, 2) NULL; -- Assuming distance is numeric
ALTER TABLE office ADD COLUMN visit_type VARCHAR(100) NULL;
ALTER TABLE office ADD COLUMN remarks TEXT NULL;
ALTER TABLE office
ADD COLUMN branch_virtual VARCHAR(255) NULL DEFAULT NULL;

CREATE TABLE site_engineers (
    engineer_id INT PRIMARY KEY AUTO_INCREMENT,   -- Engineer ka unique ID
    username VARCHAR(50) NOT NULL UNIQUE,         -- Engineer ka login username (unique)
    full_name VARCHAR(100) NULL,                  -- Engineer ka poora naam (optional, but good for display)
    password_hash VARCHAR(255) NOT NULL,          -- Engineer ka Hashed password
    contact_number VARCHAR(20) NULL               -- Engineer ka contact number (optional)
);

ALTER TABLE office
ADD COLUMN site_photo_filenames TEXT NULL DEFAULT NULL,
ADD COLUMN site_document_filenames TEXT NULL DEFAULT NULL;
ALTER TABLE office
ADD COLUMN site_photo_filenames TEXT NULL DEFAULT NULL,
ADD COLUMN site_document_filenames TEXT NULL DEFAULT NULL;

