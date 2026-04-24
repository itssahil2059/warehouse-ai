-- ============================================================================
-- Metro Warehouse Management System - Database Schema
-- SQLite Version
-- ============================================================================

-- Drop existing tables if they exist
DROP TABLE IF EXISTS Workforce_Plan;
DROP TABLE IF EXISTS Equipment;
DROP TABLE IF EXISTS Damaged_Product;
DROP TABLE IF EXISTS Order_Line_Item;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Order_Picker;
DROP TABLE IF EXISTS Store;
DROP TABLE IF EXISTS Warehouse;

-- ============================================================================
-- TABLE 1: Warehouse
-- ============================================================================
CREATE TABLE Warehouse (
    Warehouse_ID  INTEGER PRIMARY KEY,
    Name          TEXT NOT NULL,
    Location      TEXT,
    Type          TEXT CHECK (Type IN ('General','Frozen')),
    Temperature_C REAL
);

-- ============================================================================
-- TABLE 2: Store
-- ============================================================================
CREATE TABLE Store (
    Store_ID    INTEGER PRIMARY KEY,
    Store_Name  TEXT NOT NULL,
    City        TEXT,
    Province    TEXT
);

-- ============================================================================
-- TABLE 3: Order_Picker (Workers)
-- ============================================================================
CREATE TABLE Order_Picker (
    Picker_ID    INTEGER PRIMARY KEY,
    Name         TEXT NOT NULL,
    Login_ID     TEXT UNIQUE NOT NULL,
    Warehouse_ID INTEGER,
    Shift        TEXT CHECK (Shift IN ('Day','Night')),
    Status       TEXT DEFAULT 'Active',
    FOREIGN KEY (Warehouse_ID) REFERENCES Warehouse(Warehouse_ID)
);

-- ============================================================================
-- TABLE 4: Product
-- ============================================================================
CREATE TABLE Product (
    Product_ID   INTEGER PRIMARY KEY,
    Name         TEXT NOT NULL,
    SKU          TEXT,
    Weight_kg    REAL,
    Warehouse_ID INTEGER,
    FOREIGN KEY (Warehouse_ID) REFERENCES Warehouse(Warehouse_ID)
);

-- ============================================================================
-- TABLE 5: Location (Aisle locations)
-- ============================================================================
CREATE TABLE Location (
    Location_ID   INTEGER PRIMARY KEY,
    Warehouse_ID  INTEGER,
    Aisle_Number  INTEGER NOT NULL,
    Location_Code TEXT,
    Confirm_Code  TEXT,
    Product_ID    INTEGER,
    Stock_Qty     INTEGER DEFAULT 0,
    FOREIGN KEY (Warehouse_ID) REFERENCES Warehouse(Warehouse_ID),
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
);

-- ============================================================================
-- TABLE 6: Orders
-- ============================================================================
CREATE TABLE Orders (
    Order_ID        INTEGER PRIMARY KEY,
    Store_ID        INTEGER,
    Picker_ID       INTEGER,
    Total_Items     INTEGER,
    Total_Weight_kg REAL,
    Status          TEXT DEFAULT 'Pending' CHECK (Status IN ('Pending','Active','Completed')),
    Assigned_Door   INTEGER,
    Created_At      TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Store_ID) REFERENCES Store(Store_ID),
    FOREIGN KEY (Picker_ID) REFERENCES Order_Picker(Picker_ID)
);

-- ============================================================================
-- TABLE 7: Order_Line_Item
-- ============================================================================
CREATE TABLE Order_Line_Item (
    Line_ID      INTEGER PRIMARY KEY,
    Order_ID     INTEGER,
    Product_ID   INTEGER,
    Location_ID  INTEGER,
    Qty_Required INTEGER NOT NULL,
    Qty_Picked   INTEGER DEFAULT 0,
    FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID),
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
);

-- ============================================================================
-- TABLE 8: Damaged_Product
-- ============================================================================
CREATE TABLE Damaged_Product (
    Damage_ID   INTEGER PRIMARY KEY,
    Product_ID  INTEGER,
    Picker_ID   INTEGER,
    Qty_Damaged INTEGER,
    Reason      TEXT,
    Reported_At TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID),
    FOREIGN KEY (Picker_ID) REFERENCES Order_Picker(Picker_ID)
);

-- ============================================================================
-- TABLE 9: Equipment
-- ============================================================================
CREATE TABLE Equipment (
    Equipment_ID INTEGER PRIMARY KEY,
    Type         TEXT CHECK (Type IN ('Pallet Jack','Forklift')),
    Warehouse_ID INTEGER,
    Status       TEXT DEFAULT 'Available',
    FOREIGN KEY (Warehouse_ID) REFERENCES Warehouse(Warehouse_ID)
);

-- ============================================================================
-- TABLE 10: Workforce_Plan
-- ============================================================================
CREATE TABLE Workforce_Plan (
    Plan_ID           INTEGER PRIMARY KEY,
    Warehouse_ID      INTEGER,
    Shift_Date        TEXT,
    Shift_Type        TEXT,
    Pending_Orders    INTEGER DEFAULT 0,
    Workers_Needed    INTEGER DEFAULT 0,
    Overtime_Flag     INTEGER DEFAULT 0,
    FOREIGN KEY (Warehouse_ID) REFERENCES Warehouse(Warehouse_ID)
);

-- ============================================================================
-- Verification
-- ============================================================================
SELECT 'Schema created successfully - 10 tables ready!' AS Status;