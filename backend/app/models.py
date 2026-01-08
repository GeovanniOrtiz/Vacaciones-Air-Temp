"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Employee(Base):
    """Employee model"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    entry_date = Column(Date, nullable=False)
    department = Column(String)
    position = Column(String)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    vacation_records = relationship("VacationRecord", back_populates="employee", cascade="all, delete-orphan")
    user = relationship("User", back_populates="employee", uselist=False)


class VacationRecord(Base):
    """Vacation record model"""
    __tablename__ = "vacation_records"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    year = Column(Integer, nullable=False)
    days_taken = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="vacation_records")


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="employee")  # admin, employee
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    is_active = Column(Integer, default=1) # 1 for active, 0 for inactive
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="user")
