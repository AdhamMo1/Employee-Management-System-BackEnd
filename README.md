# Employee Management System

A Django REST API for managing employees, departments, and companies.

## Quick Start with Docker

### Prerequisites
- Docker Desktop installed and running

### One Command to Run
```bash
docker-compose up --build
```

### Default Admin Account
When the container starts, a default superuser is automatically created:

- **Username:** `admin`
- **Password:** `admin123`

Use these credentials to login at `http://localhost:8000/api/login/`

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/login/` | Obtain JWT token |
| `POST /api/token/refresh/` | Refresh JWT token |
| `GET /api/users/` | List users |
| `GET /api/companies/` | List companies |
| `GET /api/companies/dashboard/` | Dashboard stats (all companies or filter by `?company_id=1`) |
| `GET /api/departments/` | List departments |
| `GET /api/employees/` | List employees |

### Stopping the Application
```bash
docker-compose down
```

To remove the database volume as well:
```bash
docker-compose down -v
```
