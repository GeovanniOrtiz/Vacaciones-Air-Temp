"""
Vacation calculator based on Mexican Federal Labor Law 2025
Ley Federal del Trabajo - Artículo 76
"""
from datetime import datetime, date
from typing import Dict, Tuple, Optional


class VacationCalculator:
    """
    Calculate vacation days according to Mexican Federal Labor Law 2025
    """
    
    # Vacation days table according to Ley Federal del Trabajo
    VACATION_TABLE = {
        1: 12,   # Year 1: 12 days
        2: 14,   # Year 2: 14 days
        3: 16,   # Year 3: 16 days
        4: 18,   # Year 4: 18 days
        5: 20,   # Year 5: 20 days
    }
    
    # After 5 years: 2 additional days every 5 years
    VACATION_PREMIUM_PERCENTAGE = 25  # 25% vacation premium (prima vacacional)
    
    @staticmethod
    def calculate_years_of_service(entry_date: date, current_date: date = None) -> int:
        """
        Calculate years of service from entry date
        
        Args:
            entry_date: Date the employee started
            current_date: Current date (defaults to today)
        
        Returns:
            Years of service (minimum 1)
        """
        if current_date is None:
            current_date = date.today()
        
        # Convert string to date if needed
        if isinstance(entry_date, str):
            entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
        if isinstance(current_date, str):
            current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
        
        # Calculate years difference
        years = current_date.year - entry_date.year
        
        # Adjust if anniversary hasn't occurred yet this year
        if (current_date.month, current_date.day) < (entry_date.month, entry_date.day):
            years -= 1
        
        return max(1, years + 1)  # Minimum 1 year, +1 because first year counts
    
    @staticmethod
    def calculate_completed_years(entry_date: date, current_date: date = None) -> int:
        """
        Calculate completed years of service (0-based)
        
        Args:
            entry_date: Date the employee started
            current_date: Current date (defaults to today)
        
        Returns:
            Completed years of service (can be 0)
        """
        if current_date is None:
            current_date = date.today()
        
        # Convert string to date if needed
        if isinstance(entry_date, str):
            entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
        if isinstance(current_date, str):
            current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
        
        # Calculate years difference
        years = current_date.year - entry_date.year
        
        # Adjust if anniversary hasn't occurred yet this year
        if (current_date.month, current_date.day) < (entry_date.month, entry_date.day):
            years -= 1
            
        return max(0, years)
    
    @staticmethod
    def calculate_service_time(entry_date: date, current_date: date = None) -> Tuple[int, int]:
        """
        Calculate years and months of service
        
        Args:
            entry_date: Date the employee started
            current_date: Current date (defaults to today)
        
        Returns:
            Tuple (years, months)
        """
        if current_date is None:
            current_date = date.today()
        
        # Convert string to date if needed
        if isinstance(entry_date, str):
            entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
        if isinstance(current_date, str):
            current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
            
        years = current_date.year - entry_date.year
        
        # Adjust years if anniversary hasn't occurred yet
        if (current_date.month, current_date.day) < (entry_date.month, entry_date.day):
            years -= 1
            
        years = max(0, years)
        
        # Calculate months
        # If current month >= entry month: simple difference
        # If current month < entry month: (12 - entry month) + current month
        if current_date.month >= entry_date.month:
            months = current_date.month - entry_date.month
            # If day is earlier, we haven't completed the month yet
            if current_date.day < entry_date.day:
                months -= 1
        else:
            months = (12 - entry_date.month) + current_date.month
            if current_date.day < entry_date.day:
                months -= 1
                
        if months < 0:
            months += 12
            
        return years, months
    
    @staticmethod
    def calculate_vacation_days(years_of_service: int) -> int:
        """
        Calculate vacation days based on years of service
        
        Args:
            years_of_service: Number of years worked
        
        Returns:
            Number of vacation days
        """
        if years_of_service < 1:
            return 0
            
        # Years 1-5: Use lookup table
        if years_of_service <= 5:
            return VacationCalculator.VACATION_TABLE.get(years_of_service, 12)
        
        # Years 6-10: 22 days
        # Years 11-15: 24 days
        # Years 16-20: 26 days
        # And so on (+2 days every 5 years)
        
        # Base calculation for years > 5
        # We start at year 6 with 22 days
        base_days = 22
        years_after_start = years_of_service - 6
        
        # Add 2 days for every complete 5-year period passed since year 6
        additional_periods = years_after_start // 5
        additional_days = additional_periods * 2
        
        return base_days + additional_days
    
    @staticmethod
    def calculate_vacation_premium(vacation_days: int) -> float:
        """
        Calculate vacation premium (25% of vacation days)
        
        Args:
            vacation_days: Number of vacation days
        
        Returns:
            Vacation premium in days
        """
        return vacation_days * (VacationCalculator.VACATION_PREMIUM_PERCENTAGE / 100)
    
    @staticmethod
    def get_vacation_info(entry_date: date, current_date: date = None) -> Dict:
        """
        Get complete vacation information for an employee
        
        Args:
            entry_date: Date the employee started
            current_date: Current date (defaults to today)
        
        Returns:
            Dictionary with vacation information
        """
        if current_date is None:
            current_date = date.today()
        
        years_of_service = VacationCalculator.calculate_years_of_service(
            entry_date, current_date
        )
        completed_years = VacationCalculator.calculate_completed_years(
            entry_date, current_date
        )
        service_years, service_months = VacationCalculator.calculate_service_time(
            entry_date, current_date
        )
        vacation_days = VacationCalculator.calculate_vacation_days(years_of_service)
        vacation_premium = VacationCalculator.calculate_vacation_premium(vacation_days)
        
        return {
            'entry_date': entry_date,
            'entry_year': entry_date.year if isinstance(entry_date, date) else int(entry_date.split('-')[0]),
            'current_year': current_date.year if isinstance(current_date, date) else datetime.now().year,
            'years_of_service': years_of_service,
            'completed_years': completed_years,
            'service_years': service_years,
            'service_months': service_months,
            'vacation_days': vacation_days,
            'vacation_premium_percentage': VacationCalculator.VACATION_PREMIUM_PERCENTAGE,
            'vacation_premium_days': vacation_premium,
            'next_increase_years': VacationCalculator._years_until_next_increase(years_of_service),
            'next_vacation_days': VacationCalculator._next_vacation_days(years_of_service),
        }
    
    @staticmethod
    def get_service_period(entry_date: date, target_date: date = None) -> Tuple[date, date, int]:
        """
        Get the service period (start, end, year) for a given date
        
        Args:
            entry_date: Employee entry date
            target_date: Date to check (defaults to today)
            
        Returns:
            (period_start, period_end, period_year)
            period_year is the year the period started
        """
        if target_date is None:
            target_date = date.today()
            
        # Ensure dates are date objects
        if isinstance(entry_date, str):
            entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
        if isinstance(target_date, str):
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
            
        # Calculate anniversary in target year
        anniversary_this_year = date(target_date.year, entry_date.month, entry_date.day)
        
        if target_date >= anniversary_this_year:
            # Current period started this year
            period_start = anniversary_this_year
            period_end = date(target_date.year + 1, entry_date.month, entry_date.day)
            period_year = target_date.year
        else:
            # Current period started last year
            period_start = date(target_date.year - 1, entry_date.month, entry_date.day)
            period_end = anniversary_this_year
            period_year = target_date.year - 1
            
        return period_start, period_end, period_year

    @staticmethod
    def get_vacation_summary(entry_date: date, days_taken: float = 0, year: int = None) -> Dict:
        """
        Get vacation summary including taken and remaining days for a service period
        
        Args:
            entry_date: Date the employee started
            days_taken: Total vacation days taken for the period
            year: Service period start year (defaults to current period)
        
        Returns:
            Dictionary with vacation summary (total, taken, remaining)
        """
        # Ensure entry_date is date object
        if isinstance(entry_date, str):
            entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
            
        if year is None:
            # Determine current service period year
            _, _, year = VacationCalculator.get_service_period(entry_date)
        
        # Calculate years of service at the START of this period
        # If period starts in 2024 and entry was 2017 -> 2024 - 2017 = 7 years completed
        years_completed = year - entry_date.year
        
        # Vacation days are earned for the COMPLETED year. 
        # So in period 7 (working towards year 8), you use days earned from year 7.
        # Year 0 (0-1): 0 completed years -> 0 days
        # Year 1 (1-2): 1 completed year -> 12 days
        
        vacation_days = VacationCalculator.calculate_vacation_days(years_completed)
        
        # Use current date for service time calculation to show actual years/months
        # But override vacation days/premium for the specific period
        vacation_info = VacationCalculator.get_vacation_info(entry_date, date.today())
        
        # Override vacation days with the specific period calculation
        vacation_info['vacation_days'] = vacation_days
        vacation_info['vacation_premium_days'] = VacationCalculator.calculate_vacation_premium(vacation_days)
        
        remaining_days = max(0, vacation_days - days_taken)
        usage_percentage = (days_taken / vacation_days * 100) if vacation_days > 0 else 0
        
        return {
            **vacation_info,
            'year': year,
            'total_days': vacation_days,
            'days_taken': days_taken,
            'days_remaining': remaining_days,
            'usage_percentage': usage_percentage,
            'period_start': date(year, entry_date.month, entry_date.day),
            'period_end': date(year + 1, entry_date.month, entry_date.day)
        }
    
    @staticmethod
    def _years_until_next_increase(years_of_service: int) -> int:
        """Calculate years until next vacation day increase"""
        if years_of_service < 5:
            return 1  # Increases every year for first 5 years
        
        # After 5 years, increases every 5 years starting from year 6
        # Years 6-10 (22 days) -> Increase at year 11
        # Years 11-15 (24 days) -> Increase at year 16
        
        years_since_block_start = (years_of_service - 6) % 5
        return 5 - years_since_block_start
    
    @staticmethod
    def _next_vacation_days(years_of_service: int) -> int:
        """Calculate vacation days for next year"""
        return VacationCalculator.calculate_vacation_days(years_of_service + 1)
    
    @staticmethod
    def get_vacation_breakdown(entry_date: date, current_date: date = None) -> str:
        """
        Get a formatted breakdown of vacation calculation
        
        Args:
            entry_date: Date the employee started
            current_date: Current date (defaults to today)
        
        Returns:
            Formatted string with calculation breakdown
        """
        info = VacationCalculator.get_vacation_info(entry_date, current_date)
        
        years = info.get('service_years', info.get('completed_years', 0))
        months = info.get('service_months', 0)
        
        years_str = f"{years} año{'s' if years != 1 else ''}"
        months_str = f"{months} mes{'es' if months != 1 else ''}"
        
        service_time_str = f"{years_str} {months_str}" if months > 0 else years_str
        
        breakdown = f"""
Fecha de Entrada: {info['entry_date']}
Año Actual: {info['current_year']}
Años de Servicio: {service_time_str}

Días de Vacaciones: {info['vacation_days']} días
Prima Vacacional ({info['vacation_premium_percentage']}%): {info['vacation_premium_days']:.1f} días

Próximo Aumento: En {info['next_increase_years']} año(s)
Días Siguientes: {info['next_vacation_days']} días
        """.strip()
        
        return breakdown

