# Auth Service

A FastAPI-based authentication and authorization service with JWT support.  
Provides secure user registration, login, and role-protected routes.  
Designed for microservices or standalone deployment.

---

## 🚀 Features

- User registration with password validation
- Secure password hashing (bcrypt)
- JWT-based authentication (access tokens)
- Role-based access to protected routes
- Modular project structure (API, models, schemas, CRUD, DB)
- Separate environments for local, test, and Docker
- Fully tested with pytest

---

## 📂 Project Structure

```
auth_service/
├── app/
│   ├── api/
│   │   └── v1/           # API routes (auth endpoints)
│   │       ├── auth.py
│   │       ├── deps.py
│   │       └── __init__.py
│   ├── core/             # Config & security
│   │   ├── config.py
│   │   ├── security.py
│   │   └── __init__.py
│   ├── crud/             # Database operations
│   │   ├── user.py
│   │   └── __init__.py
│   ├── db/               # DB session & setup
│   │   ├── session.py
│   │   └── __init__.py
│   ├── models/           # SQLAlchemy models
│   │   ├── user.py
│   │   └── __init__.py
│   ├── schemas/          # Pydantic schemas
│   │   ├── token.py
│   │   ├── user.py
│   │   └── __init__.py
│   ├── main.py           # FastAPI entrypoint
│   └── __init__.py
├── db_init/              # DB init scripts
│   └── create_test_db.sql
├── tests/                # Test suite (pytest)
│   ├── test_auth_api.py
│   └── __init__.py
├── .env.example          # Docker environment (copy to .env)
├── local.env.example     # Local development env (copy to local.env)
├── test.env.example      # Test environment (copy to test.env)
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml        # Dependencies
├── uv.lock               # Dependency lock file
├── pytest.ini            # Pytest config
└── README.md
```

---

## ⚙️ Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (fast dependency manager)
- PostgreSQL (local or via Docker)

---

## 📦 Installation

Create your env files (they are git-ignored; set your own `SECRET_KEY` and DB password):

```bash
cp .env.example .env && cp local.env.example local.env && cp test.env.example test.env
```

Then install dependencies (drop `--no-dev` if you will run the tests):

```bash
uv sync --frozen --no-dev
```

---

## ▶️ Running the Service

### Local Development

```bash
ENV_FILE=local.env uv run uvicorn app.main:app --reload
```

App available at: [http://localhost:8000](http://localhost:8000)

### Docker

The API image does not work yet: see the known gaps in the [build log](../../README.md). The database container works:

```bash
docker compose up -d identity-db
```

---

## 🧪 Running Tests

Uses an isolated test database defined in `test.env` (`pytest.ini` loads it). Start the database first.

```bash
docker compose up -d identity-db
uv run pytest
```

---

## 🔑 API Endpoints

### Register User

`POST /register`

**Body (JSON):**
```json
{
  "email": "user@example.com",
  "password": "strongpassword",
  "password_repeat": "strongpassword"
}
```

---

### Login (Get Token)

`POST /token`

**Form data:**
- `username`: user’s email
- `password`: user’s password

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

---

### Get Current User

`GET /users/me`

**Headers:**
- `Authorization: Bearer <access_token>`

---

## 🔒 Role-Based Access

Protected routes validate:
- The JWT token
- User’s role (e.g., admin, user)

Unauthorized access → **403 Forbidden**

---

## 📚 Tech Stack

- FastAPI – Web framework
- Uvicorn – ASGI server
- SQLAlchemy – ORM
- PostgreSQL – Database
- Passlib – Password hashing
- Python-JOSE – JWT handling
- Pydantic Settings – Environment config
- Pytest – Testing

---

## 🛠️ Environment Files

- `.env` → Docker deployment
- `local.env` → Local development
- `test.env` → Testing

Each contains DB connection strings and JWT secrets.