"""
Warehouse database query functions
The AI calls these to get data
"""

import sqlite3

DB = "warehouse.db"


# Get workers by shift
def get_worker_availability(shift):
    """Check how many workers are free"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    if shift == "All":
        query = "SELECT Name, Shift, Status FROM Order_Picker WHERE Status = 'Active' ORDER BY Shift, Name"
        cursor.execute(query)
    else:
        query = "SELECT Name, Shift, Status FROM Order_Picker WHERE Status = 'Active' AND Shift = ? ORDER BY Name"
        cursor.execute(query, (shift,))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return f"No active workers for {shift} shift"
    
    # Format the answer
    output = f"Workers available ({shift} shift):\n"
    output += f"Total: {len(results)}\n\n"
    for name, shift_type, status in results:
        output += f"• {name} - {shift_type} shift\n"
    
    return output


# Get today's workload
def get_daily_load(shift="All"):
    """Check total orders and items for today"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    if shift == "All":
        query = """
            SELECT COUNT(*), SUM(Total_Items), SUM(Total_Weight_kg)
            FROM Orders
            WHERE date(Created_At) = date('now')
            AND Status IN ('Pending', 'Active')
        """
        cursor.execute(query)
    else:
        query = """
            SELECT COUNT(*), SUM(o.Total_Items), SUM(o.Total_Weight_kg)
            FROM Orders o
            LEFT JOIN Order_Picker p ON o.Picker_ID = p.Picker_ID
            WHERE date(o.Created_At) = date('now')
            AND o.Status IN ('Pending', 'Active')
            AND (p.Shift = ? OR o.Picker_ID IS NULL)
        """
        cursor.execute(query, (shift,))
    
    result = cursor.fetchone()
    conn.close()
    
    orders = result[0] or 0
    items = result[1] or 0
    weight = result[2] or 0.0
    
    output = f"Today's Load ({shift}):\n"
    output += f"• Orders: {orders}\n"
    output += f"• Items to pick: {items}\n"
    output += f"• Total weight: {weight:.1f} kg\n"
    
    return output


# Get pending orders
def get_pending_orders():
    """Show orders waiting to be picked"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    query = """
        SELECT o.Order_ID, s.Store_Name, o.Total_Items, o.Total_Weight_kg, o.Assigned_Door
        FROM Orders o
        JOIN Store s ON o.Store_ID = s.Store_ID
        WHERE o.Status = 'Pending'
        ORDER BY o.Order_ID
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return "No pending orders"
    
    output = f"Pending Orders ({len(results)} total):\n\n"
    for order_id, store, items, weight, door in results:
        output += f"Order #{order_id}:\n"
        output += f"  Store: {store}\n"
        output += f"  Items: {items}\n"
        output += f"  Weight: {weight:.1f} kg\n"
        output += f"  Door: {door}\n\n"
    
    return output


# Get active orders being picked
def get_active_orders():
    """Show orders currently being picked"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    query = """
        SELECT o.Order_ID, p.Name, s.Store_Name, o.Total_Items, o.Total_Weight_kg
        FROM Orders o
        JOIN Order_Picker p ON o.Picker_ID = p.Picker_ID
        JOIN Store s ON o.Store_ID = s.Store_ID
        WHERE o.Status = 'Active'
        ORDER BY o.Order_ID
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return "No active orders right now"
    
    output = f"Active Orders ({len(results)} total):\n\n"
    for order_id, picker, store, items, weight in results:
        output += f"Order #{order_id}:\n"
        output += f"  Picker: {picker}\n"
        output += f"  Store: {store}\n"
        output += f"  Items: {items}\n"
        output += f"  Weight: {weight:.1f} kg\n\n"
    
    return output


# Check if overtime needed
def check_overtime_needed():
    """Check workforce planning for overtime"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    query = """
        SELECT Shift_Type, Pending_Orders, Workers_Needed, Overtime_Flag
        FROM Workforce_Plan
        WHERE date(Shift_Date) = date('now')
        ORDER BY Shift_Type
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return "No workforce data for today"
    
    output = "Overtime Check:\n\n"
    for shift, pending, workers, overtime in results:
        output += f"{shift} Shift:\n"
        output += f"  Pending orders: {pending}\n"
        output += f"  Workers needed: {workers}\n"
        if overtime == 1:
            output += f"  ⚠️ OVERTIME NEEDED\n\n"
        else:
            output += f"  ✓ Staffing OK\n\n"
    
    return output


