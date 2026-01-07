"""
Database queries for employee operations
"""
from typing import List, Optional
from datetime import datetime, date
from database.models import Employee, VacationRecord
from database.database import get_database


class EmployeeQueries:
    """CRUD operations for employees"""
    
    def __init__(self):
        self.db = get_database()
    
    def create_employee(self, employee: Employee) -> int:
        """
        Create a new employee
        Returns: employee ID
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO employees (
                employee_number, full_name, entry_date,
                department, position, email, phone
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            employee.employee_number,
            employee.full_name,
            employee.entry_date.strftime('%Y-%m-%d'),
            employee.department,
            employee.position,
            employee.email,
            employee.phone
        ))
        
        employee_id = cursor.fetchone()['id']
        conn.commit()
        return employee_id
    
    def get_employee_by_id(self, employee_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_employee(row)
        return None
    
    def get_employee_by_number(self, employee_number: str) -> Optional[Employee]:
        """Get employee by employee number"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM employees WHERE employee_number = %s",
            (employee_number,)
        )
        row = cursor.fetchone()
        
        if row:
            return self._row_to_employee(row)
        return None
    
    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM employees 
            ORDER BY full_name ASC
        """)
        rows = cursor.fetchall()
        
        return [self._row_to_employee(row) for row in rows]
    
    def search_employees(self, search_term: str) -> List[Employee]:
        """
        Search employees by name or employee number
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{search_term}%"
        cursor.execute("""
            SELECT * FROM employees 
            WHERE full_name LIKE %s OR employee_number LIKE %s
            ORDER BY full_name ASC
        """, (search_pattern, search_pattern))
        
        rows = cursor.fetchall()
        return [self._row_to_employee(row) for row in rows]
    
    def update_employee(self, employee: Employee) -> bool:
        """
        Update employee information
        Returns: True if successful
        """
        if not employee.id:
            raise ValueError("Employee ID is required for update")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE employees 
            SET employee_number = %s,
                full_name = %s,
                entry_date = %s,
                department = %s,
                position = %s,
                email = %s,
                phone = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (
            employee.employee_number,
            employee.full_name,
            employee.entry_date.strftime('%Y-%m-%d'),
            employee.department,
            employee.position,
            employee.email,
            employee.phone,
            employee.id
        ))
        
        conn.commit()
        return cursor.rowcount > 0
    
    def delete_employee(self, employee_id: int) -> bool:
        """
        Delete employee by ID
        Returns: True if successful
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        conn.commit()
        
        return cursor.rowcount > 0
    
    def employee_number_exists(self, employee_number: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if employee number already exists
        exclude_id: Exclude this ID from check (for updates)
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        if exclude_id:
            cursor.execute(
                "SELECT COUNT(*) as count FROM employees WHERE employee_number = %s AND id != %s",
                (employee_number, exclude_id)
            )
        else:
            cursor.execute(
                "SELECT COUNT(*) as count FROM employees WHERE employee_number = %s",
                (employee_number,)
            )
        
        result = cursor.fetchone()
        return result['count'] > 0 if result else False
    
    def _row_to_employee(self, row) -> Employee:
        """Convert database row to Employee object"""
        return Employee(
            id=row['id'],
            employee_number=row['employee_number'],
            full_name=row['full_name'],
            entry_date=row['entry_date'],
            department=row['department'],
            position=row['position'],
            email=row['email'],
            phone=row['phone'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )


class VacationRecordQueries:
    """CRUD operations for vacation records"""
    
    def __init__(self):
        self.db = get_database()
    
    def create_record(self, record: VacationRecord) -> int:
        """
        Create a new vacation record
        Returns: record ID
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO vacation_records (
                employee_id, year, days_taken,
                start_date, end_date, description
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            record.employee_id,
            record.year,
            record.days_taken,
            record.start_date.strftime('%Y-%m-%d'),
            record.end_date.strftime('%Y-%m-%d'),
            record.description
        ))
        
        record_id = cursor.fetchone()['id']
        conn.commit()
        return record_id
    
    def get_record_by_id(self, record_id: int) -> Optional[VacationRecord]:
        """Get vacation record by ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM vacation_records WHERE id = %s", (record_id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_record(row)
        return None
    
    def get_records_by_employee(self, employee_id: int) -> List[VacationRecord]:
        """Get all vacation records for an employee"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM vacation_records 
            WHERE employee_id = %s
            ORDER BY year DESC, start_date DESC
        """, (employee_id,))
        
        rows = cursor.fetchall()
        return [self._row_to_record(row) for row in rows]
    
    def get_records_by_year(self, employee_id: int, year: int) -> List[VacationRecord]:
        """Get vacation records for specific employee and year"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM vacation_records 
            WHERE employee_id = %s AND year = %s
            ORDER BY start_date DESC
        """, (employee_id, year))
        
        rows = cursor.fetchall()
        return [self._row_to_record(row) for row in rows]
    
    def get_total_days_taken(self, employee_id: int, year: int) -> float:
        """Calculate total vacation days taken for a specific year"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COALESCE(SUM(days_taken), 0) as total
            FROM vacation_records 
            WHERE employee_id = %s AND year = %s
        """, (employee_id, year))
        
        result = cursor.fetchone()
        return float(result['total']) if result else 0.0
    
    def update_record(self, record: VacationRecord) -> bool:
        """
        Update vacation record
        Returns: True if successful
        """
        if not record.id:
            raise ValueError("Record ID is required for update")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE vacation_records 
            SET employee_id = %s,
                year = %s,
                days_taken = %s,
                start_date = %s,
                end_date = %s,
                description = %s
            WHERE id = %s
        """, (
            record.employee_id,
            record.year,
            record.days_taken,
            record.start_date.strftime('%Y-%m-%d'),
            record.end_date.strftime('%Y-%m-%d'),
            record.description,
            record.id
        ))
        
        conn.commit()
        return cursor.rowcount > 0
    
    def delete_record(self, record_id: int) -> bool:
        """
        Delete vacation record by ID
        Returns: True if successful
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM vacation_records WHERE id = %s", (record_id,))
        conn.commit()
        
        return cursor.rowcount > 0
    
    def check_overlap(self, employee_id: int, start_date: date, end_date: date, exclude_record_id: Optional[int] = None) -> bool:
        """
        Check if there are any overlapping vacation records
        
        Args:
            employee_id: Employee ID
            start_date: Start date of new record
            end_date: End date of new record
            exclude_record_id: Record ID to exclude (for updates)
            
        Returns:
            True if overlap exists, False otherwise
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Format dates
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        query = """
            SELECT COUNT(*) as count FROM vacation_records 
            WHERE employee_id = %s 
            AND (
                (start_date <= %s AND end_date >= %s) OR  -- New starts inside existing
                (start_date <= %s AND end_date >= %s) OR  -- New ends inside existing
                (start_date >= %s AND end_date <= %s)     -- New encloses existing
            )
        """
        params = [employee_id, end_str, end_str, start_str, start_str, start_str, end_str]
        
        if exclude_record_id:
            query += " AND id != %s"
            params.append(exclude_record_id)
            
        cursor.execute(query, tuple(params))
        result = cursor.fetchone()
        
        return result['count'] > 0 if result else False

    def _row_to_record(self, row) -> VacationRecord:
        """Convert database row to VacationRecord object"""
        return VacationRecord(
            id=row['id'],
            employee_id=row['employee_id'],
            year=row['year'],
            days_taken=row['days_taken'],
            start_date=row['start_date'],
            end_date=row['end_date'],
            description=row['description'],
            created_at=row['created_at']
        )

