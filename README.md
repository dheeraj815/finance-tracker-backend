# 💰 Finance Tracker API

🚀 A **production-ready REST API** for managing personal financial transactions — built with **FastAPI, SQLAlchemy, and SQLite**.

This project demonstrates **clean architecture, modular backend design, and scalable API development practices**, making it suitable for real-world backend systems.

---

## ✨ Key Highlights

* ⚡ High-performance API using FastAPI
* 🧱 Clean and modular architecture
* 📊 Built-in financial analytics engine
* 🔍 Advanced filtering (date, category, type)
* 📄 Pagination support
* 🧪 Ready for extension and scaling

---

## 🚀 Features

### 📌 Transaction Management

* Create, read, update, delete transactions
* Track **income & expenses**
* Category-based organization

### 📊 Analytics Engine

* Total income & expenses
* Net balance calculation
* Category-wise breakdown
* Monthly financial summary

### 🔍 Query Capabilities

* Filter by date range
* Filter by category/type
* Pagination for large datasets

---

## 🛠️ Tech Stack

| Technology | Purpose         |
| ---------- | --------------- |
| FastAPI    | API framework   |
| SQLAlchemy | ORM             |
| Pydantic   | Data validation |
| SQLite     | Database        |
| Uvicorn    | ASGI server     |

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
venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
uvicorn app.main:app --reload
```

---

## 🌐 API Documentation

* http://127.0.0.1:8000/docs
* http://127.0.0.1:8000/redoc

---

## 📊 API Endpoints

### 👤 Users

* POST /users
* GET /users

### 💸 Transactions

* POST /transactions
* GET /transactions
* PUT /transactions/{id}
* DELETE /transactions/{id}

### 📈 Analytics

* GET /analytics/summary
* GET /analytics/category
* GET /analytics/monthly

---

## 📌 Sample Request

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

## 🧠 Architecture

* Clean separation of concerns
* Modular routing & service layers
* Scalable backend structure
* Maintainable code

---

## 🚀 Future Improvements

* JWT Authentication
* PostgreSQL
* Docker
* Cloud deployment

---

## 👨‍💻 Author

Dheeraj Muley

---

## ⭐ Final Note

This project demonstrates **real-world backend development practices and scalable system design**.
