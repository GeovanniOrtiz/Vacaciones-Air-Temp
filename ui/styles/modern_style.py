"""
Modern professional styling for the application
"""
import config


def get_stylesheet() -> str:
    """Get the complete application stylesheet"""
    
    c = config.COLORS
    
    return f"""
    /* ===== GLOBAL STYLES ===== */
    QWidget {{
        background-color: {c['bg_dark']};
        color: {c['text_primary']};
        font-family: {config.FONT_FAMILY};
        font-size: {config.FONT_SIZE_NORMAL}px;
    }}
    
    /* ===== MAIN WINDOW ===== */
    QMainWindow {{
        background-color: {c['bg_dark']};
    }}
    
    /* ===== MENU BAR ===== */
    QMenuBar {{
        background-color: {c['bg_dark']};
        color: {c['text_primary']};
        border-bottom: 1px solid {c['border']};
        padding: 4px;
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: 6px 12px;
        border-radius: 4px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {c['bg_light']};
    }}
    
    QMenu {{
        background-color: {c['bg_medium']};
        color: {c['text_primary']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        padding: 4px;
    }}
    
    QMenu::item {{
        padding: 8px 24px;
        border-radius: 4px;
    }}
    
    QMenu::item:selected {{
        background-color: {c['primary']};
    }}
    
    /* ===== TOOLBAR ===== */
    QToolBar {{
        background-color: {c['bg_dark']};
        border-bottom: 1px solid {c['border']};
        spacing: 8px;
        padding: 8px;
    }}
    
    QToolButton {{
        background-color: transparent;
        color: {c['text_primary']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        padding: 6px 12px;
        font-weight: 500;
    }}
    
    QToolButton:hover {{
        background-color: {c['bg_light']};
        border-color: {c['text_secondary']};
    }}
    
    /* ===== STATUS BAR ===== */
    QStatusBar {{
        background-color: {c['bg_dark']};
        color: {c['text_muted']};
        border-top: 1px solid {c['border']};
    }}
    
    /* ===== BUTTONS ===== */
    QPushButton {{
        background-color: {c['bg_light']};
        color: {c['text_primary']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
        font-size: {config.FONT_SIZE_NORMAL}px;
    }}
    
    QPushButton:hover {{
        background-color: {c['bg_medium']};
        border-color: {c['text_secondary']};
    }}
    
    QPushButton:pressed {{
        background-color: {c['bg_dark']};
    }}
    
    QPushButton:disabled {{
        background-color: {c['bg_dark']};
        color: {c['text_muted']};
        border-color: {c['border']};
    }}
    
    QPushButton#primaryButton, QPushButton#addButton {{
        background-color: {c['primary']};
        color: white;
        border: none;
    }}
    
    QPushButton#primaryButton:hover, QPushButton#addButton:hover {{
        background-color: {c['primary_light']};
    }}
    
    QPushButton#deleteButton {{
        background-color: transparent;
        color: {c['error']};
        border: 1px solid {c['border']};
    }}
    
    QPushButton#deleteButton:hover {{
        background-color: {c['error']};
        color: white;
        border-color: {c['error']};
    }}
    
    QPushButton#editButton {{
        background-color: transparent;
        color: {c['accent']};
        border: 1px solid {c['border']};
    }}
    
    QPushButton#editButton:hover {{
        background-color: {c['accent']};
        color: white;
        border-color: {c['accent']};
    }}
    
    /* ===== LABELS ===== */
    QLabel {{
        color: {c['text_primary']};
        background-color: transparent;
    }}
    
    QLabel#titleLabel {{
        font-size: {config.FONT_SIZE_TITLE}px;
        font-weight: 300; /* Lighter weight for minimalist look */
        color: {c['text_primary']};
        padding-bottom: 12px;
        margin-bottom: 10px;
    }}
    
    QLabel#sectionHeader {{
        font-size: {config.FONT_SIZE_LARGE}px;
        font-weight: 600;
        color: {c['text_primary']};
        padding-bottom: 8px;
        border-bottom: 1px solid {c['border']};
    }}
    
    QLabel#metricValue {{
        font-family: 'Segoe UI', sans-serif;
        font-weight: 300;
    }}
    
    /* ===== INPUT FIELDS ===== */
    QLineEdit, QSpinBox, QDateEdit, QDoubleSpinBox, QTextEdit {{
        background-color: {c['bg_dark']};
        color: {c['text_primary']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        padding: 8px 10px;
        font-size: {config.FONT_SIZE_NORMAL}px;
        selection-background-color: {c['primary_light']};
    }}
    
    QLineEdit:focus, QSpinBox:focus, QDateEdit:focus, QDoubleSpinBox:focus, QTextEdit:focus {{
        border: 1px solid {c['primary']};
        background-color: {c['bg_medium']};
    }}
    
    /* ===== TABLE WIDGET ===== */
    QTableWidget {{
        background-color: {c['bg_dark']};
        alternate-background-color: {c['bg_medium']};
        color: {c['text_primary']};
        gridline-color: transparent; /* No grid lines */
        border: none;
        selection-background-color: {c['bg_light']};
        selection-color: {c['text_primary']};
    }}
    
    QTableWidget::item {{
        padding: 10px;
        border-bottom: 1px solid {c['border']};
    }}
    
    QTableWidget::item:selected {{
        background-color: {c['bg_light']};
    }}
    
    QHeaderView::section {{
        background-color: {c['bg_dark']};
        color: {c['text_secondary']};
        padding: 10px;
        border: none;
        border-bottom: 1px solid {c['border']};
        font-weight: 600;
        text-transform: uppercase;
        font-size: {config.FONT_SIZE_SMALL}px;
        letter-spacing: 1px;
    }}
    
    /* ===== TABS ===== */
    QTabWidget::pane {{
        border: none;
        background-color: {c['bg_dark']};
    }}
    
    QTabBar::tab {{
        background-color: transparent;
        color: {c['text_secondary']};
        padding: 10px 20px;
        border-bottom: 2px solid transparent;
        font-weight: 500;
    }}
    
    QTabBar::tab:selected {{
        color: {c['primary']};
        border-bottom: 2px solid {c['primary']};
    }}
    
    QTabBar::tab:hover {{
        color: {c['text_primary']};
    }}
    
    /* ===== SCROLL BAR ===== */
    QScrollBar:vertical {{
        background-color: {c['bg_dark']};
        width: 10px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {c['border']};
        border-radius: 5px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {c['text_secondary']};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    /* ===== PROGRESS BAR ===== */
    QProgressBar {{
        background-color: {c['bg_light']};
        border: none;
        border-radius: 2px;
        text-align: center;
        color: {c['text_primary']};
    }}
    
    QProgressBar::chunk {{
        background-color: {c['primary']};
        border-radius: 2px;
    }}
    
    /* ===== DIALOG ===== */
    QDialog {{
        background-color: {c['bg_dark']};
    }}
    
    /* ===== CARDS (Minimalist) ===== */
    QFrame#cardFrame {{
        background-color: transparent;
        border: none;
    }}
    
    QFrame#metricCard {{
        background-color: transparent;
        border: 1px solid {c['border']};
        border-radius: 8px;
    }}
    """


def get_card_style() -> str:
    """Get style for card widgets"""
    # Minimalist: no background, just spacing
    return "background-color: transparent; border: none;"


def get_gradient_style(color1: str, color2: str) -> str:
    """Get gradient background style"""
    # Minimalist: return solid color instead of gradient
    return f"background-color: {color1}; border-radius: 6px;"
