"""
Employee API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from .. import models, schemas, crud
from ..database import get_db
from .auth import get_current_user
from ..services.vacation_calculator import VacationCalculator

router = APIRouter(prefix="/api/employees", tags=["employees"])
vacation_calc = VacationCalculator()


@router.get("/", response_model=List[schemas.Employee])
def get_employees(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = Query(None, description="Search by name or employee number"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all employees with optional search (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    if search:
        employees = crud.search_employees(db, search)
    else:
        employees = crud.get_employees(db, skip, limit)
    return employees


@router.get("/{employee_id}", response_model=schemas.Employee)
def get_employee(
    employee_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get employee by ID"""
    if current_user.role != "admin" and current_user.employee_id != employee_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.get("/{employee_id}/vacation-summary", response_model=schemas.VacationSummary)
def get_employee_vacation_summary(
    employee_id: int,
    year: Optional[int] = Query(None, description="Service period year (defaults to current)"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get employee vacation summary with calculations"""
    if current_user.role != "admin" and current_user.employee_id != employee_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Determine year if not provided
    if year is None:
        _, _, year = vacation_calc.get_service_period(employee.entry_date, date.today())
    
    # Get total days taken for the year
    days_taken = crud.get_total_days_taken(db, employee_id, year)
    
    # Calculate vacation summary
    summary = vacation_calc.get_vacation_summary(employee.entry_date, days_taken, year)
    
    # Add employee information
    summary['employee_id'] = employee.id
    summary['employee_number'] = employee.employee_number
    summary['full_name'] = employee.full_name
    
    return summary


@router.post("/", response_model=schemas.Employee)
def create_employee(
    employee: schemas.EmployeeCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create new employee (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    # Check if employee number already exists
    existing = crud.get_employee_by_number(db, employee.employee_number)
    if existing:
        raise HTTPException(status_code=400, detail="Employee number already exists")
    
    return crud.create_employee(db, employee)


@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(
    employee_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update employee (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_employee = crud.update_employee(db, employee_id, employee)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete employee (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    success = crud.delete_employee(db, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}
