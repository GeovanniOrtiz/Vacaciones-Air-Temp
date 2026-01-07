"""
Vacation record form dialog for adding/editing vacation records
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QPushButton, QLabel, QMessageBox, 
    QDateEdit, QDoubleSpinBox, QTextEdit
)
from PySide6.QtCore import Qt, QDate
from datetime import datetime, date
from database.models import VacationRecord
from typing import Optional
import config


class VacationRecordFormDialog(QDialog):
    """Dialog for adding or editing vacation records"""
    
    def __init__(self, parent=None, employee_id: int = None, record: Optional[VacationRecord] = None):
        super().__init__(parent)
        self.employee_id = employee_id
        self.record = record
        self.is_edit_mode = record is not None
        self.employee_entry_date = None
        
        # Fetch employee entry date
        if employee_id:
            from business.employee_service import EmployeeService
            service = EmployeeService()
            employee = service.get_employee_by_id(employee_id)
            if employee:
                self.employee_entry_date = employee.entry_date
        
        self._init_ui()
        
        if self.is_edit_mode:
            self._populate_form()
        else:
            # Initial calculation for default date
            self._on_date_changed()
    
    def _init_ui(self):
        """Initialize the user interface"""
        title = "Editar Registro de Vacaciones" if self.is_edit_mode else "Registrar Vacaciones Tomadas"
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
        
        # Start date
        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDisplayFormat("dd/MM/yyyy")
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.dateChanged.connect(self._on_date_changed)
        form_layout.addRow("Fecha Inicio: *", self.start_date_input)
        
        # End date
        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDisplayFormat("dd/MM/yyyy")
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.dateChanged.connect(self._on_date_changed)
        form_layout.addRow("Fecha Fin: *", self.end_date_input)
        
        # Period Display (Read-only)
        self.period_label = QLabel("--")
        self.period_label.setStyleSheet(f"color: {config.COLORS['primary']}; font-weight: 600;")
        form_layout.addRow("Periodo:", self.period_label)
        
        # Hidden year field (stores the period start year)
        self.period_year = datetime.now().year
        
        # Days taken (auto-calculated but editable)
        self.days_taken_input = QDoubleSpinBox()
        self.days_taken_input.setRange(0.5, 365)
        self.days_taken_input.setSingleStep(0.5)
        self.days_taken_input.setDecimals(1)
        self.days_taken_input.setValue(1.0)
        form_layout.addRow("Días Tomados: *", self.days_taken_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Opcional: Motivo o notas sobre estas vacaciones")
        self.description_input.setMaximumHeight(80)
        form_layout.addRow("Descripción:", self.description_input)
        
        layout.addLayout(form_layout)
        
        # Info label
        self.info_label = QLabel("Los días se calcularán automáticamente según las fechas")
        self.info_label.setStyleSheet(f"color: {config.COLORS['text_muted']}; font-size: {config.FONT_SIZE_SMALL}px;")
        layout.addWidget(self.info_label)
        
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
    
    def _on_date_changed(self):
        """Auto-calculate days and period when dates change"""
        start_qdate = self.start_date_input.date()
        end_qdate = self.end_date_input.date()
        
        start_date = date(start_qdate.year(), start_qdate.month(), start_qdate.day())
        end_date = date(end_qdate.year(), end_qdate.month(), end_qdate.day())
        
        # Calculate days
        if end_date >= start_date:
            days = (end_date - start_date).days + 1  # Include both start and end day
            self.days_taken_input.setValue(float(days))
            self.info_label.setText(f"✓ Calculado: {days} día(s) entre las fechas seleccionadas")
            self.info_label.setStyleSheet(f"color: {config.COLORS['success']}; font-size: {config.FONT_SIZE_SMALL}px;")
        else:
            self.info_label.setText("⚠ La fecha de fin debe ser posterior o igual a la fecha de inicio")
            self.info_label.setStyleSheet(f"color: {config.COLORS['error']}; font-size: {config.FONT_SIZE_SMALL}px;")
            
        # Calculate Service Period
        if self.employee_entry_date:
            from business.vacation_calculator import VacationCalculator
            p_start, p_end, p_year = VacationCalculator.get_service_period(self.employee_entry_date, start_date)
            self.period_year = p_year
            self.period_label.setText(f"{p_start.strftime('%d/%m/%Y')} - {p_end.strftime('%d/%m/%Y')} (Año {p_year})")
    
    def _populate_form(self):
        """Populate form with record data (edit mode)"""
        if not self.record:
            return
        
        # Set start date
        start_date = self.record.start_date
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        start_qdate = QDate(start_date.year, start_date.month, start_date.day)
        self.start_date_input.setDate(start_qdate)
        
        # Set end date
        end_date = self.record.end_date
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        end_qdate = QDate(end_date.year, end_date.month, end_date.day)
        self.end_date_input.setDate(end_qdate)
        
        self.days_taken_input.setValue(self.record.days_taken)
        
        if self.record.description:
            self.description_input.setPlainText(self.record.description)
            
        # Trigger calculation to update period label
        self._on_date_changed()
    
    def _on_save(self):
        """Validate and save vacation record"""
        # Get values
        start_qdate = self.start_date_input.date()
        start_date = date(start_qdate.year(), start_qdate.month(), start_qdate.day())
        
        end_qdate = self.end_date_input.date()
        end_date = date(end_qdate.year(), end_qdate.month(), end_qdate.day())
        
        days_taken = self.days_taken_input.value()
        description = self.description_input.toPlainText().strip() or None
        
        # Validate
        if end_date < start_date:
            QMessageBox.warning(
                self,
                "Error de Validación",
                "La fecha de fin debe ser posterior o igual a la fecha de inicio."
            )
            return
        
        if days_taken <= 0:
            QMessageBox.warning(
                self,
                "Error de Validación",
                "Los días tomados deben ser mayor a 0."
            )
            return
        
        # Create or update record
        try:
            if self.is_edit_mode:
                # Update existing record
                self.record.year = self.period_year
                self.record.start_date = start_date
                self.record.end_date = end_date
                self.record.days_taken = days_taken
                self.record.description = description
            else:
                # Create new record
                self.record = VacationRecord(
                    employee_id=self.employee_id,
                    year=self.period_year,
                    start_date=start_date,
                    end_date=end_date,
                    days_taken=days_taken,
                    description=description
                )
            
            self.accept()
            
        except ValueError as e:
            QMessageBox.warning(
                self,
                "Error de Validación",
                str(e)
            )
    
    def get_record(self) -> Optional[VacationRecord]:
        """Get the vacation record object"""
        return self.record
