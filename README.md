# 💰 Finance Tracker API

A **production-style REST API** for managing personal financial transactions — built using FastAPI, SQLAlchemy, and SQLite. This project demonstrates clean architecture, modular design, and scalable backend engineering practices.

---

## 🚀 Features

* CRUD operations for financial transactions
* Income & Expense tracking
* Category-wise filtering
* Date range filtering
* Pagination support
* Financial analytics:

  * Total income
  * Total expenses
  * Net balance
  * Category breakdown
  * Monthly summary
* Clean modular architecture

---

## 🛠️ Tech Stack

* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* Uvicorn

---

## 📂 Project Structure

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

## ⚙️ Setup & Installation

```bash
git clone https://github.com/dheeraj815/finance-tracker-backend.git
cd finance-tracker-backend

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

---

## ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

Open in browser:

* http://127.0.0.1:8000/docs (Swagger UI)
* http://127.0.0.1:8000/redoc

---

## 📊 API Endpoints

### Users

* POST /users
* GET /users

### Transactions

* POST /transactions
* GET /transactions
* PUT /transactions/{id}
* DELETE /transactions/{id}

### Analytics

* GET /analytics/summary
* GET /analytics/category
* GET /analytics/monthly

---

## 📌 Example JSON

### Create Transaction

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

## 🧠 Design Approach

* Modular structure (routes, services, models)
* Separation of concerns
* Clean and readable code
* Scalable backend design

---

## 👨‍💻 Author

Dheeraj Muley
