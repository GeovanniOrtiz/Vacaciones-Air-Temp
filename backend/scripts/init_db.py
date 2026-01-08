import sys
import os
from sqlalchemy.orm import Session

# Add the parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app import crud, schemas, models

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin = crud.get_user_by_username(db, "admin")
        if not admin:
            print("Creating admin user...")
            admin_in = schemas.UserCreate(
                username="admin",
                password="adminpassword", # Change this in production!
                role="admin",
                employee_id=None,
                is_active=1
            )
            crud.create_user(db, admin_in)
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")
            
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
