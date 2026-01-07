"""
Employee list widget with search functionality
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLineEdit, QLabel, QPushButton, QHeaderView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from typing import List, Dict
from business.vacation_calculator import VacationCalculator


class EmployeeListWidget(QWidget):
    """Widget for displaying and searching employees"""
    
    employee_selected = Signal(int)  # Emits employee ID
    add_employee_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vacation_calc = VacationCalculator()
        self.employees_data = []
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Header with title and add button
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Empleados")
        title_label.setObjectName("sectionLabel")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        add_btn = QPushButton("+ Agregar Empleado")
        add_btn.setObjectName("addButton")
        add_btn.clicked.connect(self.add_employee_clicked.emit)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍")
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre o número de empleado...")
        self.search_input.textChanged.connect(self._on_search)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "No. Empleado",
            "Nombre Completo",
            "Fecha Entrada",
            "Años Servicio",
            "Días Totales",
            "Días Restantes"
        ])
        
        # Configure table
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # No. Empleado
        header.setSectionResizeMode(1, QHeaderView.Stretch)          # Nombre Completo (Stretch to fill space)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # Fecha Entrada
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Años Servicio
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) # Días Totales
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Días Restantes
        
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        
        layout.addWidget(self.table)
        
        # Employee count label
        self.count_label = QLabel("Total: 0 empleados")
        self.count_label.setStyleSheet("color: #94a3b8;")
        layout.addWidget(self.count_label)
    
    def set_employees(self, employees_with_vacation: List[Dict]):
        """Set the list of employees to display"""
        self.employees_data = employees_with_vacation
        self._update_table(employees_with_vacation)
    
    def _update_table(self, employees_with_vacation: List[Dict]):
        """Update table with employee data"""
        self.table.setRowCount(0)
        
        for data in employees_with_vacation:
            employee = data['employee']
            vacation_info = data['vacation_info']
            
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Employee number
            item = QTableWidgetItem(employee.employee_number)
            item.setData(Qt.UserRole, employee.id)
            self.table.setItem(row, 0, item)
            
            # Full name
            self.table.setItem(row, 1, QTableWidgetItem(employee.full_name))
            
            # Entry date
            entry_date = employee.entry_date
            if isinstance(entry_date, str):
                from datetime import datetime
                entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
            date_str = entry_date.strftime('%d/%m/%Y')
            self.table.setItem(row, 2, QTableWidgetItem(date_str))
            
            # Years of service
            years = vacation_info.get('service_years', vacation_info.get('completed_years', 0))
            months = vacation_info.get('service_months', 0)
            
            years_str = f"{years} año{'s' if years != 1 else ''}"
            
            if months > 0:
                months_str = f"{months} mes{'es' if months != 1 else ''}"
                display_str = f"{years_str}, {months_str}"
            else:
                display_str = years_str

            self.table.setItem(row, 3, QTableWidgetItem(display_str))
            
            # Total vacation days
            total_days = vacation_info.get('total_days', vacation_info.get('vacation_days', 0))
            self.table.setItem(row, 4, QTableWidgetItem(f"{total_days} días"))
            
            # Days remaining
            days_remaining = vacation_info.get('days_remaining', total_days)
            self.table.setItem(row, 5, QTableWidgetItem(f"{days_remaining:.1f} días"))
        
        self.count_label.setText(f"Total: {len(employees_with_vacation)} empleado(s)")
    
    def _on_search(self, text: str):
        """Filter table based on search text"""
        search_text = text.lower()
        
        for row in range(self.table.rowCount()):
            employee_num = self.table.item(row, 0).text().lower()
            full_name = self.table.item(row, 1).text().lower()
            
            match = search_text in employee_num or search_text in full_name
            self.table.setRowHidden(row, not match)
    
    def _on_selection_changed(self):
        """Handle row selection"""
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            employee_id = self.table.item(row, 0).data(Qt.UserRole)
            if employee_id:
                self.employee_selected.emit(employee_id)
    
    def clear_selection(self):
        """Clear table selection"""
        self.table.clearSelection()
    
    def refresh(self):
        """Refresh the table display"""
        self._update_table(self.employees_data)
