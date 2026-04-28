# Employee Management System (EMS)

A comprehensive Django REST API for managing employees, departments, and companies with JWT authentication and role-based access control.

![Django](https://img.shields.io/badge/Django-6.0-green)
![DRF](https://img.shields.io/badge/DRF-3.15-red)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

---

## Features

- **JWT Authentication** - Secure token-based authentication
- **Role-Based Access Control** - System Admin, HR Manager, Employee roles
- **Company Management** - Create, update, delete companies
- **Department Management** - Organize departments within companies
- **Employee Management** - Full employee lifecycle management
- **Dashboard Statistics** - Real-time metrics and analytics
- **Multi-Language Support** - English & Arabic
- **Docker Support** - One-command deployment

---

## Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git (for cloning)

### One Command to Run

```bash
# Clone the repository
git clone https://github.com/AdhamMo1/Employee-Management-System-BackEnd.git
cd "Employee Management System"

# Start the application
docker-compose up --build
```

The API will be available at `http://localhost:8000`

---

## Default Admin Account

When the container starts, a default superuser is automatically created:

| Field | Value |
|-------|-------|
| **Username** | `admin` |
| **Password** | `admin123` |
| **Email** | `admin@example.com` |
| **Role** | `SYSTEM_ADMINISTRATOR` |

Use these credentials to login and obtain a JWT token.

---

## API Documentation

### Postman Collection
[![Run in Postman](https://run.pstmn.io/button.svg)](https://www.postman.com/adham-api/workspace/employee-management-system-sme)

Or import directly: `https://www.postman.com/adham-api/workspace/employee-management-system-sme`

### Base URL
```
http://localhost:8000
```

### Response Format
All API responses follow this structure:
```json
{
  "details": "Success message or error details",
  "data": { ... }
}
```

### Authentication Header
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/v1/auth/login` | No | Login and get JWT tokens |

### Login
**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "username": "admin",
      "password": "admin123"
    }
  }'
```

**Response:**
```json
{
  "details": "Login successful",
  "data": {
    "session": {
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    },
    "user_info": {
      "id": 1,
      "email": "admin@example.com",
      "role": "SYSTEM_ADMINISTRATOR",
      "employee_id": null,
      "company_id": null
    }
  }
}
```

---

## Dashboard Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/companies/dashboard` | Yes | Get dashboard statistics |

### Get Dashboard Stats

**Query Parameters:**
- `company_id` (optional) - Filter stats by specific company ID

**Request (All Companies):**
```bash
curl -X GET http://localhost:8000/api/v1/companies/dashboard \
  -H "Authorization: Bearer <token>"
```

**Request (Specific Company):**
```bash
curl -X GET "http://localhost:8000/api/v1/companies/dashboard?company_id=1" \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "details": "Dashboard stats retrieved successfully",
  "data": {
    "total_companies": 5,
    "total_departments": 12,
    "total_employees": 45,
    "active_employees": 40,
    "inactive_employees": 5,
    "avg_days_employed": 365,
    "filtered_by_company": {
      "id": 1,
      "name": "TechCorp Inc."
    }
  }
}
```

---

## Company Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/companies` | Yes | List all companies |
| `POST` | `/api/v1/companies` | Yes | Create new company |
| `GET` | `/api/v1/companies/<id>` | Yes | Get company details |
| `PUT` | `/api/v1/companies/<id>` | Yes | Update company |
| `PATCH` | `/api/v1/companies/<id>` | Yes | Update company status |
| `DELETE` | `/api/v1/companies/<id>` | Yes | Delete company |

### List Companies
```bash
curl -X GET http://localhost:8000/api/v1/companies \
  -H "Authorization: Bearer <token>"
```

### Create Company
```bash
curl -X POST http://localhost:8000/api/v1/companies \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "name": "TechCorp Inc."
    }
  }'
```

### Update Company
```bash
curl -X PUT http://localhost:8000/api/v1/companies/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "name": "TechCorp Solutions"
    }
  }'
```

### Update Company Status
```bash
curl -X PATCH http://localhost:8000/api/v1/companies/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "is_active": false
    }
  }'
```

### Delete Company
```bash
curl -X DELETE http://localhost:8000/api/v1/companies/1 \
  -H "Authorization: Bearer <token>"
```

---

## Department Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/departments` | Yes | List all departments |
| `POST` | `/api/v1/departments` | Yes | Create new department |
| `GET` | `/api/v1/departments/<id>` | Yes | Get department details |
| `PUT` | `/api/v1/departments/<id>` | Yes | Update department |
| `PATCH` | `/api/v1/departments/<id>` | Yes | Update department status |
| `DELETE` | `/api/v1/departments/<id>` | Yes | Delete department |

### List Departments
```bash
curl -X GET http://localhost:8000/api/v1/departments \
  -H "Authorization: Bearer <token>"
```

### Create Department
```bash
curl -X POST http://localhost:8000/api/v1/departments \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "name": "Engineering",
      "company_id": 1
    }
  }'
```

### Update Department
```bash
curl -X PUT http://localhost:8000/api/v1/departments/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "name": "Software Engineering",
      "company_id": 1
    }
  }'
```

### Update Department Status
```bash
curl -X PATCH http://localhost:8000/api/v1/departments/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "is_active": false
    }
  }'
```

### Delete Department
```bash
curl -X DELETE http://localhost:8000/api/v1/departments/1 \
  -H "Authorization: Bearer <token>"
```

---

## Employee Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/employees` | Yes | List all employees |
| `POST` | `/api/v1/employees` | Yes | Create new employee |
| `GET` | `/api/v1/employees/<id>` | Yes | Get employee details |
| `PUT` | `/api/v1/employees/<id>` | Yes | Update employee |
| `PATCH` | `/api/v1/employees/<id>` | Yes | Update employee status |
| `DELETE` | `/api/v1/employees/<id>` | Yes | Delete employee |

### List Employees
```bash
curl -X GET http://localhost:8000/api/v1/employees \
  -H "Authorization: Bearer <token>"
```

### Create Employee
```bash
curl -X POST http://localhost:8000/api/v1/employees \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "name": "John Doe",
      "title": "Senior Developer",
      "department_id": 1,
      "company_id": 1,
      "email": "john@example.com",
      "password": "password123",
      "mobile": "+1234567890",
      "address": "123 Main St",
      "hire_date": "2024-01-15"
    }
  }'
```

### Update Employee
```bash
curl -X PUT http://localhost:8000/api/v1/employees/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "name": "John Smith",
      "title": "Lead Developer",
      "department_id": 1
    }
  }'
```

### Update Employee Status
```bash
curl -X PATCH http://localhost:8000/api/v1/employees/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "is_active": false
    }
  }'
```

### Delete Employee
```bash
curl -X DELETE http://localhost:8000/api/v1/employees/1 \
  -H "Authorization: Bearer <token>"
```

---

## User Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/users` | Yes | List all users |
| `POST` | `/api/v1/users` | Yes | Create new user |
| `GET` | `/api/v1/users/<id>` | Yes | Get user details |
| `PUT` | `/api/v1/users/<id>` | Yes | Update user |
| `PATCH` | `/api/v1/users/<id>` | Yes | Update user status |
| `DELETE` | `/api/v1/users/<id>` | Yes | Delete user |

### List Users
```bash
curl -X GET http://localhost:8000/api/v1/users \
  -H "Authorization: Bearer <token>"
```

### Create User
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "username": "johndoe",
      "email": "john@example.com",
      "password": "securepass123",
      "first_name": "John",
      "last_name": "Doe",
      "role": "EMPLOYEE",
      "company_id": 1
    }
  }'
```

### Update User Status
```bash
curl -X PATCH http://localhost:8000/api/v1/users/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "request_data": {
      "is_active": false
    }
  }'
