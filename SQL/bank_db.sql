DROP DATABASE IF EXISTS bank_db;
CREATE DATABASE bank_db;
USE bank_db;

-- Clients Table
CREATE TABLE clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    age INT NOT NULL,
    job VARCHAR(50),
    marital VARCHAR(20),
    education VARCHAR(50),
    default_status ENUM('yes', 'no') NOT NULL,
    balance INT NOT NULL,
    housing ENUM('yes', 'no') NOT NULL,
    loan ENUM('yes', 'no') NOT NULL
);

-- Contacts Table
CREATE TABLE contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    contact_type VARCHAR(20),
    day INT,
    month VARCHAR(20),
    duration INT,
    campaign INT,
    pdays INT,
    previous INT,
    poutcome VARCHAR(20),
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
);

-- Deposits Table
CREATE TABLE deposits (
    deposit_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    deposit ENUM('yes', 'no') NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
);

-- Balance Logs Table
CREATE TABLE balance_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    old_balance INT NOT NULL,
    new_balance INT NOT NULL,
    change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
);

-- Stored Procedure: Insert New Client
DELIMITER $$
CREATE PROCEDURE InsertClient (
    IN p_age INT, 
    IN p_job VARCHAR(50), 
    IN p_marital VARCHAR(20), 
    IN p_education VARCHAR(50),
    IN p_default ENUM('yes', 'no'), 
    IN p_balance INT, 
    IN p_housing ENUM('yes', 'no'), 
    IN p_loan ENUM('yes', 'no')
)
BEGIN
    INSERT INTO clients (age, job, marital, education, default_status, balance, housing, loan) 
    VALUES (p_age, p_job, p_marital, p_education, p_default, p_balance, p_housing, p_loan);
END $$

DELIMITER ;

-- Trigger: Log Balance Changes
DELIMITER $$
CREATE TRIGGER BalanceChangeTrigger 
BEFORE UPDATE ON clients
FOR EACH ROW
BEGIN
    IF OLD.balance <> NEW.balance THEN
        INSERT INTO balance_logs (client_id, old_balance, new_balance, change_time)
        VALUES (NEW.client_id, OLD.balance, NEW.balance, NOW());
    END IF;
END $$

DELIMITER ;