# Get top performers
def get_top_pickers(limit=5):
    """Show best pickers by items picked"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    query = """
        SELECT p.Name, COUNT(o.Order_ID), SUM(o.Total_Items)
        FROM Order_Picker p
        JOIN Orders o ON p.Picker_ID = o.Picker_ID
        WHERE o.Status = 'Completed'
        GROUP BY p.Name
        ORDER BY SUM(o.Total_Items) DESC
        LIMIT ?
    """
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return "No performance data yet"
    
    output = f"Top {limit} Pickers:\n\n"
    for rank, (name, orders, items) in enumerate(results, 1):
        output += f"{rank}. {name}\n"
        output += f"   Orders: {orders}\n"
        output += f"   Items: {items}\n\n"
    
    return output


# Get equipment status
def get_equipment_status(warehouse_id=None):
    """Check what equipment is available"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    if warehouse_id:
        query = """
            SELECT Type, Status, COUNT(*)
            FROM Equipment
            WHERE Warehouse_ID = ?
            GROUP BY Type, Status
        """
        cursor.execute(query, (warehouse_id,))
    else:
        query = """
            SELECT Type, Status, COUNT(*)
            FROM Equipment
            GROUP BY Type, Status
        """
        cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return "No equipment found"
    
    output = "Equipment Status:\n\n"
    for equip_type, status, count in results:
        output += f"{equip_type}: {count} {status}\n"
    
    return output


# Get low stock items
def get_low_stock_items(threshold=100):
    """Find products running low"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    query = """
        SELECT p.Name, l.Aisle_Number, l.Stock_Qty
        FROM Location l
        JOIN Product p ON l.Product_ID = p.Product_ID
        WHERE l.Stock_Qty < ?
        ORDER BY l.Stock_Qty ASC
    """
    cursor.execute(query, (threshold,))
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return f"No items below {threshold} units"
    
    output = f"⚠️ Low Stock (< {threshold}):\n\n"
    for product, aisle, qty in results:
        output += f"• {product}\n"
        output += f"  Aisle {aisle} - Only {qty} left\n\n"
    
    return output


# Get damage report
def get_damage_report():
    """Show damaged products"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    query = """
        SELECT pr.Name, pk.Name, d.Qty_Damaged, d.Reason, d.Reported_At
        FROM Damaged_Product d
        JOIN Product pr ON d.Product_ID = pr.Product_ID
        JOIN Order_Picker pk ON d.Picker_ID = pk.Picker_ID
        ORDER BY d.Reported_At DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return "No damage reports"
    
    output = f"Damage Report ({len(results)} incidents):\n\n"
    for product, reporter, qty, reason, date in results:
        output += f"• {product} - {qty} units\n"
        output += f"  Reported by: {reporter}\n"
        output += f"  Reason: {reason}\n"
        output += f"  Date: {date}\n\n"
    
    return output


# Main dispatcher - routes tool calls to functions
def execute_tool(tool_name, tool_input):
    """Run the right function based on tool name"""
    
    if tool_name == "get_worker_availability":
        return get_worker_availability(tool_input.get("shift", "All"))
    
    elif tool_name == "get_daily_load":
        return get_daily_load(tool_input.get("shift", "All"))
    
    elif tool_name == "get_pending_orders":
        return get_pending_orders()
    
    elif tool_name == "get_active_orders":
        return get_active_orders()
    
    elif tool_name == "check_overtime_needed":
        return check_overtime_needed()
    
    elif tool_name == "get_top_pickers":
        return get_top_pickers(tool_input.get("limit", 5))
    
    elif tool_name == "get_equipment_status":
        return get_equipment_status(tool_input.get("warehouse_id"))
    
    elif tool_name == "get_low_stock_items":
        return get_low_stock_items(tool_input.get("threshold", 100))
    
    elif tool_name == "get_damage_report":
        return get_damage_report()
    
    else:
        return f"Unknown tool: {tool_name}"