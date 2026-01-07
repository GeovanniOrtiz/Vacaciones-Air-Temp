"""
Configuration settings for the Vacation Management System
"""
import os
from pathlib import Path

# Application Information
APP_NAME = "Sistema de Control de Vacaciones Test"
APP_VERSION = "1.0.0"
COMPANY_NAME = "Air Temp de Mexico"

# Paths
BASE_DIR = Path(__file__).parent
DATABASE_DIR = BASE_DIR / "data"
DATABASE_PATH = DATABASE_DIR / "vacaciones.db"

# Ensure data directory exists
DATABASE_DIR.mkdir(exist_ok=True)

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Airtemp@127.0.0.1:5432/vacaciones_db")

# UI Constants
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 700
WINDOW_DEFAULT_WIDTH = 1600
WINDOW_DEFAULT_HEIGHT = 800

# Colors - Modern Professional Theme
COLORS = {
    # Primary colors
    "primary": "#2563eb",  # Blue
    "primary_dark": "#1e40af",
    "primary_light": "#3b82f6",
    
    # Accent colors
    "accent": "#06b6d4",  # Cyan
    "accent_dark": "#0891b2",
    "accent_light": "#22d3ee",
    
    # Background colors
    "bg_dark": "#0f172a",  # Dark slate
    "bg_medium": "#1e293b",
    "bg_light": "#334155",
    "bg_card": "#1e293b",
    
    # Text colors
    "text_primary": "#f1f5f9",
    "text_secondary": "#cbd5e1",
    "text_muted": "#94a3b8",
    
    # Status colors
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "info": "#3b82f6",
    
    # Border and divider
    "border": "#475569",
    "divider": "#334155",
}

# Fonts
FONT_FAMILY = "Segoe UI, SF Pro Display, Inter, -apple-system, BlinkMacSystemFont, sans-serif"
FONT_SIZE_SMALL = 11
FONT_SIZE_NORMAL = 13
FONT_SIZE_LARGE = 15
FONT_SIZE_XLARGE = 18
FONT_SIZE_TITLE = 24

# Animation durations (ms)
ANIMATION_FAST = 150
ANIMATION_NORMAL = 250
ANIMATION_SLOW = 400
