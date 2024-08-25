-- 設置資料庫
USE master;
GO

-- 創建一個新的資料庫
CREATE DATABASE my_database;
GO

-- 使用新建立的資料庫
USE my_database;
GO

-- 創建表格
CREATE TABLE exchange_rates (
    id INT IDENTITY(1,1) PRIMARY KEY,
    usd_rate DECIMAL(18, 6) NOT NULL,
    jpy_rate DECIMAL(18, 6) NOT NULL,
    gbp_rate DECIMAL(18, 6) NOT NULL,
    aud_rate DECIMAL(18, 6) NOT NULL,
    timestamp DATETIME NOT NULL
);
GO

-- 插入一些初始數據
INSERT INTO exchange_rates (usd_rate, jpy_rate, gbp_rate, aud_rate, timestamp)
VALUES
    (0.031, 4.5, 0.022, 0.048, '2024-08-23T12:56:00');
GO
