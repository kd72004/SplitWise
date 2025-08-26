-- Database setup for Splitwise application
-- Run this script in PostgreSQL to create the required tables

CREATE DATABASE IF NOT EXISTS splitwise_db;

\c splitwise_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(32) PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Groups table
CREATE TABLE IF NOT EXISTS groups (
    group_id VARCHAR(32) PRIMARY KEY,
    group_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Group members table
CREATE TABLE IF NOT EXISTS group_members (
    group_id VARCHAR(32) REFERENCES groups(group_id) ON DELETE CASCADE,
    user_id VARCHAR(32) REFERENCES users(user_id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, user_id)
);

-- Expenses table
CREATE TABLE IF NOT EXISTS expense (
    expense_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    paid_by VARCHAR(32) REFERENCES users(user_id),
    total_amount DECIMAL(10,2) NOT NULL,
    split_type VARCHAR(20) NOT NULL CHECK (split_type IN ('equal', 'unequal', 'percentage')),
    group_id VARCHAR(32) REFERENCES groups(group_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Expense shares table
CREATE TABLE IF NOT EXISTS expense_share (
    expense_id VARCHAR(32) REFERENCES expense(expense_id) ON DELETE CASCADE,
    borrower_id VARCHAR(32) REFERENCES users(user_id),
    paid_by_id VARCHAR(32) REFERENCES users(user_id),
    amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (expense_id, borrower_id)
);

-- Balance sheet table for settlements
CREATE TABLE IF NOT EXISTS balance_sheet (
    id SERIAL PRIMARY KEY,
    group_id VARCHAR(32) REFERENCES groups(group_id) ON DELETE CASCADE,
    borrower_id VARCHAR(32) REFERENCES users(user_id),
    receiver_id VARCHAR(32) REFERENCES users(user_id),
    amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_group_members_user ON group_members(user_id);
CREATE INDEX IF NOT EXISTS idx_expense_group ON expense(group_id);
CREATE INDEX IF NOT EXISTS idx_expense_share_borrower ON expense_share(borrower_id);
CREATE INDEX IF NOT EXISTS idx_balance_sheet_group ON balance_sheet(group_id);