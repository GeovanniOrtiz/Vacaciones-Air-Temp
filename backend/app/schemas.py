"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


# Employee Schemas
class EmployeeBase(BaseModel):
    employee_number: str
    full_name: str
    entry_date: date
    department: Optional[str] = None
    position: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    employee_number: Optional[str] = None
    full_name: Optional[str] = None
    entry_date: Optional[date] = None
    department: Optional[str] = None
    position: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class Employee(EmployeeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Vacation Record Schemas
class VacationRecordBase(BaseModel):
    employee_id: int
    year: int
    days_taken: float
    start_date: date
    end_date: date
    description: Optional[str] = None


class VacationRecordCreate(VacationRecordBase):
    pass


class VacationRecordUpdate(BaseModel):
    year: Optional[int] = None
    days_taken: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None


class VacationRecord(VacationRecordBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Vacation Summary Schema
class VacationSummary(BaseModel):
    """Vacation summary with calculations"""
    employee_id: int
    employee_number: str
    full_name: str
    entry_date: date
    entry_year: int
    current_year: int
    years_of_service: int
    completed_years: int
    service_years: int
    service_months: int
    vacation_days: int
    vacation_premium_percentage: int
    vacation_premium_days: float
    next_increase_years: int
    next_vacation_days: int
    year: int
    total_days: int
    days_taken: float
    days_remaining: float
    usage_percentage: float
    period_start: date
    period_end: date
    
    class Config:
        from_attributes = True
