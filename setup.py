"""
Database setup script
Run this once to create the warehouse database
"""

import sqlite3
import os

DB = "warehouse.db"


def run_sql_file(cursor, filepath):
    """Read and run SQL from a file"""
    with open(filepath, 'r') as f:
        sql = f.read()
        cursor.executescript(sql)


def main():
    print("\n" + "="*60)
    print("     WAREHOUSE DATABASE SETUP")
    print("="*60)
    
    # Check if database already exists
    if os.path.exists(DB):
        answer = input(f"\n{DB} already exists. Delete and recreate? (yes/no): ")
        if answer.lower() != 'yes':
            print("\nSetup cancelled\n")
            return
        os.remove(DB)
        print(f"✓ Deleted old database")
    
    # Create new database
    print(f"\n✓ Creating {DB}...")
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    try:
        # Create tables
        print("✓ Creating tables...")
        run_sql_file(cursor, "database/schema.sql")
        
        # Insert data
        print("✓ Adding sample data...")
        run_sql_file(cursor, "database/data.sql")
        
        # Add triggers
        print("✓ Creating triggers...")
        run_sql_file(cursor, "database/triggers.sql")
        
        conn.commit()
        
        # Show summary
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM Warehouse) AS Warehouses,
                (SELECT COUNT(*) FROM Store) AS Stores,
                (SELECT COUNT(*) FROM Order_Picker) AS Pickers,
                (SELECT COUNT(*) FROM Orders) AS Orders
        """)
        
        result = cursor.fetchone()
        
        print("\n" + "="*60)
        print("     SETUP COMPLETE!")
        print("="*60)
        print(f"\n  Warehouses: {result[0]}")
        print(f"  Stores: {result[1]}")
        print(f"  Workers: {result[2]}")
        print(f"  Orders: {result[3]}")
        print("\nYou can now run:")
        print("  python3 demos/1_trigger_demo.py")
        print("  python3 demos/2_warehouse_ai.py")
        print()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        conn.rollback()
        
    finally:
        conn.close()


if __name__ == "__main__":
    main()