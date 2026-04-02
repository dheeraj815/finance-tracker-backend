"""
app/crud.py

Data access layer — all direct database interaction lives here.
Routes call CRUD functions; CRUD functions talk to the DB.
This separation makes the codebase testable and maintainable.
"""

from datetime import date
from typing import Optional, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Transaction, TransactionType, User
from app.schemas import TransactionCreate, TransactionUpdate, UserCreate


# ---------------------------------------------------------------------------
# User CRUD
# ---------------------------------------------------------------------------

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, limit: int = 20, offset: int = 0) -> List[User]:
    return db.query(User).offset(offset).limit(limit).all()


def create_user(db: Session, payload: UserCreate) -> User:
    user = User(name=payload.name, email=payload.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------------------------------------------------------------------------
# Transaction CRUD
# ---------------------------------------------------------------------------

def get_transaction(db: Session, transaction_id: int) -> Optional[Transaction]:
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def get_transactions(
    db: Session,
    user_id: Optional[int] = None,
    type: Optional[TransactionType] = None,
    category: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    limit: int = 20,
    offset: int = 0,
) -> List[Transaction]:
    """
    Fetch transactions with composable filters.
    Only applies filters that are explicitly provided — clean and extensible.
    """
    query = db.query(Transaction)

    if user_id is not None:
        query = query.filter(Transaction.user_id == user_id)
    if type is not None:
        query = query.filter(Transaction.type == type)
    if category is not None:
        query = query.filter(Transaction.category == category.strip().title())
    if date_from is not None:
        query = query.filter(Transaction.date >= date_from)
    if date_to is not None:
        query = query.filter(Transaction.date <= date_to)

    return (
        query
        .order_by(Transaction.date.desc(), Transaction.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def count_transactions(
    db: Session,
    user_id: Optional[int] = None,
    type: Optional[TransactionType] = None,
    category: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> int:
    """Return total count for the same filter set — used for pagination metadata."""
    query = db.query(func.count(Transaction.id))

    if user_id is not None:
        query = query.filter(Transaction.user_id == user_id)
    if type is not None:
        query = query.filter(Transaction.type == type)
    if category is not None:
        query = query.filter(Transaction.category == category.strip().title())
    if date_from is not None:
        query = query.filter(Transaction.date >= date_from)
    if date_to is not None:
        query = query.filter(Transaction.date <= date_to)

    return query.scalar() or 0


def create_transaction(db: Session, payload: TransactionCreate) -> Transaction:
    transaction = Transaction(**payload.model_dump())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def update_transaction(
    db: Session, transaction: Transaction, payload: TransactionUpdate
) -> Transaction:
    """
    Apply only the fields that were explicitly sent in the update payload.
    Uses model_dump(exclude_unset=True) so missing fields don't overwrite
    existing values — correct partial-update semantics.
    """
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(db: Session, transaction: Transaction) -> None:
    db.delete(transaction)
    db.commit()
