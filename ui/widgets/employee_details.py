"""
Employee details widget
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGridLayout
)
from PySide6.QtCore import Qt, Signal
from database.models import Employee
import config


class EmployeeDetailsWidget(QWidget):
    """Widget for displaying employee details in a minimalist profile view"""
    
    edit_clicked = Signal(int)
    delete_clicked = Signal(int)
    report_clicked = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.employee = None
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Header with Name and Actions
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)
        
        # Name and ID container
        name_container = QVBoxLayout()
        name_container.setSpacing(5)
        
        self.name_label = QLabel("Seleccione un empleado")
        self.name_label.setStyleSheet(f"font-size: 32px; font-weight: 300; color: {config.COLORS['text_primary']};")
        
        self.id_label = QLabel("--")
        self.id_label.setStyleSheet(f"color: {config.COLORS['primary']}; font-weight: 500; font-size: 14px; letter-spacing: 1px;")
        
        name_container.addWidget(self.name_label)
        name_container.addWidget(self.id_label)
        
        header_layout.addLayout(name_container)
        header_layout.addStretch()
        
        # Action Buttons
        self.report_btn = QPushButton("GENERAR REPORTE")
        self.report_btn.setObjectName("reportButton")
        self.report_btn.setStyleSheet(f"""
            QPushButton#reportButton {{
                background-color: {config.COLORS['info']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton#reportButton:hover {{
                background-color: #0ea5e9;
            }}
            QPushButton#reportButton:disabled {{
                background-color: {config.COLORS['bg_medium']};
                color: {config.COLORS['text_muted']};
            }}
        """)
        self.report_btn.clicked.connect(self._on_report)
        self.report_btn.setEnabled(False)
        self.report_btn.setCursor(Qt.PointingHandCursor)
        
        self.edit_btn = QPushButton("EDITAR")
        self.edit_btn.setObjectName("editButton")
        self.edit_btn.clicked.connect(self._on_edit)
        self.edit_btn.setEnabled(False)
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        
        self.delete_btn = QPushButton("ELIMINAR")
        self.delete_btn.setObjectName("deleteButton")
        self.delete_btn.clicked.connect(self._on_delete)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        
        header_layout.addWidget(self.report_btn)
        header_layout.addWidget(self.edit_btn)
        header_layout.addWidget(self.delete_btn)
        
        layout.addLayout(header_layout)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet(f"background-color: {config.COLORS['border']}; max-height: 1px;")
        layout.addWidget(divider)
        
        # Details Grid
        details_grid = QGridLayout()
        details_grid.setSpacing(30)
        details_grid.setContentsMargins(0, 10, 0, 0)
        
        # Department
        self.dept_label = self._create_detail_item("Departamento", "--")
        details_grid.addLayout(self.dept_label, 0, 0)
        
        # Position
        self.pos_label = self._create_detail_item("Puesto", "--")
        details_grid.addLayout(self.pos_label, 0, 1)
        
        # Email
        self.email_label = self._create_detail_item("Email", "--")
        details_grid.addLayout(self.email_label, 1, 0)
        
        # Phone
        self.phone_label = self._create_detail_item("Teléfono", "--")
        details_grid.addLayout(self.phone_label, 1, 1)
        
        # Entry Date
        self.entry_date_label = self._create_detail_item("Fecha de Ingreso", "--")
        details_grid.addLayout(self.entry_date_label, 2, 0)
        
        # Service Time
        self.service_time_label = self._create_detail_item("Años de Servicio", "--")
        details_grid.addLayout(self.service_time_label, 2, 1)
        
        layout.addLayout(details_grid)
        layout.addStretch()
    
    def _create_detail_item(self, label_text: str, value_text: str) -> QVBoxLayout:
        """Create a detail item layout"""
        container = QVBoxLayout()
        container.setSpacing(4)
        
        label = QLabel(label_text)
        label.setStyleSheet(f"color: {config.COLORS['text_secondary']}; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;")
        
        value = QLabel(value_text)
        value.setObjectName("detailValue")
        value.setStyleSheet(f"color: {config.COLORS['text_primary']}; font-size: 16px; font-weight: 400;")
        
        container.addWidget(label)
        container.addWidget(value)
        
        return container
    
    def set_employee(self, employee: Employee, vacation_info: dict = None):
        """Set the employee to display"""
        self.employee = employee
        
        self.name_label.setText(employee.full_name)
        self.id_label.setText(f"ID: {employee.employee_number}")
        
        # Update details directly accessing the value label (second item in layout)
        self.dept_label.itemAt(1).widget().setText(employee.department or "--")
        self.pos_label.itemAt(1).widget().setText(employee.position or "--")
        self.email_label.itemAt(1).widget().setText(employee.email or "--")
        self.phone_label.itemAt(1).widget().setText(employee.phone or "--")
        
        # Entry date
        entry_date = employee.entry_date
        if hasattr(entry_date, 'strftime'):
            self.entry_date_label.itemAt(1).widget().setText(entry_date.strftime('%d/%m/%Y'))
        elif isinstance(entry_date, str) and '-' in entry_date:
            from datetime import datetime
            date_obj = datetime.strptime(entry_date, '%Y-%m-%d')
            self.entry_date_label.itemAt(1).widget().setText(date_obj.strftime('%d/%m/%Y'))
        else:
            self.entry_date_label.itemAt(1).widget().setText(str(entry_date))
        
        # Service time
        if vacation_info:
            years = vacation_info.get('service_years', vacation_info.get('completed_years', 0))
            months = vacation_info.get('service_months', 0)
            
            years_str = f"{years} año{'s' if years != 1 else ''}"
            
            if months > 0:
                months_str = f"{months} mes{'es' if months != 1 else ''}"
                display_str = f"{years_str} {months_str}"
            else:
                display_str = years_str
                
            self.service_time_label.itemAt(1).widget().setText(display_str)
        else:
            self.service_time_label.itemAt(1).widget().setText("--")
        
        self.edit_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)
        self.report_btn.setEnabled(True)
    
    def clear(self):
        """Clear the display"""
        self.employee = None
        self.name_label.setText("Seleccione un empleado")
        self.id_label.setText("--")
        
        self.dept_label.itemAt(1).widget().setText("--")
        self.pos_label.itemAt(1).widget().setText("--")
        self.email_label.itemAt(1).widget().setText("--")
        self.phone_label.itemAt(1).widget().setText("--")
        self.entry_date_label.itemAt(1).widget().setText("--")
        self.service_time_label.itemAt(1).widget().setText("--")
        
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.report_btn.setEnabled(False)
    
    def _on_edit(self):
        """Handle edit button click"""
        if self.employee:
            self.edit_clicked.emit(self.employee.id)
    
    def _on_delete(self):
        """Handle delete button click"""
        if self.employee:
            self.delete_clicked.emit(self.employee.id)

    def _on_report(self):
        """Handle report button click"""
        if self.employee:
            self.report_clicked.emit(self.employee.id)
