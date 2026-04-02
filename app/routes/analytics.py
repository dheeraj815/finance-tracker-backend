"""
app/routes/analytics.py

Analytics endpoints — thin controllers that delegate to analytics_service.py.
These endpoints expose financial insights without leaking query logic into routes.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CategoryResponse, MonthlyResponse, SummaryResponse
from app.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/summary",
    response_model=SummaryResponse,
    summary="Get overall financial summary",
)
def get_summary(
    user_id: Optional[int] = Query(None, description="Scope summary to a specific user"),
    db: Session = Depends(get_db),
) -> SummaryResponse:
    """
    Returns aggregated totals:
    - Total income
    - Total expenses
    - Net balance (income − expenses)
    - Total transaction count

    Optionally scoped to a single user.
    """
    return analytics_service.get_summary(db, user_id=user_id)


@router.get(
    "/category",
    response_model=CategoryResponse,
    summary="Get category-wise breakdown",
)
def get_category_breakdown(
    user_id: Optional[int] = Query(None, description="Scope to a specific user"),
    db: Session = Depends(get_db),
) -> CategoryResponse:
    """
    Returns per-category aggregations split by transaction type.
    Results are sorted by total amount (descending) — highest spend first.
    Useful for identifying top spending categories.
    """
    breakdown = analytics_service.get_category_breakdown(db, user_id=user_id)
    return CategoryResponse(breakdown=breakdown)


@router.get(
    "/monthly",
    response_model=MonthlyResponse,
    summary="Get monthly income vs. expense summary",
)
def get_monthly_summary(
    user_id: Optional[int] = Query(None, description="Scope to a specific user"),
    db: Session = Depends(get_db),
) -> MonthlyResponse:
    """
    Returns a chronological month-by-month breakdown of income, expenses,
    and net balance. Ideal for trend charts and period-over-period analysis.
    """
    monthly = analytics_service.get_monthly_summary(db, user_id=user_id)
    return MonthlyResponse(monthly_summary=monthly)
