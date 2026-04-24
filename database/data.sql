-- ============================================================================
-- Metro Warehouse Management System - Sample Data
-- ============================================================================

-- ============================================================================
-- Insert Warehouses
-- ============================================================================
INSERT INTO Warehouse VALUES (1, 'Metro Etobicoke', 'Toronto, ON', 'General', 20.0);
INSERT INTO Warehouse VALUES (2, 'Metro Etobicoke Frozen', 'Toronto, ON', 'Frozen', -20.0);

-- ============================================================================
-- Insert Stores
-- ============================================================================
INSERT INTO Store VALUES (1, 'Metro King Street', 'Toronto', 'ON');
INSERT INTO Store VALUES (2, 'Metro Brampton', 'Brampton', 'ON');
INSERT INTO Store VALUES (3, 'Metro Mississauga', 'Mississauga', 'ON');

-- ============================================================================
-- Insert Order Pickers (Workers)
-- ============================================================================
INSERT INTO Order_Picker VALUES (1, 'Sahil Sharma', 'sahil01', 1, 'Day', 'Active');
INSERT INTO Order_Picker VALUES (2, 'Ali Hassan', 'ali02', 1, 'Night', 'Active');
INSERT INTO Order_Picker VALUES (3, 'Priya Singh', 'priya03', 2, 'Day', 'Active');
INSERT INTO Order_Picker VALUES (4, 'John Smith', 'john04', 1, 'Day', 'Active');
INSERT INTO Order_Picker VALUES (5, 'Maria Garcia', 'maria05', 1, 'Night', 'Active');

-- ============================================================================
-- Insert Products
-- ============================================================================
INSERT INTO Product VALUES (1, 'Orange Juice 2L', 'OJ-2L', 2.1, 1);
INSERT INTO Product VALUES (2, 'Frozen Fries 1kg', 'FF-1KG', 1.0, 2);
INSERT INTO Product VALUES (3, 'Milk 4L', 'MILK-4L', 4.2, 1);
INSERT INTO Product VALUES (4, 'Water 24pk', 'WAT-24', 9.8, 1);
INSERT INTO Product VALUES (5, 'Frozen Pizza', 'PIZ-FRZ', 0.85, 2);

-- ============================================================================
-- Insert Locations
-- ============================================================================
INSERT INTO Location VALUES (1, 1, 65, '365', '64', 1, 120);
INSERT INTO Location VALUES (2, 1, 42, '420', '21', 3, 80);
INSERT INTO Location VALUES (3, 1, 18, '180', '09', 4, 200);
INSERT INTO Location VALUES (4, 2, 12, '120', '55', 2, 60);
INSERT INTO Location VALUES (5, 2, 8, '080', '33', 5, 45);

-- ============================================================================
-- Insert Orders
-- ============================================================================
INSERT INTO Orders VALUES (1001, 1, 1, 48, 320.5, 'Completed', 12, date('now'));
INSERT INTO Orders VALUES (1002, 2, 1, 30, 150.0, 'Completed', 8, date('now'));
INSERT INTO Orders VALUES (1003, 3, 2, 55, 410.2, 'Active', 15, date('now'));
INSERT INTO Orders VALUES (1004, 1, 3, 20, 95.0, 'Pending', 6, date('now'));
INSERT INTO Orders VALUES (1005, 2, 4, 25, 120.0, 'Pending', 7, date('now'));
INSERT INTO Orders VALUES (1006, 3, NULL, 40, 200.0, 'Pending', 10, date('now'));

-- ============================================================================
-- Insert Order Line Items
-- ============================================================================
INSERT INTO Order_Line_Item VALUES (1, 1001, 1, 1, 12, 12);
INSERT INTO Order_Line_Item VALUES (2, 1001, 3, 2, 20, 20);
INSERT INTO Order_Line_Item VALUES (3, 1002, 4, 3, 16, 16);
INSERT INTO Order_Line_Item VALUES (4, 1003, 2, 4, 25, 18);
INSERT INTO Order_Line_Item VALUES (5, 1003, 5, 5, 30, 30);

-- ============================================================================
-- Insert Damaged Products
-- ============================================================================
INSERT INTO Damaged_Product VALUES (1, 1, 1, 3, 'Crushed by pallet jack', date('now'));
INSERT INTO Damaged_Product VALUES (2, 4, 2, 5, 'Dropped from shelf', date('now'));
INSERT INTO Damaged_Product VALUES (3, 2, 3, 2, 'Freezer bag torn', date('now'));

-- ============================================================================
-- Insert Equipment
-- ============================================================================
INSERT INTO Equipment VALUES (1, 'Pallet Jack', 1, 'In Use');
INSERT INTO Equipment VALUES (2, 'Pallet Jack', 1, 'In Use');
INSERT INTO Equipment VALUES (3, 'Forklift', 1, 'Available');
INSERT INTO Equipment VALUES (4, 'Forklift', 2, 'Available');
INSERT INTO Equipment VALUES (5, 'Pallet Jack', 1, 'Available');

-- ============================================================================
-- Insert Workforce Plan
-- ============================================================================
INSERT INTO Workforce_Plan VALUES (1, 1, date('now'), 'Day', 3, 2, 0);
INSERT INTO Workforce_Plan VALUES (2, 1, date('now'), 'Night', 2, 2, 1);

-- ============================================================================
-- Verification
-- ============================================================================
SELECT 'Data inserted successfully!' AS Status;