"""
app/routes/transactions.py

Transaction CRUD endpoints with filtering, sorting, and pagination.
Route handlers are intentionally thin — all data access is delegated to crud.py.
"""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.models import TransactionType
from app.schemas import TransactionCreate, TransactionResponse, TransactionUpdate

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new transaction",
)
def create_transaction(
    payload: TransactionCreate, db: Session = Depends(get_db)
) -> TransactionResponse:
    """
    Record a new income or expense transaction.
    The referenced user_id must exist — returns 404 otherwise.
    """
    user = crud.get_user(db, payload.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={payload.user_id} not found.",
        )
    return crud.create_transaction(db, payload)


@router.get(
    "/",
    response_model=List[TransactionResponse],
    summary="List transactions with optional filters",
)
def list_transactions(
    user_id: Optional[int] = Query(None, description="Filter by user"),
    type: Optional[TransactionType] = Query(None, description="Filter by type: income | expense"),
    category: Optional[str] = Query(None, description="Filter by category (case-insensitive)"),
    date_from: Optional[date] = Query(None, description="Start of date range (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End of date range (YYYY-MM-DD)"),
    limit: int = Query(default=20, ge=1, le=100, description="Results per page"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db),
) -> List[TransactionResponse]:
    """
    Retrieve transactions with composable filters.
    All filters are optional and combinable. Results are sorted newest-first.
    """
    if date_from and date_to and date_from > date_to:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="date_from cannot be later than date_to.",
        )

    return crud.get_transactions(
        db,
        user_id=user_id,
        type=type,
        category=category,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    summary="Get a single transaction",
)
def get_transaction(
    transaction_id: int, db: Session = Depends(get_db)
) -> TransactionResponse:
    """Fetch a transaction by its ID. Returns 404 if not found."""
    transaction = crud.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id={transaction_id} not found.",
        )
    return transaction


@router.put(
    "/{transaction_id}",
    response_model=TransactionResponse,
    summary="Update a transaction",
)
def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
) -> TransactionResponse:
    """
    Partially update a transaction.
    Only provided fields are changed — omitted fields retain their current values.
    """
    transaction = crud.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id={transaction_id} not found.",
        )

    if not payload.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No update fields provided.",
        )

    return crud.update_transaction(db, transaction, payload)


@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a transaction",
)
def delete_transaction(
    transaction_id: int, db: Session = Depends(get_db)
) -> None:
    """Permanently delete a transaction by ID."""
    transaction = crud.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id={transaction_id} not found.",
        )
    crud.delete_transaction(db, transaction)
