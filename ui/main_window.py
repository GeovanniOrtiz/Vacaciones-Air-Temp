"""
Main application window
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QMessageBox, QStatusBar, QMenuBar, QMenu, QToolBar,
    QTabWidget, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from ui.widgets.employee_list import EmployeeListWidget
from ui.widgets.employee_details import EmployeeDetailsWidget
from ui.widgets.vacation_display import VacationDisplayWidget
from ui.widgets.vacation_records import VacationRecordsWidget
from ui.widgets.employee_form import EmployeeFormDialog
from business.employee_service import EmployeeService
from business.report_generator import ReportGenerator
from ui.styles.modern_style import get_stylesheet
import config


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.employee_service = EmployeeService()
        self.current_employee_data = None
        
        self._init_ui()
        self._create_menu_bar()
        self._create_toolbar()
        self._load_employees()
    
    def _init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"{config.APP_NAME} - {config.COMPANY_NAME}")
        self.setMinimumSize(
            config.WINDOW_MIN_WIDTH,
            config.WINDOW_MIN_HEIGHT
        )
        self.resize(
            config.WINDOW_DEFAULT_WIDTH,
            config.WINDOW_DEFAULT_HEIGHT
        )
        
        # Apply stylesheet
        self.setStyleSheet(get_stylesheet())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel: Employee list
        self.employee_list = EmployeeListWidget()
        self.employee_list.setMinimumWidth(750)
        self.employee_list.employee_selected.connect(self._on_employee_selected)
        self.employee_list.add_employee_clicked.connect(self._on_add_employee)
        splitter.addWidget(self.employee_list)
        
        # Right panel: Details and vacation info
        right_panel = QWidget()
        right_panel.setMinimumWidth(400)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(16)
        
        # Employee details (Always visible at top)
        self.employee_details = EmployeeDetailsWidget()
        self.employee_details.edit_clicked.connect(self._on_edit_employee)
        self.employee_details.delete_clicked.connect(self._on_delete_employee)
        self.employee_details.report_clicked.connect(self._on_generate_report)
        right_layout.addWidget(self.employee_details)
        
        # Tabs for Vacation Info and History
        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")
        
        # Tab 1: Summary
        self.vacation_display = VacationDisplayWidget()
        self.tabs.addTab(self.vacation_display, "Resumen de Vacaciones")
        
        # Tab 2: History
        self.vacation_records = VacationRecordsWidget()
        self.vacation_records.record_added.connect(self._on_vacation_record_added)
        self.vacation_records.record_updated.connect(self._on_vacation_record_updated)
        self.vacation_records.record_deleted.connect(self._on_vacation_record_deleted)
        self.tabs.addTab(self.vacation_records, "Historial de Registros")
        
        right_layout.addWidget(self.tabs)
        
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([650, 950])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo")
    
    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("Archivo")
        
        add_action = QAction("Agregar Empleado", self)
        add_action.setShortcut("Ctrl+N")
        add_action.triggered.connect(self._on_add_employee)
        file_menu.addAction(add_action)
        
        file_menu.addSeparator()
        
        refresh_action = QAction("Actualizar", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._load_employees)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Ayuda")
        
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self):
        """Create toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Add employee button
        add_action = QAction("+ Agregar Empleado", self)
        add_action.triggered.connect(self._on_add_employee)
        toolbar.addAction(add_action)
        
        toolbar.addSeparator()
        
        # Refresh button
        refresh_action = QAction("🔄 Actualizar", self)
        refresh_action.triggered.connect(self._load_employees)
        toolbar.addAction(refresh_action)
    
    def _load_employees(self):
        """Load all employees from database"""
        try:
            employees_data = self.employee_service.get_all_employees_with_vacation()
            self.employee_list.set_employees(employees_data)
            self.status_bar.showMessage(
                f"Cargados {len(employees_data)} empleado(s)",
                3000
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al cargar empleados: {str(e)}"
            )
    
    def _on_employee_selected(self, employee_id: int):
        """Handle employee selection"""
        try:
            employee = self.employee_service.get_employee_by_id(employee_id)
            if employee:
                self.current_employee_data = self.employee_service.get_employee_with_vacation_info(employee)
                
                # Update details panel
                self.employee_details.set_employee(employee, self.current_employee_data['vacation_info'])
                
                # Update vacation display
                self.vacation_display.set_vacation_info(
                    self.current_employee_data['vacation_info']
                )
                
                # Load vacation records
                records = self.employee_service.get_vacation_records(employee.id)
                self.vacation_records.set_employee(employee.id, employee.full_name)
                self.vacation_records.set_records(records)
                
                self.status_bar.showMessage(
                    f"Empleado seleccionado: {employee.full_name}",
                    3000
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al cargar empleado: {str(e)}"
            )
    
    def _on_add_employee(self):
        """Handle add employee action"""
        dialog = EmployeeFormDialog(self)
        
        if dialog.exec():
            employee = dialog.get_employee()
            if employee:
                success, message, employee_id = self.employee_service.create_employee(employee)
                
                if success:
                    QMessageBox.information(self, "Éxito", message)
                    self._load_employees()
                    self.status_bar.showMessage(message, 3000)
                else:
                    QMessageBox.warning(self, "Error", message)
    
    def _on_edit_employee(self, employee_id: int):
        """Handle edit employee action"""
        try:
            employee = self.employee_service.get_employee_by_id(employee_id)
            if not employee:
                QMessageBox.warning(self, "Error", "Empleado no encontrado")
                return
            
            dialog = EmployeeFormDialog(self, employee)
            
            if dialog.exec():
                updated_employee = dialog.get_employee()
                if updated_employee:
                    success, message = self.employee_service.update_employee(updated_employee)
                    
                    if success:
                        QMessageBox.information(self, "Éxito", message)
                        self._load_employees()
                        self._on_employee_selected(employee_id)
                        self.status_bar.showMessage(message, 3000)
                    else:
                        QMessageBox.warning(self, "Error", message)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al editar empleado: {str(e)}"
            )
    
    def _on_delete_employee(self, employee_id: int):
        """Handle delete employee action"""
        try:
            employee = self.employee_service.get_employee_by_id(employee_id)
            if not employee:
                QMessageBox.warning(self, "Error", "Empleado no encontrado")
                return
            
            # Confirm deletion
            reply = QMessageBox.question(
                self,
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar al empleado '{employee.full_name}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success, message = self.employee_service.delete_employee(employee_id)
                
                if success:
                    QMessageBox.information(self, "Éxito", message)
                    self._load_employees()
                    self.employee_details.clear()
                    self.vacation_display.clear()
                    self.vacation_records.clear()
                    self.status_bar.showMessage(message, 3000)
                else:
                    QMessageBox.warning(self, "Error", message)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al eliminar empleado: {str(e)}"
            )
    
    def _on_vacation_record_added(self, record):
        """Handle vacation record added"""
        try:
            if record:
                success, message, record_id = self.employee_service.create_vacation_record(record)
                
                if success:
                    QMessageBox.information(self, "Éxito", message)
                    # Refresh employee data to update vacation summary
                    if self.current_employee_data:
                        employee_id = self.current_employee_data['employee'].id
                        self._on_employee_selected(employee_id)
                        self._load_employees()  # Refresh list to show updated remaining days
                    self.status_bar.showMessage(message, 3000)
                else:
                    QMessageBox.warning(self, "Error", message)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al agregar registro: {str(e)}"
            )
    
    def _on_vacation_record_updated(self):
        """Handle vacation record updated"""
        try:
            # Get selected record
            record_id = self.vacation_records.get_selected_record_id()
            if not record_id:
                return
            
            # Get the record from service
            records = self.vacation_records.records
            record = next((r for r in records if r.id == record_id), None)
            if not record:
                return
            
            success, message = self.employee_service.update_vacation_record(record)
            
            if success:
                QMessageBox.information(self, "Éxito", message)
                # Refresh employee data
                if self.current_employee_data:
                    employee_id = self.current_employee_data['employee'].id
                    self._on_employee_selected(employee_id)
                    self._load_employees()
                self.status_bar.showMessage(message, 3000)
            else:
                QMessageBox.warning(self, "Error", message)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al actualizar registro: {str(e)}"
            )
    
    def _on_vacation_record_deleted(self):
        """Handle vacation record deleted"""
        try:
            record_id = self.vacation_records.get_selected_record_id()
            if not record_id:
                return
            
            success, message = self.employee_service.delete_vacation_record(record_id)
            
            if success:
                QMessageBox.information(self, "Éxito", message)
                # Refresh employee data
                if self.current_employee_data:
                    employee_id = self.current_employee_data['employee'].id
                    self._on_employee_selected(employee_id)
                    self._load_employees()
                self.status_bar.showMessage(message, 3000)
            else:
                QMessageBox.warning(self, "Error", message)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al eliminar registro: {str(e)}"
            )
    
    def _on_generate_report(self, employee_id: int):
        """Handle report generation"""
        try:
            employee = self.employee_service.get_employee_by_id(employee_id)
            if not employee:
                QMessageBox.warning(self, "Error", "Empleado no encontrado")
                return
            
            # Get vacation info
            vacation_data = self.employee_service.get_employee_with_vacation_info(employee)
            vacation_info = vacation_data['vacation_info']
            
            # Get records
            records = self.employee_service.get_vacation_records(employee.id)
            
            # Ask for file path
            filename = f"Reporte_Vacaciones_{employee.full_name.replace(' ', '_')}.pdf"
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Reporte",
                filename,
                "Archivos PDF (*.pdf)"
            )
            
            if filepath:
                ReportGenerator.generate_employee_report(
                    employee,
                    vacation_info,
                    records,
                    filepath
                )
                
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"Reporte generado exitosamente en:\n{filepath}"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al generar reporte: {str(e)}"
            )
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            f"Acerca de {config.APP_NAME}",
            f"""
            <h2>{config.APP_NAME}</h2>
            <p>Versión {config.APP_VERSION}</p>
            <p>{config.COMPANY_NAME}</p>
            <br>
            <p>Sistema profesional para el control de vacaciones de empleados</p>
            <p>basado en la Ley Federal del Trabajo de México 2025.</p>
            <br>
            <p>Desarrollado con PySide6</p>
            """
        )

