"""
app/models.py

SQLAlchemy ORM models representing the database schema.
Designed with proper relationships, indexes, and constraints
to ensure data integrity and query performance.
"""

from datetime import date
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Text,
    ForeignKey,
    Enum as SAEnum,
    Index,
)
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class TransactionType(str, enum.Enum):
    """Strict enum for transaction type — enforced at the DB and app layer."""
    INCOME = "income"
    EXPENSE = "expense"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)

    # Cascade delete: removing a user removes their transactions
    transactions = relationship(
        "Transaction",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(SAEnum(TransactionType), nullable=False)
    category = Column(String(100), nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="transactions")

    # Composite indexes to accelerate the most common query patterns
    __table_args__ = (
        Index("ix_transactions_user_type", "user_id", "type"),
        Index("ix_transactions_user_date", "user_id", "date"),
        Index("ix_transactions_user_category", "user_id", "category"),
    )

    def __repr__(self) -> str:
        return (
            f"<Transaction id={self.id} type={self.type.value} "
            f"amount={self.amount} category={self.category!r}>"
        )
