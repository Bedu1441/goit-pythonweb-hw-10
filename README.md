# goit-pythonweb-hw-12

REST API application built with FastAPI for managing contacts.

## Project overview

This project is the final homework for the Python Web course.  
It extends the previous REST API application with documentation, testing, Redis caching, password reset, role-based access control, refresh token support, and Docker Compose orchestration.

## Features

- JWT authentication
- Refresh token support
- User roles: `user` / `admin`
- Redis cache for current user
- Password reset flow
- Contacts CRUD
- Unit and integration tests
- Test coverage: **88%+**
- Sphinx documentation
- Docker Compose support
- Swagger / OpenAPI descriptions
- Basic application logging

## Implemented requirements

### Mandatory requirements

- Sphinx documentation
- Docstrings in core modules and functions
- Unit tests
- Integration tests
- Test coverage above 75%
- Redis cache for `get_current_user`
- Password reset mechanism
- Role-based access control
- Admin-only default avatar update
- Docker Compose for all services
- Sensitive settings moved to `.env`

### Additional improvements

- Refresh token support
- Improved Swagger UI descriptions
- Logging for authentication and cache flow
- Extra edge-case integration tests
- Deploy-ready project structure and settings

## Project structure

- `app/main.py` — application entry point
- `app/database.py` — database settings and session creation
- `app/models.py` — SQLAlchemy models
- `app/schemas.py` — Pydantic schemas
- `app/auth.py` — password hashing and JWT helpers
- `app/crud.py` — CRUD logic
- `app/dependencies.py` — authentication and role dependencies
- `app/redis_cache.py` — Redis cache helpers
- `app/routes_auth.py` — authentication routes
- `app/routes_contacts.py` — contacts routes
- `app/routes_users.py` — user routes
- `tests/` — unit and integration tests
- `docs/` — Sphinx documentation

## Security notes

- Passwords are stored as hashes
- JWT is used for authentication
- Refresh token is implemented for access token renewal
- Secrets are stored in `.env`
- Role checks protect admin-only endpoints
- Password reset is token-based
- Redis cache falls back safely if Redis is unavailable

## Main API endpoints

### Auth
- `POST /auth/signup`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/request_password_reset`
- `POST /auth/reset_password/{token}`

### Users
- `GET /users/me`
- `PATCH /users/default-avatar`

### Contacts
- `GET /contacts/`
- `POST /contacts/`
- `GET /contacts/search`
- `GET /contacts/birthdays`
- `GET /contacts/{id}`
- `PUT /contacts/{id}`
- `DELETE /contacts/{id}`

### System
- `GET /`

## Demo flow

1. Register a new user
2. Login and receive `access_token` + `refresh_token`
3. Create contacts
4. View the current user with `/users/me`
5. Request password reset
6. Reset password using a reset token
7. Refresh access token using `/auth/refresh`

## Test results

The project includes both unit and integration tests.

Final test result:

- **24 tests passed**
- **88.11% coverage**

Run tests with:

```bash
pytest
````

Coverage report:

```bash
pytest --cov=app --cov-report=term-missing
```

## Documentation

Sphinx HTML documentation is generated into:

```text
docs/build/html/index.html
```

Build documentation:

### Linux / macOS

```bash
cd docs
make html
```

### Windows PowerShell

```powershell
cd docs
py -m sphinx -b html source build\html
```

## Local run

### Run with Docker Compose

```bash
docker compose up --build
```

Because some standard local ports were already occupied on the development machine, the project may be exposed with remapped ports, for example:

* application: `http://127.0.0.1:8001/docs`
* PostgreSQL external port: `5433`
* Redis external port: `6379`

### Run directly with Uvicorn

```bash
python -m uvicorn app.main:app --reload
```

## Environment configuration

All sensitive settings are expected in `.env`.

Example variables are provided in `.env.example`.

Important variables include:

* `DATABASE_URL`
* `SECRET_KEY`
* `ALGORITHM`
* `ACCESS_TOKEN_EXPIRE_MINUTES`
* `RESET_TOKEN_EXPIRE_MINUTES`
* `REDIS_HOST`
* `REDIS_PORT`
* `APP_BASE_URL`
* `PORT`
* `DEBUG`

## About cloud deployment

Cloud deployment was **not completed in this submission**.

Reason:
the development was performed on a **work computer with ARM architecture**, and I decided not to finalize cloud deployment from this environment in order to avoid unstable build/runtime issues and environment-specific deployment problems during final submission preparation.

At the same time, the project was prepared for deployment:

* Dockerized application
* environment-based configuration
* refresh token support
* production-style settings structure
* deploy-ready README notes

So the application is **deployment-ready in structure**, but a public cloud link is intentionally not included in this submission.

## Conclusion

This project fully implements the mandatory requirements of the final homework and also includes several additional improvements:

* refresh token support
* improved Swagger documentation
* extra edge-case tests
* logging
* deploy-ready configuration

The result is a production-style FastAPI REST API with documentation, tests, caching, role-based access control, password reset flow, and containerized local execution.
