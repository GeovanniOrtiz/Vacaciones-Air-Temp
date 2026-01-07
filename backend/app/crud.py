"""
CRUD operations for database models
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import date
from . import models, schemas


# Employee CRUD operations
def get_employee(db: Session, employee_id: int) -> Optional[models.Employee]:
    """Get employee by ID"""
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def get_employee_by_number(db: Session, employee_number: str) -> Optional[models.Employee]:
    """Get employee by employee number"""
    return db.query(models.Employee).filter(
        models.Employee.employee_number == employee_number
    ).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[models.Employee]:
    """Get all employees with pagination"""
    return db.query(models.Employee).offset(skip).limit(limit).all()


def search_employees(db: Session, search_term: str) -> List[models.Employee]:
    """Search employees by name or employee number"""
    search_pattern = f"%{search_term}%"
    return db.query(models.Employee).filter(
        or_(
            models.Employee.full_name.ilike(search_pattern),
            models.Employee.employee_number.ilike(search_pattern)
        )
    ).all()


def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    """Create new employee"""
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(
    db: Session, 
    employee_id: int, 
    employee: schemas.EmployeeUpdate
) -> Optional[models.Employee]:
    """Update employee"""
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None
    
    update_data = employee.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_employee, field, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int) -> bool:
    """Delete employee"""
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return False
    
    db.delete(db_employee)
    db.commit()
    return True


# Vacation Record CRUD operations
def get_vacation_record(db: Session, record_id: int) -> Optional[models.VacationRecord]:
    """Get vacation record by ID"""
    return db.query(models.VacationRecord).filter(
        models.VacationRecord.id == record_id
    ).first()


def get_vacation_records_by_employee(
    db: Session, 
    employee_id: int
) -> List[models.VacationRecord]:
    """Get all vacation records for an employee"""
    return db.query(models.VacationRecord).filter(
        models.VacationRecord.employee_id == employee_id
    ).all()


def get_vacation_records_by_year(
    db: Session, 
    employee_id: int, 
    year: int
) -> List[models.VacationRecord]:
    """Get vacation records for an employee in a specific year"""
    return db.query(models.VacationRecord).filter(
        models.VacationRecord.employee_id == employee_id,
        models.VacationRecord.year == year
    ).all()


def get_total_days_taken(db: Session, employee_id: int, year: int) -> float:
    """Get total vacation days taken by employee in a specific year"""
    records = get_vacation_records_by_year(db, employee_id, year)
    return sum(record.days_taken for record in records)


def check_vacation_overlap(
    db: Session,
    employee_id: int,
    start_date: date,
    end_date: date,
    exclude_record_id: Optional[int] = None
) -> bool:
    """Check if vacation dates overlap with existing records"""
    query = db.query(models.VacationRecord).filter(
        models.VacationRecord.employee_id == employee_id,
        models.VacationRecord.start_date <= end_date,
        models.VacationRecord.end_date >= start_date
    )
    
    if exclude_record_id:
        query = query.filter(models.VacationRecord.id != exclude_record_id)
    
    return query.first() is not None


def create_vacation_record(
    db: Session, 
    record: schemas.VacationRecordCreate
) -> models.VacationRecord:
    """Create new vacation record"""
    db_record = models.VacationRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_vacation_record(
    db: Session,
    record_id: int,
    record: schemas.VacationRecordUpdate
) -> Optional[models.VacationRecord]:
    """Update vacation record"""
    db_record = get_vacation_record(db, record_id)
    if not db_record:
        return None
    
    update_data = record.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_vacation_record(db: Session, record_id: int) -> bool:
    """Delete vacation record"""
    db_record = get_vacation_record(db, record_id)
    if not db_record:
        return False
    
    db.delete(db_record)
    db.commit()
    return True
