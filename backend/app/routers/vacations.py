"""
Vacation records API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, crud
from ..database import get_db
from .auth import get_current_user
from ..services.vacation_calculator import VacationCalculator

router = APIRouter(prefix="/api/vacations", tags=["vacations"])
vacation_calc = VacationCalculator()


@router.get("/", response_model=List[schemas.VacationRecord])
def get_vacation_records(
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    year: Optional[int] = Query(None, description="Filter by year"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get vacation records with optional filters"""
    if current_user.role != "admin":
        # Employees can only see their own records
        if employee_id and employee_id != current_user.employee_id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        employee_id = current_user.employee_id
    if employee_id and year:
        return crud.get_vacation_records_by_year(db, employee_id, year)
    elif employee_id:
        return crud.get_vacation_records_by_employee(db, employee_id)
    else:
        # Return all records (with reasonable limit)
        return db.query(models.VacationRecord).limit(1000).all()


@router.get("/{record_id}", response_model=schemas.VacationRecord)
def get_vacation_record(
    record_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get vacation record by ID"""
    record = crud.get_vacation_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Vacation record not found")
        
    if current_user.role != "admin" and record.employee_id != current_user.employee_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    return record


@router.post("/", response_model=schemas.VacationRecord)
def create_vacation_record(
    record: schemas.VacationRecordCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create new vacation record (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    # Verify employee exists
    employee = crud.get_employee(db, record.employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check for overlap
    if crud.check_vacation_overlap(db, record.employee_id, record.start_date, record.end_date):
        raise HTTPException(
            status_code=400, 
            detail="Ya existe un registro de vacaciones en estas fechas"
        )
    
    # Check for cross-cycle (start and end must be in same period)
    _, _, start_year = vacation_calc.get_service_period(employee.entry_date, record.start_date)
    _, _, end_year = vacation_calc.get_service_period(employee.entry_date, record.end_date)
    
    if start_year != end_year:
        raise HTTPException(
            status_code=400,
            detail="Las vacaciones no pueden exceder el ciclo actual. Por favor divida el registro en dos partes."
        )
    
    return crud.create_vacation_record(db, record)


@router.put("/{record_id}", response_model=schemas.VacationRecord)
def update_vacation_record(
    record_id: int,
    record: schemas.VacationRecordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update vacation record (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_record = crud.get_vacation_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Vacation record not found")
    
    # If dates are being updated, check for overlap
    start_date = record.start_date if record.start_date else db_record.start_date
    end_date = record.end_date if record.end_date else db_record.end_date
    
    if crud.check_vacation_overlap(
        db, 
        db_record.employee_id, 
        start_date, 
        end_date, 
        exclude_record_id=record_id
    ):
        raise HTTPException(
            status_code=400,
            detail="Ya existe un registro de vacaciones en estas fechas"
        )
    
    # Check for cross-cycle if dates are being updated
    if record.start_date or record.end_date:
        employee = crud.get_employee(db, db_record.employee_id)
        _, _, start_year = vacation_calc.get_service_period(employee.entry_date, start_date)
        _, _, end_year = vacation_calc.get_service_period(employee.entry_date, end_date)
        
        if start_year != end_year:
            raise HTTPException(
                status_code=400,
                detail="Las vacaciones no pueden exceder el ciclo actual. Por favor divida el registro en dos partes."
            )
    
    updated_record = crud.update_vacation_record(db, record_id, record)
    return updated_record


@router.delete("/{record_id}")
def delete_vacation_record(
    record_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete vacation record (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    success = crud.delete_vacation_record(db, record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vacation record not found")
    return {"message": "Vacation record deleted successfully"}
