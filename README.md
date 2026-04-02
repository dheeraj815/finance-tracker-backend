<<<<<<< HEAD
# 💸 Finance Tracker API

A **production-style REST API** for managing personal financial transactions — built with FastAPI, SQLAlchemy, and SQLite. Designed to demonstrate clean architecture, separation of concerns, and scalable backend engineering principles.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Running the Server](#running-the-server)
- [API Reference](#api-reference)
- [Example Requests & Responses](#example-requests--responses)
- [Design Decisions](#design-decisions)

---

## Overview

Finance Tracker provides a clean API surface for:

- **Transaction Management** — create, read, update, and delete income/expense records with filtering and pagination
- **Financial Analytics** — aggregate summaries, category-wise breakdowns, and month-over-month trends
- **User Management** — simple user accounts with one-to-many transaction ownership

Built without external dependencies beyond the Python ecosystem — no auth service, no cloud storage, no message broker. Just a well-structured, immediately runnable backend.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   HTTP Clients                  │
└────────────────────────┬────────────────────────┘
                         │
┌────────────────────────▼────────────────────────┐
│              FastAPI Application                │
│  ┌──────────────────────────────────────────┐  │
│  │              Routes (Controllers)        │  │
│  │   users.py  transactions.py  analytics.py│  │
│  └──────────────┬───────────────────────────┘  │
│                 │                               │
│  ┌──────────────▼────────────┐                 │
│  │   Service Layer           │                 │
│  │   analytics_service.py    │                 │
│  └──────────────┬────────────┘                 │
│                 │                               │
│  ┌──────────────▼────────────┐                 │
│  │   Data Access Layer       │                 │
│  │        crud.py            │                 │
│  └──────────────┬────────────┘                 │
│                 │                               │
│  ┌──────────────▼────────────┐                 │
│  │   ORM Models + Schemas    │                 │
│  │   models.py  schemas.py   │                 │
│  └──────────────┬────────────┘                 │
└─────────────────┼───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              SQLite Database                    │
└─────────────────────────────────────────────────┘
```

**Layered responsibilities:**

| Layer | File(s) | Responsibility |
|---|---|---|
| Routes | `routes/*.py` | HTTP surface — thin controllers only |
| Service | `services/analytics_service.py` | Business logic and complex aggregations |
| Data Access | `crud.py` | All DB queries, reusable across routes |
| Models | `models.py` | Database schema via SQLAlchemy ORM |
| Schemas | `schemas.py` | Request validation + response serialization |
| Config | `core/config.py` | Centralised settings, env-aware |

---

## Tech Stack

| Technology | Version | Role |
|---|---|---|
| **FastAPI** | 0.115 | Async-ready web framework with OpenAPI out of the box |
| **SQLAlchemy** | 2.0 | ORM with type-safe query expressions |
| **Pydantic v2** | 2.9 | Request/response validation and serialization |
| **SQLite** | — | Zero-config embedded database (swap for Postgres in prod) |
| **Uvicorn** | 0.30 | High-performance ASGI server |

---

## Project Structure

```
finance_tracker/
├── app/
│   ├── main.py               # App factory, middleware, router registration
│   ├── database.py           # Engine, session factory, get_db() dependency
│   ├── models.py             # SQLAlchemy ORM models (User, Transaction)
│   ├── schemas.py            # Pydantic schemas (Create / Update / Response)
│   ├── crud.py               # Data access layer — all DB interaction
│   ├── core/
│   │   └── config.py         # Centralised settings via pydantic-settings
│   ├── routes/
│   │   ├── users.py          # POST /users, GET /users
│   │   ├── transactions.py   # Full CRUD for /transactions
│   │   └── analytics.py      # GET /analytics/summary|category|monthly
│   └── services/
│       └── analytics_service.py  # Aggregation business logic
├── requirements.txt
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- `pip`

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/dheeraj815/finance-tracker.git
cd finance_tracker

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

No additional database setup is needed — SQLite creates the file automatically on first run.

---

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API is now live at **http://localhost:8000**

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | Swagger UI — interactive API explorer |
| `http://localhost:8000/redoc` | ReDoc documentation |
| `http://localhost:8000/health` | Health check endpoint |

---

## API Reference

### Users

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/users/` | Create a new user |
| `GET` | `/users/` | List all users (paginated) |
| `GET` | `/users/{id}` | Get a single user |

### Transactions

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/transactions/` | Create a new transaction |
| `GET` | `/transactions/` | List transactions with filters + pagination |
| `GET` | `/transactions/{id}` | Get a single transaction |
| `PUT` | `/transactions/{id}` | Partially update a transaction |
| `DELETE` | `/transactions/{id}` | Delete a transaction |

**Query Parameters for `GET /transactions/`:**

| Parameter | Type | Description |
|---|---|---|
| `user_id` | int | Filter by user |
| `type` | `income` \| `expense` | Filter by transaction type |
| `category` | string | Filter by category (case-insensitive) |
| `date_from` | `YYYY-MM-DD` | Start of date range |
| `date_to` | `YYYY-MM-DD` | End of date range |
| `limit` | int (1–100) | Results per page (default: 20) |
| `offset` | int | Pagination offset (default: 0) |

### Analytics

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/analytics/summary` | Total income, expenses, net balance, count |
| `GET` | `/analytics/category` | Per-category aggregation sorted by total |
| `GET` | `/analytics/monthly` | Month-by-month income vs. expense breakdown |

All analytics endpoints accept an optional `?user_id=` query parameter to scope results.

---

## Example Requests & Responses

### Create a User

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "email": "alice@example.com"}'
```

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com"
}
```

---

### Create a Transaction

```bash
curl -X POST http://localhost:8000/transactions/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000.00,
    "type": "income",
    "category": "Salary",
    "description": "Monthly salary deposit",
    "user_id": 1
  }'
```

```json
{
  "id": 1,
  "amount": 5000.0,
  "type": "income",
  "category": "Salary",
  "date": "2026-04-02",
  "description": "Monthly salary deposit",
  "user_id": 1
}
```

---

### List Transactions (Filtered)

```bash
curl "http://localhost:8000/transactions/?user_id=1&type=expense&limit=5"
```

```json
[
  {
    "id": 3,
    "amount": 1200.0,
    "type": "expense",
    "category": "Rent",
    "date": "2026-04-02",
    "description": "March rent",
    "user_id": 1
  },
  {
    "id": 2,
    "amount": 120.5,
    "type": "expense",
    "category": "Groceries",
    "date": "2026-04-02",
    "description": "Weekly shop",
    "user_id": 1
  }
]
```

---

### Partial Update

```bash
curl -X PUT http://localhost:8000/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{"amount": 5500.00, "description": "Salary after raise"}'
```

```json
{
  "id": 1,
  "amount": 5500.0,
  "type": "income",
  "category": "Salary",
  "date": "2026-04-02",
  "description": "Salary after raise",
  "user_id": 1
}
```

---

### Analytics Summary

```bash
curl "http://localhost:8000/analytics/summary?user_id=1"
```

```json
{
  "total_income": 8000.0,
  "total_expenses": 1465.5,
  "net_balance": 6534.5,
  "transaction_count": 6
}
```

---

### Category Breakdown

```bash
curl "http://localhost:8000/analytics/category?user_id=1"
```

```json
{
  "breakdown": [
    { "category": "Salary",    "type": "income",  "total": 5500.0, "count": 1 },
    { "category": "Freelance", "type": "income",  "total": 2500.0, "count": 1 },
    { "category": "Rent",      "type": "expense", "total": 1200.0, "count": 1 },
    { "category": "Groceries", "type": "expense", "total":  205.5, "count": 2 },
    { "category": "Utilities", "type": "expense", "total":   60.0, "count": 1 }
  ]
}
```

---

### Monthly Summary

```bash
curl "http://localhost:8000/analytics/monthly?user_id=1"
```

```json
{
  "monthly_summary": [
    {
      "year": 2026,
      "month": 4,
      "total_income": 8000.0,
      "total_expenses": 1465.5,
      "net_balance": 6534.5
    }
  ]
}
```

---

## Error Responses

The API returns consistent, descriptive error responses:

| Status | Scenario |
|---|---|
| `201 Created` | Resource successfully created |
| `204 No Content` | Successful deletion |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Duplicate resource (e.g., email already registered) |
| `422 Unprocessable Entity` | Validation failure (e.g., negative amount, invalid type) |
| `500 Internal Server Error` | Unexpected server-side error |

```json
{ "detail": "Transaction with id=99 not found." }
```

---

## Design Decisions

### Why FastAPI?
FastAPI gives us automatic OpenAPI documentation, native Pydantic integration, dependency injection, and async support — all with less boilerplate than Flask/Django for pure API work. It's the modern standard for Python APIs.

### Why SQLAlchemy 2.0?
The 2.0 API is fully type-safe and explicit. Using `Session.query()` with typed models means IDE autocompletion and static analysis work correctly — important for maintainability at scale.

### Why SQLite?
Zero configuration for development and testing. The database layer is fully abstracted behind `DATABASE_URL` in `config.py` — swapping to PostgreSQL for production requires changing exactly one environment variable and removing `check_same_thread`.

### Why a Service Layer for Analytics?
Analytics logic involves multi-step aggregations, merging DB rows, and formatting output. Putting this in routes would violate single-responsibility and make the logic untestable in isolation. `analytics_service.py` is independently testable with just a DB session.

### Why `model_dump(exclude_unset=True)` for Updates?
This is the correct way to implement partial updates in Pydantic v2. Fields not included in the request body are not present in the serialized dict, so existing DB values are never accidentally overwritten with `None`.

### Why Composite Indexes?
The most common query pattern is `WHERE user_id = ? AND type = ?` or `WHERE user_id = ? AND date BETWEEN ? AND ?`. Composite indexes on `(user_id, type)`, `(user_id, date)`, and `(user_id, category)` ensure these scans are O(log n) rather than full table scans.

### Production Upgrade Path
| Concern | Current | Production Swap |
|---|---|---|
| Database | SQLite | PostgreSQL via `DATABASE_URL` |
| Migrations | `create_all()` | Alembic |
| Auth | None | JWT middleware in `core/` |
| Config | `.env` file | AWS SSM / Vault |
| Deployment | `uvicorn` | Gunicorn + uvicorn workers behind Nginx |
=======
# finance-tracker-backend
Finance Tracker Backend using FastAPI with analytics
>>>>>>> 78113ea0a684e95cb1f1ce551aba3adfc9ddd141
