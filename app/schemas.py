"""
app/schemas.py

Pydantic v2 schemas for request validation and response serialization.
Separating Input (Create/Update) from Output schemas gives us fine-grained
control over what data is read vs. written — a key production pattern.
"""

import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

from app.models import TransactionType


# ---------------------------------------------------------------------------
# User Schemas
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Alice Johnson"])
    email: EmailStr = Field(..., examples=["alice@example.com"])


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str


class UserWithTransactions(UserResponse):
    """Extended user view that includes transaction list — used sparingly."""
    transactions: List["TransactionResponse"] = []


# ---------------------------------------------------------------------------
# Transaction Schemas
# ---------------------------------------------------------------------------

class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Must be a positive value", examples=[1500.00])
    type: TransactionType = Field(..., examples=["income"])
    category: str = Field(..., min_length=1, max_length=100, examples=["Salary"])
    date: datetime.date = Field(default_factory=datetime.date.today)
    description: Optional[str] = Field(None, max_length=500, examples=["Monthly salary deposit"])
    user_id: int = Field(..., gt=0)

    @field_validator("category")
    @classmethod
    def normalize_category(cls, v: str) -> str:
        """Normalize category to title-case for consistent grouping."""
        return v.strip().title()


class TransactionUpdate(BaseModel):
    """All fields optional — supports partial (PATCH-style) updates via PUT."""
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    date: Optional[datetime.date] = None
    description: Optional[str] = Field(None, max_length=500)

    @field_validator("category")
    @classmethod
    def normalize_category(cls, v: Optional[str]) -> Optional[str]:
        return v.strip().title() if v else v


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: float
    type: TransactionType
    category: str
    date: datetime.date
    description: Optional[str]
    user_id: int


# ---------------------------------------------------------------------------
# Analytics Schemas (response-only)
# ---------------------------------------------------------------------------

class SummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    transaction_count: int


class CategorySummary(BaseModel):
    category: str
    type: TransactionType
    total: float
    count: int


class CategoryResponse(BaseModel):
    breakdown: List[CategorySummary]


class MonthlySummary(BaseModel):
    year: int
    month: int
    total_income: float
    total_expenses: float
    net_balance: float


class MonthlyResponse(BaseModel):
    monthly_summary: List[MonthlySummary]


# Resolve forward reference for UserWithTransactions
UserWithTransactions.model_rebuild()
