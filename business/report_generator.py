"""
Report generator for employee vacation data
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import config
import os

# Spanish month names
SPANISH_MONTHS = {
    'January': 'enero', 'February': 'febrero', 'March': 'marzo',
    'April': 'abril', 'May': 'mayo', 'June': 'junio',
    'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
    'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
}

class ReportGenerator:
    """Generates PDF reports for employee vacation data"""
    
    # Professional color palette
    COLORS = {
        'primary': colors.HexColor('#1e40af'),      # Deep blue
        'primary_light': colors.HexColor('#3b82f6'), # Light blue
        'accent': colors.HexColor('#0891b2'),        # Teal
        'success': colors.HexColor('#059669'),       # Green
        'text_dark': colors.HexColor('#1f2937'),     # Dark gray
        'text_medium': colors.HexColor('#4b5563'),   # Medium gray
        'text_light': colors.HexColor('#6b7280'),    # Light gray
        'bg_light': colors.HexColor('#f9fafb'),      # Very light gray
        'bg_medium': colors.HexColor('#e5e7eb'),     # Light gray background
        'border': colors.HexColor('#d1d5db'),        # Border gray
    }
    
    @staticmethod
    def add_watermark(canvas, doc):
        """Add watermark logo to the first page"""
        canvas.saveState()
        
        # Logo as watermark in top right
        logo_path = os.path.join(config.BASE_DIR, 'assets', 'logo.jpg')
        if os.path.exists(logo_path):
            # Draw logo in top right corner with transparency
            # Page width is letter[0] (612), height is letter[1] (792)
            # Position: x = width - margin - logo_width, y = height - margin - logo_height
            logo_width = 1.2 * inch
            logo_height = 1.2 * inch
            x = letter[0] - 40 - logo_width
            y = letter[1] - 40 - logo_height
            
            # Set transparency (50%)
            canvas.setFillAlpha(0.5)
            
            canvas.drawImage(logo_path, x, y, width=logo_width, height=logo_height, mask='auto', preserveAspectRatio=True)
            
        canvas.restoreState()

    @staticmethod
    def generate_employee_report(employee, vacation_info, vacation_records, filepath):
        """
        Generate a PDF report for an employee
        
        Args:
            employee: Employee object
            vacation_info: Dictionary with vacation information
            vacation_records: List of VacationRecord objects
            filepath: Path to save the PDF file
        """
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=60,
            leftMargin=60,
            topMargin=80, # Increased top margin for logo space
            bottomMargin=60
        )
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Custom Styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=ReportGenerator.COLORS['primary'],
            alignment=TA_LEFT, # Left aligned for corporate look
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=ReportGenerator.COLORS['text_light'],
            alignment=TA_LEFT,
            spaceAfter=30
        )
        
        company_style = ParagraphStyle(
            'CompanyStyle',
            parent=styles['Normal'],
            fontSize=20,
            textColor=ReportGenerator.COLORS['accent'],
            alignment=TA_LEFT,
            spaceAfter=15,
            fontName='Helvetica-Bold'
        )
        
        dept_style = ParagraphStyle(
            'DeptStyle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=ReportGenerator.COLORS['text_medium'],
            alignment=TA_LEFT,
            spaceAfter=25,
            fontName='Helvetica'
        )
        
        section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=ReportGenerator.COLORS['primary'],
            spaceBefore=25,
            spaceAfter=15,
            fontName='Helvetica-Bold',
            borderPadding=8,
            leftIndent=0
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=ReportGenerator.COLORS['text_medium']
        )
        
        elements = []
        
        # 1. Header / Title
        # Logo is now handled in add_watermark
            
        #elements.append(Paragraph(config.COMPANY_NAME, company_style))
        #elements.append(Paragraph("Departamento de Integración", dept_style))
        elements.append(Paragraph("Reporte de Vacaciones", title_style))
        
        # Format date in Spanish
        now = datetime.now()
        month_english = now.strftime('%B')
        month_spanish = SPANISH_MONTHS.get(month_english, month_english)
        date_str = f"Generado el {now.strftime('%d')} de {month_spanish} de {now.strftime('%Y')} a las {now.strftime('%H:%M')}"
        elements.append(Paragraph(date_str, subtitle_style))

        elements.append(Paragraph(config.COMPANY_NAME, company_style))
        elements.append(Paragraph("Departamento de Integración", dept_style))
        
        # Decorative line
        elements.append(HRFlowable(width="100%", thickness=2, color=ReportGenerator.COLORS['primary_light'], spaceBefore=5, spaceAfter=20))
        
        # 2. Employee Info Section
        elements.append(Paragraph("Información del Empleado", section_header_style))
        
        # Prepare employee data for table
        emp_data = [
            ["Nombre Completo:", employee.full_name, "No. Empleado:", employee.employee_number],
            ["Departamento:", employee.department or "—", "Puesto:", employee.position or "—"],
            ["Fecha de Ingreso:", employee.entry_date.strftime('%d/%m/%Y') if hasattr(employee.entry_date, 'strftime') else str(employee.entry_date),
             "Email:", employee.email or "—"]
        ]
        
        emp_table = Table(emp_data, colWidths=[1.4*inch, 2.2*inch, 1.2*inch, 2.0*inch])
        emp_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), ReportGenerator.COLORS['text_dark']),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), ReportGenerator.COLORS['text_medium']),
            ('TEXTCOLOR', (2, 0), (2, -1), ReportGenerator.COLORS['text_medium']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, -1), ReportGenerator.COLORS['bg_light']),
            ('GRID', (0, 0), (-1, -1), 0.5, ReportGenerator.COLORS['border']),
            ('WORDWRAP', (0, 0), (-1, -1), True),
        ]))
        elements.append(emp_table)
        elements.append(Spacer(1, 25))
        
        # 3. Vacation Summary Section
        elements.append(Paragraph("Resumen de Vacaciones", section_header_style))
        
        # Service time formatting
        years = vacation_info.get('service_years', vacation_info.get('completed_years', 0))
        months = vacation_info.get('service_months', 0)
        years_str = f"{years} año{'s' if years != 1 else ''}"
        if months > 0:
            months_str = f"{months} mes{'es' if months != 1 else ''}"
            service_time_str = f"{years_str}, {months_str}"
        else:
            service_time_str = years_str
            
        summary_data = [
            ["Años de Servicio", "Días Totales", "Días Tomados", "Días Restantes"],
            [
                service_time_str,
                f"{vacation_info.get('total_days', 0)}",
                f"{vacation_info.get('days_taken', 0):.1f}",
                f"{vacation_info.get('days_remaining', 0):.1f}"
            ]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), ReportGenerator.COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            
            # Values row
            ('BACKGROUND', (0, 1), (-1, 1), colors.white),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, 1), 14),
            ('TEXTCOLOR', (0, 1), (0, 1), ReportGenerator.COLORS['text_dark']),
            ('TEXTCOLOR', (1, 1), (1, 1), ReportGenerator.COLORS['primary_light']),
            ('TEXTCOLOR', (2, 1), (2, 1), ReportGenerator.COLORS['accent']),
            ('TEXTCOLOR', (3, 1), (3, 1), ReportGenerator.COLORS['success']),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 14),
            ('TOPPADDING', (0, 1), (-1, 1), 14),
            ('GRID', (0, 0), (-1, -1), 1, ReportGenerator.COLORS['border']),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 25))
        
        # 4. Vacation History Section
        elements.append(Paragraph("Historial de Registros", section_header_style))
        
        if not vacation_records:
            no_records_para = Paragraph(
                "<i>No hay registros de vacaciones disponibles.</i>",
                normal_style
            )
            elements.append(no_records_para)
        else:
            # Table Header
            history_data = [["Fecha Inicio", "Fecha Fin", "Días Tomados", "Descripción"]]
            
            # Table Rows
            for record in vacation_records:
                start_str = record.start_date.strftime('%d/%m/%Y') if hasattr(record.start_date, 'strftime') else str(record.start_date)
                end_str = record.end_date.strftime('%d/%m/%Y') if hasattr(record.end_date, 'strftime') else str(record.end_date)
                
                history_data.append([
                    start_str,
                    end_str,
                    f"{record.days_taken:.1f}",
                    record.description or "—"
                ])
            
            # Create Table
            col_widths = [1.4*inch, 1.4*inch, 1.1*inch, 2.6*inch]
            history_table = Table(history_data, colWidths=col_widths, repeatRows=1)
            
            # Table Style
            table_style = [
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), ReportGenerator.COLORS['primary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                
                # Data rows
                ('ALIGN', (0, 1), (2, -1), 'CENTER'),
                ('ALIGN', (3, 1), (3, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TEXTCOLOR', (0, 1), (-1, -1), ReportGenerator.COLORS['text_dark']),
                ('GRID', (0, 0), (-1, -1), 0.5, ReportGenerator.COLORS['border']),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, ReportGenerator.COLORS['bg_light']]),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
            ]
            
            history_table.setStyle(TableStyle(table_style))
            elements.append(history_table)
        
        # Footer
        elements.append(Spacer(1, 30))
        elements.append(HRFlowable(width="100%", thickness=1, color=ReportGenerator.COLORS['border'], spaceBefore=10, spaceAfter=10))
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=ReportGenerator.COLORS['text_light'],
            alignment=TA_CENTER
        )
        elements.append(Paragraph(
            f"Documento generado automáticamente por {config.APP_NAME} v{config.APP_VERSION}",
            footer_style
        ))
            
        # Build PDF with header/footer callback only on first page
        doc.build(elements, onFirstPage=ReportGenerator.add_watermark)
