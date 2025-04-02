# Organization Management System

## Overview
The **Organization Management System** is a FastAPI-based application designed to manage multiple organizations dynamically. Each organization gets its own separate database, and authentication is managed via JWT tokens. The system is built for scalability, security, and performance.

## Features

### Core Features
- **Multi-Tenant Architecture**: Each organization has its own dedicated database, dynamically created upon registration.
- **Organization Management**: Superusers can create organizations, triggering the creation of a new database.
- **User Management**: Organization admins can create and manage users within their respective organizations.
- **Authentication & Authorization**:
  - JWT-based authentication.
- **Dynamic Database Connections**:
  - Middleware to switch database connections based on the organization.
  - Ensures data isolation for each tenant.
- **Task Processing**:
  - Background tasks for handling heavy operations such as database creation.
- **API Documentation**:
  - Interactive API documentation using Swagger UI.
  - AI-generated API descriptions for better developer experience.

## Tech Stack
- **Backend Framework**: FastAPI (async support, OpenAPI integration)
- **Database**: PostgreSQL (multi-tenant setup)
- **ORM**: SQLAlchemy (async support for better performance)
- **Migrations**: Alembic (schema versioning and database migrations)
- **Authentication**: JWT-based authentication

## Setup & Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.9+
- PostgreSQL
- Docker (optional for containerization)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/organization-management.git
   cd organization-management
   ```

2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the environment variables:
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your database and JWT settings.

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Access API documentation at:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

### Admin Authentication
- `POST /admin/login` – Login and obtain JWT token.
- `POST /auth/register` – Register a new superuser/admin.

### Organization Management
- `POST /organization/create` – Create a new organization and initialize its database.
- `GET /organization` – List all organizations.

### User Management
- `POST /user/create` – Create a new user inside an organization's database.
- `GET /user/list` – Retrieve user details within an organization.

## Middleware & Background Processing
- **Auth Middleware**: Ensures JWT-based authentication and multi-tenancy support.
- **Background Task Processing**: Used for creating organizations asynchronously to prevent request blocking.