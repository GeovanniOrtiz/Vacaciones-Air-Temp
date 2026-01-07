# Sistema de Control de Vacaciones - Air Temp de México

Sistema profesional e integral para la gestión de vacaciones de empleados, diseñado específicamente para cumplir con la **Ley Federal del Trabajo de México 2025**.

## 🚀 Características Principales

- **Multi-plataforma**: Incluye una aplicación de escritorio (PySide6) para administración interna y una aplicación web (Next.js) para visualización en tiempo real.
- **Base de Datos Unificada**: Sincronización instantánea entre escritorio y web mediante PostgreSQL.
- **Cálculos Automáticos**: Gestión de días de vacaciones y prima vacacional según la antigüedad del empleado.
- **Sincronización en Tiempo Real**: La aplicación web se actualiza automáticamente (polling) cuando se realizan cambios en la aplicación de escritorio.
- **Generación de Reportes**: Creación de reportes detallados en formato PDF.

## 🛠️ Tecnologías Utilizadas

### Escritorio (Desktop App)
- **Lenguaje**: Python 3.x
- **Interfaz**: PySide6 (Qt for Python)
- **Base de Datos**: PostgreSQL (psycopg2)
- **Reportes**: ReportLab

### Web (Frontend)
- **Framework**: Next.js 14+ (App Router)
- **Lenguaje**: TypeScript
- **Estilos**: Tailwind CSS
- **Sincronización**: Polling optimizado (5s)

### Backend (API)
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Base de Datos**: PostgreSQL

## 📋 Requisitos Previos

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

## 🔧 Instalación y Configuración

### 1. Base de Datos
Asegúrese de tener PostgreSQL corriendo y cree la base de datos:
```sql
CREATE DATABASE vacaciones_db;
```

### 2. Aplicación de Escritorio / Backend
```bash
# Instalar dependencias
pip install -r requirements.txt
pip install -r backend/requirements.txt

# Configurar variables de entorno (.env)
# DATABASE_URL=postgresql://usuario:password@localhost:5432/vacaciones_db
```

### 3. Aplicación Web
```bash
cd web
npm install
npm run dev
```

## 📄 Licencia

Este proyecto es propiedad de **Air Temp de México**. Todos los derechos reservados.
