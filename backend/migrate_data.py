"""
Migration script to transfer data from SQLite to PostgreSQL
"""
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from app.database import SessionLocal, engine, Base, settings
from app import models

print(f"PostgreSQL URL: {settings.DATABASE_URL.split('@')[0].split(':')[0]}:***@{settings.DATABASE_URL.split('@')[1]}")


def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    
    # Path to SQLite database
    sqlite_db_path = Path(__file__).parent.parent / "data" / "vacaciones.db"
    
    if not sqlite_db_path.exists():
        print(f"SQLite database not found at {sqlite_db_path}")
        print("No data to migrate.")
        return
    
    print(f"Connecting to SQLite database: {sqlite_db_path}")
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_cursor = sqlite_conn.cursor()
    
    # Create PostgreSQL tables
    print("Creating PostgreSQL tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create PostgreSQL session
    db = SessionLocal()
    
    try:
        # Migrate employees
        print("\nMigrating employees...")
        sqlite_cursor.execute("SELECT * FROM employees")
        employees = sqlite_cursor.fetchall()
        
        employee_id_map = {}  # Map old IDs to new IDs
        
        for emp_row in employees:
            emp = models.Employee(
                employee_number=emp_row[1],
                full_name=emp_row[2],
                entry_date=datetime.strptime(emp_row[3], '%Y-%m-%d').date(),
                department=emp_row[4],
                position=emp_row[5],
                email=emp_row[6],
                phone=emp_row[7]
            )
            db.add(emp)
            db.flush()  # Get the new ID
            employee_id_map[emp_row[0]] = emp.id
            print(f"  Migrated employee: {emp.full_name} (ID: {emp_row[0]} -> {emp.id})")
        
        db.commit()
        print(f"Migrated {len(employees)} employees")
        
        # Migrate vacation records
        print("\nMigrating vacation records...")
        sqlite_cursor.execute("SELECT * FROM vacation_records")
        records = sqlite_cursor.fetchall()
        
        for rec_row in records:
            old_employee_id = rec_row[1]
            new_employee_id = employee_id_map.get(old_employee_id)
            
            if new_employee_id is None:
                print(f"  Warning: Skipping record with unknown employee ID: {old_employee_id}")
                continue
            
            record = models.VacationRecord(
                employee_id=new_employee_id,
                year=rec_row[2],
                days_taken=rec_row[3],
                start_date=datetime.strptime(rec_row[4], '%Y-%m-%d').date(),
                end_date=datetime.strptime(rec_row[5], '%Y-%m-%d').date(),
                description=rec_row[6]
            )
            db.add(record)
            print(f"  Migrated vacation record for employee ID {new_employee_id}")
        
        db.commit()
        print(f"Migrated {len(records)} vacation records")
        
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        sqlite_conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("SQLite to PostgreSQL Migration Script")
    print("=" * 60)
    migrate_data()
