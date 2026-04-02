"""
app/services/analytics_service.py

Business logic for financial analytics.
All aggregation is performed at the database level using SQLAlchemy
expressions — never pulling raw rows into Python to sum them up.
This is the correct approach for production systems at any data scale.
"""

from typing import Optional, List
from collections import defaultdict

from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from app.models import Transaction, TransactionType
from app.schemas import (
    SummaryResponse,
    CategorySummary,
    MonthlySummary,
)


def get_summary(db: Session, user_id: Optional[int] = None) -> SummaryResponse:
    """
    Compute total income, total expenses, net balance, and transaction count.
    Single aggregation query groups all metrics in one DB round-trip.
    """
    query = db.query(
        Transaction.type,
        func.sum(Transaction.amount).label("total"),
        func.count(Transaction.id).label("count"),
    ).group_by(Transaction.type)

    if user_id is not None:
        query = query.filter(Transaction.user_id == user_id)

    rows = query.all()

    total_income = 0.0
    total_expenses = 0.0
    transaction_count = 0

    for row in rows:
        if row.type == TransactionType.INCOME:
            total_income = round(row.total, 2)
        elif row.type == TransactionType.EXPENSE:
            total_expenses = round(row.total, 2)
        transaction_count += row.count

    return SummaryResponse(
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=round(total_income - total_expenses, 2),
        transaction_count=transaction_count,
    )


def get_category_breakdown(
    db: Session, user_id: Optional[int] = None
) -> List[CategorySummary]:
    """
    Aggregate spending and income by category.
    Returns a flat list sorted by total (descending) for easy ranking.
    """
    query = db.query(
        Transaction.category,
        Transaction.type,
        func.sum(Transaction.amount).label("total"),
        func.count(Transaction.id).label("count"),
    ).group_by(Transaction.category, Transaction.type)

    if user_id is not None:
        query = query.filter(Transaction.user_id == user_id)

    rows = query.order_by(func.sum(Transaction.amount).desc()).all()

    return [
        CategorySummary(
            category=row.category,
            type=row.type,
            total=round(row.total, 2),
            count=row.count,
        )
        for row in rows
    ]


def get_monthly_summary(
    db: Session, user_id: Optional[int] = None
) -> List[MonthlySummary]:
    """
    Group transactions by year-month and compute income vs. expense totals.
    Uses SQL EXTRACT for date decomposition — DB-native and efficient.
    The result is assembled into structured monthly snapshots in Python.
    """
    query = db.query(
        extract("year", Transaction.date).label("year"),
        extract("month", Transaction.date).label("month"),
        Transaction.type,
        func.sum(Transaction.amount).label("total"),
    ).group_by("year", "month", Transaction.type)

    if user_id is not None:
        query = query.filter(Transaction.user_id == user_id)

    rows = query.order_by("year", "month").all()

    # Merge income/expense rows for the same year-month into one summary object
    month_map: dict = defaultdict(lambda: {"income": 0.0, "expense": 0.0})

    for row in rows:
        key = (int(row.year), int(row.month))
        if row.type == TransactionType.INCOME:
            month_map[key]["income"] = round(row.total, 2)
        else:
            month_map[key]["expense"] = round(row.total, 2)

    summaries = [
        MonthlySummary(
            year=year,
            month=month,
            total_income=data["income"],
            total_expenses=data["expense"],
            net_balance=round(data["income"] - data["expense"], 2),
        )
        for (year, month), data in sorted(month_map.items())
    ]

    return summaries
