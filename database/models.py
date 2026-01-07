"""
Data models for the application
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date


@dataclass
class Employee:
    """Employee data model"""
    employee_number: str
    full_name: str
    entry_date: date  # Exact entry date
    department: Optional[str] = None
    position: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    @property
    def entry_year(self) -> int:
        """Get entry year from entry date"""
        return self.entry_date.year
    
    def __post_init__(self):
        """Validate data after initialization"""
        if not self.employee_number:
            raise ValueError("Employee number is required")
        if not self.full_name:
            raise ValueError("Full name is required")
        if not self.entry_date:
            raise ValueError("Entry date is required")
        
        # Convert string to date if needed
        if isinstance(self.entry_date, str):
            self.entry_date = datetime.strptime(self.entry_date, '%Y-%m-%d').date()
        
        # Validate entry date
        if self.entry_date > date.today():
            raise ValueError("Entry date cannot be in the future")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'employee_number': self.employee_number,
            'full_name': self.full_name,
            'entry_date': self.entry_date.strftime('%Y-%m-%d') if isinstance(self.entry_date, date) else self.entry_date,
            'department': self.department,
            'position': self.position,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Employee':
        """Create from dictionary"""
        entry_date = data['entry_date']
        if isinstance(entry_date, str):
            entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
        
        return cls(
            id=data.get('id'),
            employee_number=data['employee_number'],
            full_name=data['full_name'],
            entry_date=entry_date,
            department=data.get('department'),
            position=data.get('position'),
            email=data.get('email'),
            phone=data.get('phone'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
        )


@dataclass
class VacationRecord:
    """Vacation record model for tracking taken vacation days"""
    employee_id: int
    year: int
    days_taken: float
    start_date: date
    end_date: date
    description: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[str] = None
    
    def __post_init__(self):
        """Validate data after initialization"""
        # Convert strings to dates if needed
        if isinstance(self.start_date, str):
            self.start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
        if isinstance(self.end_date, str):
            self.end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
        
        if self.start_date > self.end_date:
            raise ValueError("Start date must be before or equal to end date")
        
        if self.days_taken <= 0:
            raise ValueError("Days taken must be greater than 0")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'year': self.year,
            'days_taken': self.days_taken,
            'start_date': self.start_date.strftime('%Y-%m-%d') if isinstance(self.start_date, date) else self.start_date,
            'end_date': self.end_date.strftime('%Y-%m-%d') if isinstance(self.end_date, date) else self.end_date,
            'description': self.description,
            'created_at': self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'VacationRecord':
        """Create from dictionary"""
        start_date = data['start_date']
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        
        end_date = data['end_date']
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        return cls(
            id=data.get('id'),
            employee_id=data['employee_id'],
            year=data['year'],
            days_taken=data['days_taken'],
            start_date=start_date,
            end_date=end_date,
            description=data.get('description'),
            created_at=data.get('created_at'),
        )

