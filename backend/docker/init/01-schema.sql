-- ============================================
-- Real Estate Projects App - Database Schema
-- ============================================

CREATE DATABASE IF NOT EXISTS real_estate_app
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE real_estate_app;

-- ============================================
-- 1. Users
-- ============================================

CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50) NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),

    INDEX idx_user_email (email),
    INDEX idx_user_role (role),
    INDEX idx_user_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 2. Real Estate Companies
-- ============================================

CREATE TABLE real_estate_companies (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted_at DATETIME(6) NULL,

    created_by BIGINT NULL,
    updated_by BIGINT NULL,
    deleted_by BIGINT NULL,

    name VARCHAR(255) NOT NULL,
    legal_name VARCHAR(255) NULL,
    tax_id VARCHAR(20) NULL UNIQUE,

    email VARCHAR(255) NULL,
    phone VARCHAR(20) NULL,
    website VARCHAR(255) NULL,

    address TEXT NULL,
    city VARCHAR(100) NULL,
    region VARCHAR(100) NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    FOREIGN KEY (deleted_by) REFERENCES users(id),

    INDEX idx_company_name (name),
    INDEX idx_company_tax_id (tax_id),
    INDEX idx_company_active (is_active),
    INDEX idx_company_city (city),
    INDEX idx_company_created_by (created_by),
    INDEX idx_company_updated_by (updated_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 3. Projects
-- ============================================

CREATE TABLE projects (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted_at DATETIME(6) NULL,

    created_by BIGINT NULL,
    updated_by BIGINT NULL,
    deleted_by BIGINT NULL,

    company_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description JSON NULL,

    executive VARCHAR(255) NULL,
    executive_email VARCHAR(255) NULL,

    city VARCHAR(100) NULL,
    region VARCHAR(100) NULL,
    address TEXT NULL,
    street_number VARCHAR(20) NULL,
    commune VARCHAR(100) NULL,
    country VARCHAR(100) NULL,
    postal_code VARCHAR(20) NULL,
    url_google_maps VARCHAR(500) NULL,
    latitude VARCHAR(50) NULL,
    longitude VARCHAR(50) NULL,

    phone VARCHAR(20) NULL,
    website VARCHAR(255) NULL,

    price_from DECIMAL(15,2) NULL,
    price_to DECIMAL(15,2) NULL,
    unique_price DECIMAL(15,2) NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'CLP',

    total_units INT NULL,
    available_units INT NULL,

    type VARCHAR(100) NULL,
    delivery_type VARCHAR(100) NULL,
    state VARCHAR(50) NOT NULL DEFAULT 'development',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    is_promo BOOLEAN NOT NULL DEFAULT FALSE,
    is_hot BOOLEAN NOT NULL DEFAULT FALSE,

    start_date DATE NULL,
    delivery_date DATE NULL,
    delivery_end_date DATE NULL,
    launch_date DATE NULL,

    FOREIGN KEY (company_id) REFERENCES real_estate_companies(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    FOREIGN KEY (deleted_by) REFERENCES users(id),

    INDEX idx_project_name (name),
    INDEX idx_project_city (city),
    INDEX idx_project_commune (commune),
    INDEX idx_project_state (state),
    INDEX idx_project_active (is_active),
    INDEX idx_project_company (company_id),
    INDEX idx_project_created_by (created_by),
    INDEX idx_project_updated_by (updated_by),
    INDEX idx_project_executive (executive),
    INDEX idx_project_executive_email (executive_email),
    INDEX idx_project_street_number (street_number),
    INDEX idx_project_country (country),
    INDEX idx_project_launch_date (launch_date),
    INDEX idx_project_delivery_end_date (delivery_end_date),
    INDEX idx_project_type (type),
    INDEX idx_project_delivery_type (delivery_type),
    INDEX idx_project_unique_price (unique_price),
    INDEX idx_project_is_promo (is_promo),
    INDEX idx_project_is_hot (is_hot)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 4. Project Stock
-- ============================================

CREATE TABLE project_stock (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted_at DATETIME(6) NULL,

    created_by BIGINT NULL,
    updated_by BIGINT NULL,
    deleted_by BIGINT NULL,

    project_id BIGINT NOT NULL,
    unit_number VARCHAR(50) NOT NULL,
    unit_type VARCHAR(50) NOT NULL,
    description TEXT NULL,

    bedrooms INT NOT NULL DEFAULT 0,
    bathrooms INT NOT NULL DEFAULT 0,
    orientation VARCHAR(50) NULL,
    total_area DECIMAL(8,2) NULL,

    floor INT NULL,
    building VARCHAR(50) NULL,

    parkings VARCHAR(50) NULL,
    storages VARCHAR(50) NULL,
    has_parking BOOLEAN NOT NULL DEFAULT FALSE,
    has_storage BOOLEAN NOT NULL DEFAULT FALSE,

    surface_internal DECIMAL(8,2) NULL,
    surface_terrace DECIMAL(8,2) NULL,
    surface_garden DECIMAL(8,2) NULL,
    surface_pantry DECIMAL(8,2) NULL,
    surface_multiuse_assignable DECIMAL(8,2) NULL,
    surface_util DECIMAL(8,2) NULL,
    surface_terrain DECIMAL(8,2) NULL,
    surface_others DECIMAL(8,2) NULL,

    currency VARCHAR(10) NOT NULL DEFAULT 'CLP',
    value_base DECIMAL(15,2) NULL,
    value_uf DECIMAL(10,2) NULL,
    value_list DECIMAL(15,2) NULL,
    value_discount DECIMAL(15,2) NULL,
    value_enabled DECIMAL(15,2) NULL,
    value_promotion DECIMAL(15,2) NULL,
    value_bonus DECIMAL(15,2) NULL,
    value_parking DECIMAL(15,2) NULL,
    value_storage DECIMAL(15,2) NULL,

    status VARCHAR(50) NOT NULL DEFAULT 'available',

    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    FOREIGN KEY (deleted_by) REFERENCES users(id),

    UNIQUE INDEX idx_stock_unique_unit (project_id, unit_number),
    INDEX idx_stock_project (project_id),
    INDEX idx_stock_status (status),
    INDEX idx_stock_bedrooms (bedrooms),
    INDEX idx_stock_bathrooms (bathrooms),
    INDEX idx_stock_orientation (orientation),
    INDEX idx_stock_currency (currency),
    INDEX idx_stock_price (value_base),
    INDEX idx_stock_price_list (value_list),
    INDEX idx_stock_floor (floor),
    INDEX idx_stock_building (building),
    INDEX idx_stock_created_by (created_by),
    INDEX idx_stock_updated_by (updated_by),
    INDEX idx_stock_value_parking (value_parking),
    INDEX idx_stock_value_storage (value_storage)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 5. Legal Users
-- ============================================

CREATE TABLE legal_users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted_at DATETIME(6) NULL,

    created_by BIGINT NULL,
    updated_by BIGINT NULL,
    deleted_by BIGINT NULL,

    project_id BIGINT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    tax_id VARCHAR(20) NULL,

    email VARCHAR(255) NULL,
    phone VARCHAR(20) NULL,

    position VARCHAR(100) NULL,
    company VARCHAR(255) NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    FOREIGN KEY (deleted_by) REFERENCES users(id),

    INDEX idx_legal_user_project (project_id),
    INDEX idx_legal_user_active (is_active),
    INDEX idx_legal_user_primary (is_primary),
    INDEX idx_legal_user_name (first_name, last_name),
    INDEX idx_legal_user_created_by (created_by),
    INDEX idx_legal_user_updated_by (updated_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 6. Project Images
-- ============================================

CREATE TABLE project_images (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted_at DATETIME(6) NULL,

    created_by BIGINT NULL,
    updated_by BIGINT NULL,
    deleted_by BIGINT NULL,

    project_id BIGINT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    url VARCHAR(500) NOT NULL,

    alt_text VARCHAR(255) NULL,
    image_type VARCHAR(50) NOT NULL DEFAULT 'general',

    is_featured BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    display_order INT NOT NULL DEFAULT 0,

    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    FOREIGN KEY (deleted_by) REFERENCES users(id),

    INDEX idx_project_image_project (project_id),
    INDEX idx_project_image_type (image_type),
    INDEX idx_project_image_featured (is_featured),
    INDEX idx_project_image_order (project_id, display_order),
    INDEX idx_project_image_created_by (created_by),
    INDEX idx_project_image_updated_by (updated_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 7. Project Documents
-- ============================================

CREATE TABLE project_documents (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted_at DATETIME(6) NULL,

    created_by BIGINT NULL,
    updated_by BIGINT NULL,
    deleted_by BIGINT NULL,

    project_id BIGINT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    url VARCHAR(500) NOT NULL,

    document_type VARCHAR(50) NOT NULL DEFAULT 'general',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    FOREIGN KEY (deleted_by) REFERENCES users(id),

    INDEX idx_project_document_project (project_id),
    INDEX idx_project_document_type (document_type),
    INDEX idx_project_document_active (is_active),
    INDEX idx_project_document_created_by (created_by),
    INDEX idx_project_document_updated_by (updated_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 8. Project Commercial
-- ============================================

CREATE TABLE project_commercial (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted_at DATETIME(6) NULL,

    created_by BIGINT NULL,
    updated_by BIGINT NULL,
    deleted_by BIGINT NULL,

    project_id BIGINT NOT NULL UNIQUE,

    -- Postventa
    after_sales_email VARCHAR(255) NULL,
    after_sales_executive VARCHAR(255) NULL,
    after_sales_phone VARCHAR(20) NULL,

    -- Financiera
    finances_insurance_company VARCHAR(255) NULL,
    finances_insurance_policy VARCHAR(100) NULL,
    finances_insured_value VARCHAR(50) NULL,
    finances_insured_value_util VARCHAR(50) NULL,
    finances_benefit VARCHAR(50) NULL,
    finances_annual_rate DECIMAL(5,2) NULL,
    finances_credit_rate DECIMAL(5,2) NULL,

    -- Comercial variable
    down_payment_bonus DECIMAL(15,2) NULL,
    reservation DECIMAL(15,2) NULL,
    pre_approval VARCHAR(50) NULL,
    installments DECIMAL(15,2) NULL,
    balloon_payment VARCHAR(255) NULL,
    annual_capital_gain DECIMAL(5,2) NULL,
    construction_capital_gain DECIMAL(5,2) NULL,
    vacancy DECIMAL(5,2) NULL,
    additional_information TEXT NULL,
    initial_payment DECIMAL(5,2) NULL,
    big_down_payment DECIMAL(15,2) NULL,
    notes_rent JSON NULL,

    -- JSON flexibles
    social_networks JSON NULL,
    payment_plan_conditions JSON NULL,
    promotions_benefits JSON NULL,
    frequently_asked_questions JSON NULL,

    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    FOREIGN KEY (deleted_by) REFERENCES users(id),

    INDEX idx_project_commercial_project (project_id),
    INDEX idx_project_commercial_after_sales (after_sales_executive),
    INDEX idx_project_commercial_initial_payment (initial_payment),
    INDEX idx_project_commercial_big_down_payment (big_down_payment),
    INDEX idx_project_commercial_created_by (created_by),
    INDEX idx_project_commercial_updated_by (updated_by),
    INDEX idx_project_commercial_finances_annual_rate (finances_annual_rate),
    INDEX idx_project_commercial_finances_credit_rate (finances_credit_rate),
    INDEX idx_project_commercial_down_payment_bonus (down_payment_bonus),
    INDEX idx_project_commercial_reservation (reservation),
    INDEX idx_project_commercial_pre_approval (pre_approval),
    INDEX idx_project_commercial_installments (installments),
    INDEX idx_project_commercial_annual_capital_gain (annual_capital_gain),
    INDEX idx_project_commercial_construction_capital_gain (construction_capital_gain),
    INDEX idx_project_commercial_vacancy (vacancy)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed: usuario admin por defecto (password: admin123)
INSERT INTO users (full_name, email, password_hash, role, is_active)
VALUES ('Administrador', 'admin@realestate.com', '$2b$12$lOrWEsKi9S1IF4xjDn5rL.D4QHEDgIkeEjuDDKIaxkv7uWNUJADFO', 'admin', TRUE)
ON DUPLICATE KEY UPDATE full_name = full_name;