```

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐       ┌──────────────────┐       ┌─────────────────┐
│     users       │       │   employees      │       │  departments    │
│  (UserAccounts) │◄──────┤    (Employee)    │◄──────┤  (Department)   │
├─────────────────┤   1:1 ├──────────────────┤   N:1 ├─────────────────┤
│ id (PK)         │       │ id (PK)          │       │ id (PK)         │
│ username        │       │ user_id (FK)     │       │ company_id (FK) │
│ email           │       │ department_id(FK)│       │ name            │
│ password        │       │ name             │       │ created_at      │
│ first_name      │       │ title            │       │ updated_at      │
│ last_name       │       │ hire_date        │       └────────┬────────┘
│ role            │       │ mobile           │                │
│ company_id (FK) │       │ address          │                │ N:1
│ is_active       │       │ created_at       │                │
│ created_at      │       │ updated_at       │                ▼
│ updated_at      │       └──────────────────┘       ┌─────────────────┐
└────────┬────────┘                                   │    companies    │
         │                                            │    (Company)    │
         │ N:1                                        ├─────────────────┤
         └───────────────────────────────────────────►│ id (PK)         │
                                                       │ name            │
                                                       │ is_active       │
                                                       │ created_at      │
                                                       │ updated_at      │
                                                       └─────────────────┘
```

