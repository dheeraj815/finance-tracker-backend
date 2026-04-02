# Finance Tracker API

A clean and production-style REST API for managing personal financial transactions using FastAPI, SQLAlchemy, and SQLite.

---

## Features

* Create, read, update, and delete transactions
* Track income and expenses
* Filter by category and date
* Basic financial analytics (income, expenses, balance)
* Clean modular backend structure

---

## Tech Stack

* FastAPI
* SQLAlchemy
* Pydantic
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
│   └── services/
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

## Run Server

```bash
uvicorn app.main:app --reload
```

---

## API Docs

Open in browser:

http://127.0.0.1:8000/docs

---

## Example Request

```json
{
  "amount": 5000,
  "type": "income",
  "category": "salary",
  "description": "monthly salary",
  "user_id": 1
}
```

---

## Author

Dheeraj Muley
