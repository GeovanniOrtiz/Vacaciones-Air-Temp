"""
Employee form dialog for adding/editing employees
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QPushButton, QLabel, QMessageBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from datetime import datetime, date
from database.models import Employee
from typing import Optional
import config


class EmployeeFormDialog(QDialog):
    """Dialog for adding or editing employee information"""
    
    def __init__(self, parent=None, employee: Optional[Employee] = None):
        super().__init__(parent)
        self.employee = employee
        self.is_edit_mode = employee is not None
        
        self._init_ui()
        
        if self.is_edit_mode:
            self._populate_form()
    
    def _init_ui(self):
        """Initialize the user interface"""
        title = "Editar Empleado" if self.is_edit_mode else "Agregar Empleado"
        self.setWindowTitle(title)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # Employee number
        self.employee_number_input = QLineEdit()
        self.employee_number_input.setPlaceholderText("Ej: EMP001")
        form_layout.addRow("Número de Empleado: *", self.employee_number_input)
        
        # Full name
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText("Nombre completo del empleado")
        form_layout.addRow("Nombre Completo: *", self.full_name_input)
        
        # Entry date
        self.entry_date_input = QDateEdit()
        self.entry_date_input.setCalendarPopup(True)
        self.entry_date_input.setDisplayFormat("dd/MM/yyyy")
        self.entry_date_input.setDate(QDate.currentDate())
        self.entry_date_input.setMaximumDate(QDate.currentDate())
        form_layout.addRow("Fecha de Entrada: *", self.entry_date_input)
        
        # Department
        self.department_input = QLineEdit()
        self.department_input.setPlaceholderText("Opcional")
        form_layout.addRow("Departamento:", self.department_input)
        
        # Position
        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText("Opcional")
        form_layout.addRow("Puesto:", self.position_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Opcional")
        form_layout.addRow("Email:", self.email_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Opcional")
        form_layout.addRow("Teléfono:", self.phone_input)
        
        layout.addLayout(form_layout)
        
        # Required fields note
        note_label = QLabel("* Campos requeridos")
        note_label.setStyleSheet(f"color: {config.COLORS['text_muted']}; font-size: {config.FONT_SIZE_SMALL}px;")
        layout.addWidget(note_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Guardar")
        save_btn.setObjectName("addButton")
        save_btn.clicked.connect(self._on_save)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def _populate_form(self):
        """Populate form with employee data (edit mode)"""
        if not self.employee:
            return
        
        self.employee_number_input.setText(self.employee.employee_number)
        self.full_name_input.setText(self.employee.full_name)
        
        # Set entry date
        entry_date = self.employee.entry_date
        if isinstance(entry_date, str):
            entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
        qdate = QDate(entry_date.year, entry_date.month, entry_date.day)
        self.entry_date_input.setDate(qdate)
        
        if self.employee.department:
            self.department_input.setText(self.employee.department)
        if self.employee.position:
            self.position_input.setText(self.employee.position)
        if self.employee.email:
            self.email_input.setText(self.employee.email)
        if self.employee.phone:
            self.phone_input.setText(self.employee.phone)
    
    def _on_save(self):
        """Validate and save employee data"""
        # Get values
        employee_number = self.employee_number_input.text().strip()
        full_name = self.full_name_input.text().strip()
        
        # Get entry date from QDateEdit
        qdate = self.entry_date_input.date()
        entry_date = date(qdate.year(), qdate.month(), qdate.day())
        
        department = self.department_input.text().strip() or None
        position = self.position_input.text().strip() or None
        email = self.email_input.text().strip() or None
        phone = self.phone_input.text().strip() or None
        
        # Validate required fields
        if not employee_number:
            QMessageBox.warning(
                self,
                "Campo Requerido",
                "El número de empleado es requerido."
            )
            self.employee_number_input.setFocus()
            return
        
        if not full_name:
            QMessageBox.warning(
                self,
                "Campo Requerido",
                "El nombre completo es requerido."
            )
            self.full_name_input.setFocus()
            return
        
        # Create or update employee object
        try:
            if self.is_edit_mode:
                # Update existing employee
                self.employee.employee_number = employee_number
                self.employee.full_name = full_name
                self.employee.entry_date = entry_date
                self.employee.department = department
                self.employee.position = position
                self.employee.email = email
                self.employee.phone = phone
            else:
                # Create new employee
                self.employee = Employee(
                    employee_number=employee_number,
                    full_name=full_name,
                    entry_date=entry_date,
                    department=department,
                    position=position,
                    email=email,
                    phone=phone
                )
            
            self.accept()
            
        except ValueError as e:
            QMessageBox.warning(
                self,
                "Error de Validación",
                str(e)
            )
    
    def get_employee(self) -> Optional[Employee]:
        """Get the employee object"""
        return self.employee
