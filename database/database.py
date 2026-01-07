"""
Database connection and initialization
"""
import os
os.environ["PGCLIENTENCODING"] = "UTF8"
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
import config
from urllib.parse import urlparse


class Database:
    """Database manager for PostgreSQL operations"""
    
    def __init__(self, db_url: Optional[str] = None):
        """Initialize database connection"""
        self.db_url = db_url or config.DATABASE_URL
        # Parse URL for individual parameters to avoid encoding issues with DSN strings
        parsed = urlparse(self.db_url)
        self.db_params = {
            'host': parsed.hostname or 'localhost',
            'port': parsed.port or 5432,
            'database': parsed.path.lstrip('/') or 'vacaciones_db',
            'user': parsed.username or 'postgres',
            'password': parsed.password or 'postgres'
        }
        self.connection: Optional[psycopg2.extensions.connection] = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create employees table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                employee_number VARCHAR(50) UNIQUE NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                entry_date DATE NOT NULL,
                department VARCHAR(100),
                position VARCHAR(100),
                email VARCHAR(255),
                phone VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create vacation_records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacation_records (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER NOT NULL,
                year INTEGER NOT NULL,
                days_taken REAL NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_employee_number 
            ON employees(employee_number)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_full_name 
            ON employees(full_name)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_vacation_employee 
            ON vacation_records(employee_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_vacation_year 
            ON vacation_records(employee_id, year)
        """)
        
        conn.commit()
    
    def get_connection(self) -> psycopg2.extensions.connection:
        """Get database connection"""
        if self.connection is None or self.connection.closed:
            try:
                self.connection = psycopg2.connect(
                    **self.db_params,
                    cursor_factory=RealDictCursor
                )
            except UnicodeDecodeError as e:
                # This often happens on Windows when a connection error message 
                # contains non-UTF8 characters (like Spanish accents).
                # We try to provide a more helpful message.
                raise ConnectionError(
                    "Error de decodificación al conectar a la base de datos. "
                    "Asegúrese de que el servidor PostgreSQL esté funcionando y "
                    "que las credenciales en config.py sean correctas."
                ) from e
        return self.connection
    
    def close(self):
        """Close database connection"""
        if self.connection and not self.connection.closed:
            self.connection.close()
            self.connection = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Global database instance
_db_instance: Optional[Database] = None


def get_database() -> Database:
    """Get global database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
