"""
Vacation records widget for displaying and managing vacation records
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel, QPushButton, QHeaderView, QMessageBox,
    QFrame
)
from PySide6.QtCore import Qt, Signal
from typing import List
from database.models import VacationRecord
from datetime import datetime
import config


class VacationRecordsWidget(QWidget):
    """Widget for displaying and managing vacation records"""
    
    record_added = Signal(object)  # Emitted when a record is added (passes the new record)
    record_updated = Signal()  # Emitted when a record is updated
    record_deleted = Signal()  # Emitted when a record is deleted
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.employee_id = None
        self.employee_name = ""
        self.records = []
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Header with title and add button
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("REGISTROS DE VACACIONES")
        self.title_label.setObjectName("sectionHeader")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        self.add_btn = QPushButton("REGISTRAR VACACIONES")
        self.add_btn.setObjectName("addButton")
        self.add_btn.clicked.connect(self._on_add_record)
        self.add_btn.setEnabled(False)
        self.add_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(self.add_btn)
        
        layout.addLayout(header_layout)
        
        # Info label
        self.info_label = QLabel("Seleccione un empleado para ver sus registros")
        self.info_label.setStyleSheet(f"color: {config.COLORS['text_muted']}; font-size: {config.FONT_SIZE_SMALL}px;")
        layout.addWidget(self.info_label)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "PERIODO",
            "INICIO",
            "FIN",
            "DÍAS",
            "DESCRIPCIÓN"
        ])
        
        # Configure table
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(False) # Minimalist: no alternating colors
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False) # Minimalist: no grid
        self.table.setFrameShape(QFrame.NoFrame) # Minimalist: no border
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        layout.addWidget(self.table)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.edit_btn = QPushButton("EDITAR")
        self.edit_btn.setObjectName("editButton")
        self.edit_btn.clicked.connect(self._on_edit_record)
        self.edit_btn.setEnabled(False)
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        
        self.delete_btn = QPushButton("ELIMINAR")
        self.delete_btn.setObjectName("deleteButton")
        self.delete_btn.clicked.connect(self._on_delete_record)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        
        # Total label
        self.total_label = QLabel("Total días tomados: 0.0")
        self.total_label.setStyleSheet(f"color: {config.COLORS['text_primary']}; font-weight: 500; font-size: {config.FONT_SIZE_LARGE}px;")
        button_layout.addWidget(self.total_label)
        
        layout.addLayout(button_layout)
        
        # Connect selection
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
    
    def set_employee(self, employee_id: int, employee_name: str):
        """Set the employee for this widget"""
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.add_btn.setEnabled(True)
        self.info_label.setText(f"Registros de vacaciones de: {employee_name}")
    
    def set_records(self, records: List[VacationRecord]):
        """Set the list of vacation records"""
        self.records = records
        self._update_table()
    
    def _update_table(self):
        """Update table with records"""
        self.table.setRowCount(0)
        total_days = 0.0
        
        for record in self.records:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Period (Year)
            # Calculate period range based on year and employee entry date
            period_str = str(record.year)
            if self.employee_id:
                # We need entry date to calculate full period string
                # Ideally this would be passed or fetched, but for now we show Year-Year+1
                # Or we can fetch the employee if needed, but that might be slow in loop
                # Let's try to get it from parent or service if possible, 
                # but for simplicity/performance let's show "YYYY - YYYY+1"
                # assuming standard annual periods.
                # To be precise we need the entry month/day.
                pass
                
            item = QTableWidgetItem(f"{record.year} - {record.year + 1}")
            item.setData(Qt.UserRole, record.id)
            self.table.setItem(row, 0, item)
            
            # Start date
            start_date = record.start_date
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            self.table.setItem(row, 1, QTableWidgetItem(start_date.strftime('%d/%m/%Y')))
            
            # End date
            end_date = record.end_date
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            self.table.setItem(row, 2, QTableWidgetItem(end_date.strftime('%d/%m/%Y')))
            
            # Days taken
            self.table.setItem(row, 3, QTableWidgetItem(f"{record.days_taken:.1f}"))
            total_days += record.days_taken
            
            # Description
            desc = record.description or ""
            self.table.setItem(row, 4, QTableWidgetItem(desc))
        
        self.total_label.setText(f"Total días tomados: {total_days:.1f}")
    
    def _on_selection_changed(self):
        """Handle row selection"""
        has_selection = len(self.table.selectedItems()) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
    
    def _on_add_record(self):
        """Handle add record button"""
        if not self.employee_id:
            return
        
        from ui.widgets.vacation_record_form import VacationRecordFormDialog
        
        dialog = VacationRecordFormDialog(self, employee_id=self.employee_id)
        if dialog.exec():
            record = dialog.get_record()
            self.record_added.emit(record)
    
    def _on_edit_record(self):
        """Handle edit record button"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        record_id = self.table.item(row, 0).data(Qt.UserRole)
        
        # Find the record
        record = next((r for r in self.records if r.id == record_id), None)
        if not record:
            return
        
        from ui.widgets.vacation_record_form import VacationRecordFormDialog
        
        dialog = VacationRecordFormDialog(self, employee_id=self.employee_id, record=record)
        if dialog.exec():
            self.record_updated.emit()
    
    def _on_delete_record(self):
        """Handle delete record button"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        record_id = self.table.item(row, 0).data(Qt.UserRole)
        
        # Find the record
        record = next((r for r in self.records if r.id == record_id), None)
        if not record:
            return
        
        # Confirm deletion
        start_date = record.start_date
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el registro de vacaciones?\n\n"
            f"Fecha: {start_date.strftime('%d/%m/%Y')}\n"
            f"Días: {record.days_taken:.1f}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.record_deleted.emit()
    
    def get_selected_record_id(self) -> int:
        """Get the ID of the selected record"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            return None
        
        row = selected_items[0].row()
        return self.table.item(row, 0).data(Qt.UserRole)
    
    def clear(self):
        """Clear the widget"""
        self.employee_id = None
        self.employee_name = ""
        self.records = []
        self.table.setRowCount(0)
        self.add_btn.setEnabled(False)
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.info_label.setText("Seleccione un empleado para ver sus registros de vacaciones")
        self.total_label.setText("Total días tomados: 0.0 días")