### Tables

#### 1. `companies`
| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGINT (PK) | Auto-increment primary key |
| `name` | VARCHAR(255) | Company name |
| `is_active` | BOOLEAN | Active status (default: true) |
| `created_at` | TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | Last update timestamp |

#### 2. `departments`
| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGINT (PK) | Auto-increment primary key |
| `company_id` | BIGINT (FK) | Reference to companies.id (nullable) |
| `name` | VARCHAR(255) | Department name |
| `created_at` | TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | Last update timestamp |

#### 3. `users` (UserAccounts)
| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGINT (PK) | Auto-increment primary key |
| `username` | VARCHAR(150) | Unique username |
| `email` | VARCHAR(254) | Unique email |
| `password` | VARCHAR(128) | Hashed password |
| `first_name` | VARCHAR(150) | First name |
| `last_name` | VARCHAR(150) | Last name |
| `role` | VARCHAR(50) | Role: NOT_SELECTED, SYSTEM_ADMINISTRATOR, HR_MANAGER, EMPLOYEE |
| `company_id` | BIGINT (FK) | Reference to companies.id (nullable) |
| `is_active` | BOOLEAN | Active status |
| `is_staff` | BOOLEAN | Staff status |
| `is_superuser` | BOOLEAN | Superuser status |
| `last_login` | TIMESTAMP | Last login time |
| `date_joined` | TIMESTAMP | Account creation time |
| `created_at` | TIMESTAMP | Record creation timestamp |
| `updated_at` | TIMESTAMP | Last update timestamp |

#### 4. `employees`
| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGINT (PK) | Auto-increment primary key |
| `user_id` | BIGINT (FK) | Reference to users.id (nullable) |
| `department_id` | BIGINT (FK) | Reference to departments.id (nullable) |
| `name` | VARCHAR(255) | Employee full name |
| `title` | VARCHAR(255) | Job title (nullable) |
| `hire_date` | DATE | Employment start date (default: today) |
| `mobile` | BIGINT | Phone number (nullable) |
| `address` | VARCHAR(255) | Address (nullable) |
| `created_at` | TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | Last update timestamp |

---

## Authentication & Roles

### JWT Token Structure

**Access Token:** Valid for 60 minutes
**Refresh Token:** Valid for 15 days

### Role Hierarchy

| Role | Permissions |
|------|-------------|
| `SYSTEM_ADMINISTRATOR` | Full access to all endpoints |
| `HR_MANAGER` | Read access to all, Write access to departments/employees |
| `EMPLOYEE` | Limited read access (own data only) |
| `NOT_SELECTED` | No access until role assigned |

### Permission Decorators

- `@admin_required()` - Only System Administrators
- `@hr_or_admin_required()` - HR Managers and System Administrators
- `@authenticated_required()` - Any authenticated user

---

## Multi-Language Support

API supports English (`en`) and Arabic (`ar`). Set language via header:

```bash
curl -H "LN: ar" http://localhost:8000/api/v1/companies
```

Default language is English if not specified.

---

## Development

### Run Without Docker

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup PostgreSQL database (update settings.py with your credentials)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py initadmin

# Start server
python manage.py runserver
```

### Useful Commands

```bash
# Create superuser manually
python manage.py createsuperuser

# Run tests
python manage.py test

# Shell access
docker-compose exec web python manage.py shell

# Database shell
docker-compose exec web python manage.py dbshell

# Check system
docker-compose exec web python manage.py check
```

---

## Project Structure

```
Employee Management System/
├── backend_apps/
│   ├── authentication/    # Login & JWT
│   ├── companies/         # Company management + Dashboard
│   ├── departments/       # Department management
│   ├── employees/         # Employee management
│   └── users/             # User management
├── main_project/          # Django settings & URLs
├── docker-compose.yml     # Docker configuration
├── Dockerfile             # Web container
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

