"""
app/routes/users.py

User management endpoints.
Thin controller: validate input → call CRUD → return response.
No business logic lives here.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """
    Create a new user account.
    Returns 409 if the email address is already registered.
    """
    existing = crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with email '{payload.email}' already exists.",
        )
    return crud.create_user(db, payload)


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List all users",
)
def list_users(
    limit: int = Query(default=20, ge=1, le=100, description="Results per page"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db),
) -> List[UserResponse]:
    """Return a paginated list of all registered users."""
    return crud.get_users(db, limit=limit, offset=offset)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get a user by ID",
)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    """Fetch a single user by their ID. Returns 404 if not found."""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found.",
        )
    return user
