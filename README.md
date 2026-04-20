# GoIT Python Web HW-10

REST API for managing contacts with authentication, authorization, email verification, rate limiting, CORS support, and avatar upload functionality.

---

## Features

- User registration and authentication
- JWT-based authorization (access tokens)
- Password hashing (bcrypt)
- Email verification with token confirmation
- Protected endpoints (only authenticated users)
- Each user has access only to their own contacts
- CRUD operations for contacts
- Search contacts by first name, last name, or email
- Upcoming birthdays (next 7 days)
- Rate limiting for `/users/me` endpoint
- CORS support
- Avatar upload (Cloudinary integration)

---

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker & Docker Compose
- Pydantic
- JWT (python-jose)
- Passlib (bcrypt)
- SlowAPI (rate limiting)
- Cloudinary (image hosting)

---

## Project Structure

```

app/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── crud.py
├── dependencies.py
├── email_utils.py
├── cloudinary_service.py
├── routes_auth.py
├── routes_contacts.py
└── routes_users.py

```

---

## Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
POSTGRES_DB=contacts_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY=supersecretkey123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

EMAIL_TOKEN_SECRET=email-secret-key
APP_BASE_URL=http://localhost:8001

SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM=

CORS_ORIGINS=http://localhost:3000,http://localhost:8001

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

---

## Run Project

Build and start services:

```bash
docker compose up --build
```

Open API documentation:

```
http://localhost:8001/docs
```

---

## Authentication Flow

1. Register user → `POST /auth/signup`
2. Confirm email via token link
3. Login → `POST /auth/login`
4. Use token in Swagger:

```
Bearer <access_token>
```

---

## API Endpoints

### Auth

- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/confirmed_email/{token}`
- `POST /auth/request_email`

### Users

- `GET /users/me`
- `PATCH /users/avatar`

### Contacts

- `POST /contacts/`
- `GET /contacts/`
- `GET /contacts/{contact_id}`
- `PUT /contacts/{contact_id}`
- `DELETE /contacts/{contact_id}`
- `GET /contacts/search`
- `GET /contacts/birthdays`

---

## Email Verification

The application implements email verification using token-based confirmation.

- After registration, a verification token is generated
- A confirmation link is created and sent via email
- If SMTP is not configured, the verification link is printed in application logs
- User login is restricted until email is confirmed

---

## Avatar Upload (Cloudinary)

The application supports updating user avatars using Cloudinary.

- Endpoint: `PATCH /users/avatar`
- Image is uploaded to Cloudinary
- Returned URL is stored in the database

**Note:**
Cloudinary integration requires the following environment variables:

```
CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET
```

If these variables are not configured, the avatar upload feature may not function correctly.

---

## Security

- Passwords are hashed using bcrypt
- JWT tokens are used for authentication
- Unauthorized access returns HTTP 401
- Duplicate email registration returns HTTP 409
- Only verified users can log in
- Users can only manage their own contacts

---

## Rate Limiting

The `/users/me` endpoint is protected with rate limiting to prevent abuse.

---

## CORS

CORS is enabled and configurable via environment variables.

---

## ARM Architecture Note

This project was developed on a Windows ARM (ARM64) machine.

Some Python dependencies (e.g., httptools) may not install correctly on ARM environments.

To avoid compatibility issues, the application is designed to run inside Docker containers, where dependencies are installed in a Linux environment.

---

## Conclusion

This project demonstrates:

- REST API development with FastAPI
- Secure authentication and authorization
- Database integration with PostgreSQL
- Containerized deployment using Docker
- Handling of real-world backend concerns (security, rate limiting, verification, environment configuration)

## Verification and Access Control

Only confirmed users can access protected user and contact endpoints.

## Rate Limiting

The `/users/me` endpoint is rate-limited.

## Avatar Upload

Avatar upload validates file type and requires Cloudinary environment variables.
