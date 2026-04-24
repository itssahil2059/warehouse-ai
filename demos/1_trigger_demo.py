"""
Warehouse Trigger Demo - Shows how database prevents bad assignments
"""

import sqlite3
import os

# Make sure database exists
if not os.path.exists('warehouse.db'):
    print("\nError: warehouse.db not found!")
    print("Run the setup first to create the database")
    exit(1)


def show_header():
    """Print demo title"""
    print("\n" + "="*60)
    print("     WAREHOUSE TRIGGER DEMO")
    print("="*60)
    print("\nRule: One picker can only work on ONE order at a time")
    print("Let's see the trigger in action!\n")


def show_active_orders():
    """Show which orders are currently being picked"""
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    print("-"*60)
    print("Current Active Orders:")
    print("-"*60)
    
    # Get active orders with picker names
    cursor.execute("""
        SELECT o.Order_ID, p.Name, s.Store_Name, o.Status 
        FROM Orders o
        JOIN Order_Picker p ON o.Picker_ID = p.Picker_ID
        JOIN Store s ON o.Store_ID = s.Store_ID
        WHERE o.Status = 'Active'
    """)
    
    results = cursor.fetchall()
    
    if results:
        print(f"\nOrder    Picker              Store                 Status")
        print("-"*60)
        for order_id, picker, store, status in results:
            print(f"{order_id:<8} {picker:<20} {store:<20} {status}")
        print()
    else:
        print("\nNo active orders right now\n")
    
    conn.close()
    return results


def try_double_assignment():
    """Try to assign 2 orders to same picker - should fail!"""
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    print("-"*60)
    print("Testing: Assigning another order to Ali Hassan")
    print("-"*60)
    print("\nAli already has order 1003 active")
    print("Let's try to give him order 1010 too...")
    print("\nSQL: INSERT INTO Orders VALUES (1010, 2, 2, 25, 120, 'Active', 8, date('now'))")
    print()
    
    try:
        # Try to assign order to Ali who already has an active order
        cursor.execute("""
            INSERT INTO Orders VALUES 
            (1010, 2, 2, 25, 120.0, 'Active', 8, date('now'))
        """)
        conn.commit()
        print("✓ Order assigned")
        
    except sqlite3.IntegrityError as e:
        # The trigger blocked it!
        print("✗ BLOCKED BY TRIGGER!")
        print(f"\nError: {str(e)}")
        print("\n✓ Good! The trigger stopped the invalid assignment")
        print("✓ Data is safe - one picker, one order\n")
        
    conn.close()


def try_valid_assignment():
    """Assign order to a free picker - should work!"""
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    print("-"*60)
    print("Testing: Assigning order to John Smith")
    print("-"*60)
    print("\nJohn has no active orders")
    print("This should work fine...")
    print("\nSQL: INSERT INTO Orders VALUES (1011, 1, 4, 15, 75, 'Active', 5, date('now'))")
    print()
    
    try:
        # Clean up if exists
        cursor.execute("DELETE FROM Orders WHERE Order_ID = 1011")
        
        # Assign to John who is free
        cursor.execute("""
            INSERT INTO Orders VALUES 
            (1011, 1, 4, 15, 75.0, 'Active', 5, date('now'))
        """)
        conn.commit()
        print("✓ SUCCESS! Order assigned to John")
        print("✓ Trigger allowed it because John was free\n")
        
        # Clean up
        cursor.execute("DELETE FROM Orders WHERE Order_ID = 1011")
        conn.commit()
        
    except sqlite3.IntegrityError as e:
        print(f"✗ Error: {str(e)}\n")
        
    conn.close()


def show_summary():
    """Print what we learned"""
    print("="*60)
    print("     DEMO COMPLETE")
    print("="*60)
    print("\nWhat we learned:")
    print("✓ Triggers automatically enforce business rules")
    print("✓ Database protects data integrity")
    print("✓ No manual checking needed\n")
    print("This is traditional database programming")
    print("Next: We'll add AI on top of this!\n")


# Main demo
def main():
    show_header()
    
    # Show current state
    active = show_active_orders()
    
    if not active:
        print("No active orders to demo with")
        return
    
    # Wait for user
    input("Press Enter to try invalid assignment...")
    
    # Try to break the rule (will fail)
    try_double_assignment()
    
    # Wait for user
    input("Press Enter to try valid assignment...")
    
    # Try valid assignment (will work)
    try_valid_assignment()
    
    # Show what we learned
    show_summary()


if __name__ == "__main__":
    main()