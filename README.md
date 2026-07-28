# Sistema de Gestión Escolar (SGE)

Sistema web para la gestión académica de colegios rurales colombianos. Permite registrar estudiantes, notas, asistencia y cuenta con un asistente de inteligencia artificial para identificar estudiantes en riesgo académico.

## 🚀 Tecnologías

- **Backend:** Python, FastAPI, SQLAlchemy
- **Base de datos:** MySQL
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Autenticación:** JWT
- **IA:** Ollama (tinyllama)

## 📋 Requisitos previos

- Python 3.10 o superior
- MySQL 8.0 o superior
- Ollama instalado ([ollama.com](https://ollama.com))

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/jaimevedra/proyecto-gesti-n-escolar.git
cd proyecto-gesti-n-escolar
```

### 2. Configurar la base de datos

Entra a MySQL y ejecuta:

```sql
CREATE DATABASE sge_escolar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Luego ejecuta el archivo de diseño:

```bash
mysql -u tu_usuario -p sge_escolar < database/schema.sql
```

### 3. Configurar el backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Edita `database.py` con tus credenciales de MySQL:

```python
DB_USER = "tu_usuario"
DB_PASSWORD = "tu_password"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "sge_escolar"
```

### 4. Instalar el modelo de IA

```bash
ollama pull tinyllama
```

### 5. Iniciar el servidor

```bash
uvicorn main:app --reload
```

El servidor queda disponible en `http://127.0.0.1:8000`

## 🖥️ Uso

Abre cualquier archivo HTML de la carpeta `frontend/` en el navegador, comenzando por `login.html`.

### Roles del sistema

| Rol | Permisos |
|---|---|
| **Rector** | Acceso total: gestiona profesores, asignaturas, estudiantes y reportes |
| **Director de grupo** | Ve notas de su grado, registra notas de su asignatura, gestiona estudiantes de su grado |
| **Profesor** | Registra notas y asistencia de su asignatura |

### Páginas disponibles

| Página | Descripción |
|---|---|
| `login.html` | Inicio de sesión |
| `dashboard.html` | Panel principal |
| `estudiantes.html` | Gestión de estudiantes por grado |
| `notas.html` | Registro y consulta de notas |
| `asistencia.html` | Registro de asistencia |
| `ia.html` | Asistente IA para estudiantes en riesgo |
| `perfil.html` | Editar perfil personal |
| `registro-profesor.html` | Crear profesores (solo rector) |
| `gestion-profesores.html` | Gestionar roles y asignaciones (solo rector) |
| `asignaturas.html` | Gestionar asignaturas (solo rector) |

## 📡 API

La documentación completa de la API está disponible en: http://127.0.0.1:8000/docs

## 👨‍💻 Desarrollador

Desarrollado por **Jaime** — Estudiante de Análisis y Desarrollo de Software, SENA Colombia.