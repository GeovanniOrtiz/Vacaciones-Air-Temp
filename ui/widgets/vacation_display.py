"""
Vacation display widget for showing vacation information
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QProgressBar, QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from typing import Dict
import config


class VacationDisplayWidget(QWidget):
    """Widget for displaying vacation information in a minimalist dashboard"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)
        
        # Header
        header = QLabel("Resumen de Vacaciones")
        header.setObjectName("sectionHeader")
        layout.addWidget(header)
        
        # Metrics Container (Clean Grid)
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(40)
        
        # Total Days
        self.total_metric = self._create_minimal_metric("Días Totales", "--", config.COLORS['primary'])
        metrics_layout.addLayout(self.total_metric['layout'])
        
        # Taken Days
        self.taken_metric = self._create_minimal_metric("Días Tomados", "--", config.COLORS['warning'])
        metrics_layout.addLayout(self.taken_metric['layout'])
        
        # Remaining Days
        self.remaining_metric = self._create_minimal_metric("Días Restantes", "--", config.COLORS['success'])
        metrics_layout.addLayout(self.remaining_metric['layout'])
        
        metrics_layout.addStretch()
        layout.addLayout(metrics_layout)
        
        # Secondary Metrics (Years, Entry, Premium)
        secondary_layout = QHBoxLayout()
        secondary_layout.setSpacing(40)
        
        # Years of Service
        self.years_metric = self._create_secondary_metric("Años de Servicio", "--")
        secondary_layout.addLayout(self.years_metric['layout'])
        
        # Entry Date
        self.entry_metric = self._create_secondary_metric("Fecha de Ingreso", "--")
        secondary_layout.addLayout(self.entry_metric['layout'])
        
        # Premium
        self.premium_metric = self._create_secondary_metric("Prima Vacacional", "--")
        secondary_layout.addLayout(self.premium_metric['layout'])
        
        secondary_layout.addStretch()
        layout.addLayout(secondary_layout)
        
        # Progress Section
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(8)
        
        progress_header = QHBoxLayout()
        progress_title = QLabel("Progreso de Uso")
        progress_title.setStyleSheet(f"color: {config.COLORS['text_secondary']}; font-size: {config.FONT_SIZE_SMALL}px; text-transform: uppercase; letter-spacing: 1px;")
        
        self.progress_label = QLabel("--")
        self.progress_label.setStyleSheet(f"color: {config.COLORS['text_muted']}; font-size: {config.FONT_SIZE_SMALL}px;")
        self.progress_label.setAlignment(Qt.AlignRight)
        
        progress_header.addWidget(progress_title)
        progress_header.addStretch()
        progress_header.addWidget(self.progress_label)
        
        progress_layout.addLayout(progress_header)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addLayout(progress_layout)
        
        layout.addStretch()
    
    def _create_minimal_metric(self, title: str, value: str, color: str) -> Dict:
        """Create a minimalist metric layout"""
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {config.COLORS['text_secondary']}; font-size: {config.FONT_SIZE_SMALL}px; text-transform: uppercase; letter-spacing: 1px;")
        
        value_lbl = QLabel(value)
        value_lbl.setObjectName("metricValue")
        value_lbl.setStyleSheet(f"color: {color}; font-size: 42px; font-weight: 300;")
        
        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        
        return {
            'layout': layout,
            'value_label': value_lbl
        }
    
    def _create_secondary_metric(self, title: str, value: str) -> Dict:
        """Create a secondary metric layout"""
        layout = QVBoxLayout()
        layout.setSpacing(2)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {config.COLORS['text_secondary']}; font-size: {config.FONT_SIZE_SMALL}px;")
        
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"color: {config.COLORS['text_primary']}; font-size: {config.FONT_SIZE_LARGE}px; font-weight: 500;")
        
        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        
        return {
            'layout': layout,
            'value_label': value_lbl
        }
    
    def set_vacation_info(self, vacation_info: Dict):
        """Set vacation information to display"""
        # Total, taken, and remaining days
        total_days = vacation_info.get('total_days', vacation_info.get('vacation_days', 0))
        days_taken = vacation_info.get('days_taken', 0)
        days_remaining = vacation_info.get('days_remaining', total_days)
        
        self.total_metric['value_label'].setText(f"{total_days}")
        self.taken_metric['value_label'].setText(f"{days_taken:.1f}")
        self.remaining_metric['value_label'].setText(f"{days_remaining:.1f}")
        
        # Years of service
        years = vacation_info.get('service_years', vacation_info.get('completed_years', 0))
        months = vacation_info.get('service_months', 0)
        
        years_str = f"{years} año{'s' if years != 1 else ''}"
        
        if months > 0:
            months_str = f"{months} mes{'es' if months != 1 else ''}"
            self.years_metric['value_label'].setText(f"{years_str}, {months_str}")
        else:
            self.years_metric['value_label'].setText(years_str)
        
        # Entry date
        entry_date = vacation_info.get('entry_date', vacation_info.get('entry_year'))
        if hasattr(entry_date, 'strftime'):
            self.entry_metric['value_label'].setText(entry_date.strftime('%d/%m/%Y'))
        elif isinstance(entry_date, str) and '-' in entry_date:
            from datetime import datetime
            date_obj = datetime.strptime(entry_date, '%Y-%m-%d')
            self.entry_metric['value_label'].setText(date_obj.strftime('%d/%m/%Y'))
        else:
            self.entry_metric['value_label'].setText(str(entry_date))
        
        # Vacation premium
        premium = vacation_info['vacation_premium_days']
        self.premium_metric['value_label'].setText(f"{premium:.1f} días")
        
        # Progress bar - usage percentage
        usage_percentage = vacation_info.get('usage_percentage', 0)
        self.progress_bar.setValue(int(usage_percentage))
        
        # Progress label
        next_increase = vacation_info['next_increase_years']
        next_days = vacation_info['next_vacation_days']
        self.progress_label.setText(
            f"Próximo aumento en {next_increase} año(s): {next_days} días"
        )
    
    def clear(self):
        """Clear all displayed information"""
        self.total_metric['value_label'].setText("--")
        self.taken_metric['value_label'].setText("--")
        self.remaining_metric['value_label'].setText("--")
        self.years_metric['value_label'].setText("--")
        self.entry_metric['value_label'].setText("--")
        self.premium_metric['value_label'].setText("--")
        self.progress_bar.setValue(0)
        self.progress_label.setText("--")
