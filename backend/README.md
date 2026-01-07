# Backend API

FastAPI backend for the Vacation Management System.

## Setup

1. Install PostgreSQL (if not already installed)
2. Create database:
   ```bash
   createdb vacaciones_db
   ```

3. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. Migrate data from SQLite (optional):
   ```bash
   python migrate_data.py
   ```

## Running the API

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Employees
- `GET /api/employees/` - List all employees (with optional `?search=` parameter)
- `GET /api/employees/{id}` - Get employee by ID
- `GET /api/employees/{id}/vacation-summary` - Get employee vacation summary with calculations
- `POST /api/employees/` - Create new employee
- `PUT /api/employees/{id}` - Update employee
- `DELETE /api/employees/{id}` - Delete employee

### Vacation Records
- `GET /api/vacations/` - Get vacation records (with optional `?employee_id=` and `?year=` filters)
- `GET /api/vacations/{id}` - Get vacation record by ID
- `POST /api/vacations/` - Create new vacation record
- `PUT /api/vacations/{id}` - Update vacation record
- `DELETE /api/vacations/{id}` - Delete vacation record

## Features

- **Search**: Search employees by name or employee number
- **Validation**: Automatic validation for vacation date overlaps and cross-cycle records
- **Calculations**: Mexican Federal Labor Law compliant vacation calculations
- **CORS**: Enabled for web dashboard integration
