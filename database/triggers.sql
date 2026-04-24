-- ============================================================================
-- Metro Warehouse Management System - Triggers
-- ============================================================================

-- ============================================================================
-- TRIGGER: chk_picker_free
-- Business Rule: A picker can only work on ONE active order at a time
-- ============================================================================

DROP TRIGGER IF EXISTS chk_picker_free;

CREATE TRIGGER chk_picker_free
BEFORE INSERT ON Orders
FOR EACH ROW
WHEN (NEW.Picker_ID IS NOT NULL AND NEW.Status = 'Active')
BEGIN
    SELECT CASE
        WHEN (
            SELECT COUNT(*) 
            FROM Orders 
            WHERE Picker_ID = NEW.Picker_ID 
              AND Status = 'Active'
        ) > 0
        THEN RAISE(ABORT, 'ERROR: Picker already has an active order!')
    END;
END;

-- ============================================================================
-- Verification
-- ============================================================================
SELECT 'Trigger created successfully!' AS Status;