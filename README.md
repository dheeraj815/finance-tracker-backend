# Finance Tracker API

A simple and production-style REST API for managing personal financial transactions using FastAPI.

---

## Features

* CRUD operations for transactions
* Track income and expenses
* Basic analytics (income, expenses, balance)
* Clean backend structure

---

## Tech Stack

* FastAPI
* SQLAlchemy
* SQLite
* Uvicorn

---

## Project Structure

```
finance_tracker/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── routes/
│   │   ├── users.py
│   │   ├── transactions.py
│   │   └── analytics.py
│   └── services/
│       └── analytics_service.py
├── requirements.txt
├── README.md
```

---

## Setup

```bash
git clone https://github.com/dheeraj815/finance-tracker-backend.git
cd finance-tracker-backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

---

## Run

```bash
uvicorn app.main:app --reload
```

---

## API Docs

http://127.0.0.1:8000/docs

---

## Author

Dheeraj Muley
