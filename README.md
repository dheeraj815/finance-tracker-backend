# 💰 Finance Tracker API

A production-style REST API for managing personal financial transactions with analytics and reporting capabilities. Built using FastAPI with clean architecture and scalable backend design principles.

---

## 🚀 Features

* CRUD operations for transactions
* Income & Expense tracking
* User management system
* Filtering (user, category, type, date range)
* Pagination support (limit, offset)
* Financial analytics:

  * Total income
  * Total expenses
  * Net balance
  * Category-wise breakdown
  * Monthly summaries
* Health check endpoint
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
venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

---

## 🌐 API Access

* Base URL: http://127.0.0.1:8000
* Swagger Docs: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc
* Health Check: http://127.0.0.1:8000/health

---

## 📊 Key Endpoints

### Users

* POST /users → Create user
* GET /users → List users
* GET /users/{user_id} → Get user

### Transactions

* POST /transactions → Create transaction
* GET /transactions → List with filters
* GET /transactions/{id} → Get transaction
* PUT /transactions/{id} → Update
* DELETE /transactions/{id} → Delete

### Analytics

* GET /analytics/summary → Overall stats
* GET /analytics/category → Category breakdown
* GET /analytics/monthly → Monthly report

---

## 📌 Example Request

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

## 🧠 Design Highlights

* Modular architecture (routes, services, models)
* Separation of concerns
* Scalable backend design
* Clean and maintainable code
* Real-world API design practices

---

## 💡 Note

This API supports filtering, pagination, and analytical reporting similar to real-world fintech backend systems.

---

## 👨‍💻 Author

Dheeraj Muley
