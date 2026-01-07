"""
Employee service for business operations
"""
from typing import List, Optional, Dict
from datetime import datetime, date
from database.models import Employee, VacationRecord
from database.queries import EmployeeQueries, VacationRecordQueries
from business.vacation_calculator import VacationCalculator


class EmployeeService:
    """Business logic for employee management"""
    
    def __init__(self):
        self.queries = EmployeeQueries()
        self.vacation_record_queries = VacationRecordQueries()
        self.vacation_calc = VacationCalculator()
    
    def create_employee(self, employee: Employee) -> tuple[bool, str, Optional[int]]:
        """
        Create a new employee
        
        Returns:
            (success, message, employee_id)
        """
        try:
            # Check if employee number already exists
            if self.queries.employee_number_exists(employee.employee_number):
                return False, f"El número de empleado '{employee.employee_number}' ya existe", None
            
            # Create employee
            employee_id = self.queries.create_employee(employee)
            return True, "Empleado creado exitosamente", employee_id
            
        except Exception as e:
            return False, f"Error al crear empleado: {str(e)}", None
    
    def update_employee(self, employee: Employee) -> tuple[bool, str]:
        """
        Update employee information
        
        Returns:
            (success, message)
        """
        try:
            if not employee.id:
                return False, "ID de empleado requerido"
            
            # Check if employee number exists for another employee
            if self.queries.employee_number_exists(employee.employee_number, exclude_id=employee.id):
                return False, f"El número de empleado '{employee.employee_number}' ya existe"
            
            # Update employee
            success = self.queries.update_employee(employee)
            if success:
                return True, "Empleado actualizado exitosamente"
            else:
                return False, "No se encontró el empleado"
                
        except Exception as e:
            return False, f"Error al actualizar empleado: {str(e)}"
    
    def delete_employee(self, employee_id: int) -> tuple[bool, str]:
        """
        Delete employee
        
        Returns:
            (success, message)
        """
        try:
            success = self.queries.delete_employee(employee_id)
            if success:
                return True, "Empleado eliminado exitosamente"
            else:
                return False, "No se encontró el empleado"
                
        except Exception as e:
            return False, f"Error al eliminar empleado: {str(e)}"
    
    def get_employee_by_id(self, employee_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        return self.queries.get_employee_by_id(employee_id)
    
    def get_employee_by_number(self, employee_number: str) -> Optional[Employee]:
        """Get employee by employee number"""
        return self.queries.get_employee_by_number(employee_number)
    
    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        return self.queries.get_all_employees()
    
    def search_employees(self, search_term: str) -> List[Employee]:
        """Search employees by name or number"""
        if not search_term or search_term.strip() == "":
            return self.get_all_employees()
        return self.queries.search_employees(search_term.strip())
    
    def get_employee_with_vacation_info(self, employee: Employee, year: int = None) -> Dict:
        """
        Get employee with vacation information including taken/remaining days
        
        Returns:
            Dictionary with employee and vacation data
        """
        if year is None:
            # Calculate current service period year
            _, _, year = self.vacation_calc.get_service_period(employee.entry_date, date.today())
        
        # Get total days taken for the service period year
        days_taken = self.vacation_record_queries.get_total_days_taken(employee.id, year)
        
        # Get vacation summary
        vacation_summary = self.vacation_calc.get_vacation_summary(
            employee.entry_date,
            days_taken,
            year
        )
        
        return {
            'employee': employee,
            'vacation_info': vacation_summary,
            'days_taken': days_taken,
        }
    
    def get_all_employees_with_vacation(self, year: int = None) -> List[Dict]:
        """
        Get all employees with their vacation information
        
        Returns:
            List of dictionaries with employee and vacation data
        """
        employees = self.get_all_employees()
        return [
            self.get_employee_with_vacation_info(emp, year)
            for emp in employees
        ]
    
    # Vacation Record Management
    
    def create_vacation_record(self, record: VacationRecord) -> tuple[bool, str, Optional[int]]:
        """
        Create a new vacation record
        
        Returns:
            (success, message, record_id)
        """
        try:
            # 1. Check for overlap
            if self.vacation_record_queries.check_overlap(record.employee_id, record.start_date, record.end_date):
                return False, "Ya existe un registro de vacaciones en estas fechas", None
            
            # 2. Check for cross-cycle (start and end must be in same period)
            # Get employee to get entry date
            employee = self.get_employee_by_id(record.employee_id)
            if not employee:
                return False, "Empleado no encontrado", None
                
            _, _, start_year = self.vacation_calc.get_service_period(employee.entry_date, record.start_date)
            _, _, end_year = self.vacation_calc.get_service_period(employee.entry_date, record.end_date)
            
            if start_year != end_year:
                return False, "Las vacaciones no pueden exceder el ciclo actual. Por favor divida el registro en dos partes.", None
            
            record_id = self.vacation_record_queries.create_record(record)
            return True, "Registro de vacaciones creado exitosamente", record_id
        except Exception as e:
            return False, f"Error al crear registro: {str(e)}", None
    
    def update_vacation_record(self, record: VacationRecord) -> tuple[bool, str]:
        """
        Update vacation record
        
        Returns:
            (success, message)
        """
        try:
            # 1. Check for overlap (excluding current record)
            if self.vacation_record_queries.check_overlap(record.employee_id, record.start_date, record.end_date, exclude_record_id=record.id):
                return False, "Ya existe un registro de vacaciones en estas fechas"
            
            # 2. Check for cross-cycle
            employee = self.get_employee_by_id(record.employee_id)
            if not employee:
                return False, "Empleado no encontrado"
                
            _, _, start_year = self.vacation_calc.get_service_period(employee.entry_date, record.start_date)
            _, _, end_year = self.vacation_calc.get_service_period(employee.entry_date, record.end_date)
            
            if start_year != end_year:
                return False, "Las vacaciones no pueden exceder el ciclo actual. Por favor divida el registro en dos partes."
            
            success = self.vacation_record_queries.update_record(record)
            if success:
                return True, "Registro actualizado exitosamente"
            else:
                return False, "No se encontró el registro"
        except Exception as e:
            return False, f"Error al actualizar registro: {str(e)}"
    
    def delete_vacation_record(self, record_id: int) -> tuple[bool, str]:
        """
        Delete vacation record
        
        Returns:
            (success, message)
        """
        try:
            success = self.vacation_record_queries.delete_record(record_id)
            if success:
                return True, "Registro eliminado exitosamente"
            else:
                return False, "No se encontró el registro"
        except Exception as e:
            return False, f"Error al eliminar registro: {str(e)}"
    
    def get_vacation_records(self, employee_id: int, year: int = None) -> List[VacationRecord]:
        """Get vacation records for an employee"""
        if year:
            return self.vacation_record_queries.get_records_by_year(employee_id, year)
        return self.vacation_record_queries.get_records_by_employee(employee_id)
    
    def validate_employee_data(self, employee: Employee) -> tuple[bool, str]:
        """
        Validate employee data
        
        Returns:
            (is_valid, error_message)
        """
        try:
            # Basic validation is done in Employee.__post_init__
            # Additional business validation can be added here
            
            if len(employee.employee_number) < 1:
                return False, "El número de empleado es muy corto"
            
            if len(employee.full_name) < 3:
                return False, "El nombre completo es muy corto"
            
            return True, ""
            
        except ValueError as e:
            return False, str(e)

