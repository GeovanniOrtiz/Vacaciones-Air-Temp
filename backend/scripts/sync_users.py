import sys
import os
from sqlalchemy.orm import Session

# Add the parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app import crud, schemas, models

def sync_employees_to_users():
    db = SessionLocal()
    try:
        employees = crud.get_employees(db)
        print(f"Found {len(employees)} employees.")
        
        for emp in employees:
            # Check if user already exists for this employee
            user = db.query(models.User).filter(models.User.employee_id == emp.id).first()
            if not user:
                # Create username from employee number
                username = emp.employee_number
                # Default password is also employee number (user should change it later)
                password = emp.employee_number
                
                print(f"Creating user for {emp.full_name} (Username: {username})")
                user_in = schemas.UserCreate(
                    username=username,
                    password=password,
                    role="employee",
                    employee_id=emp.id,
                    is_active=1
                )
                crud.create_user(db, user_in)
            else:
                print(f"User already exists for {emp.full_name}")
                
        print("Sync completed successfully.")
            
    finally:
        db.close()

if __name__ == "__main__":
    sync_employees_to_users()
