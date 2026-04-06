from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, role_validation
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate
from app.services.transaction_services import (
    create_transaction,
    delete_transaction,
    get_summary,
    get_transaction_by_id,
    get_transactions,
    update_transaction,
)

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionOut, status_code=201)
def create(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(role_validation("admin")),
):
    transaction = create_transaction(db, data, current_user.id)
    return transaction


@router.get("/", response_model=list[TransactionOut])
def list_transactions(
    type=None,
    category=None,
    date_from=None,
    date_to=None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    fetch_transaction = get_transactions(
        db, current_user.id, type, category, date_from, date_to
    )
    return fetch_transaction


@router.get("/summary")
def summary(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_summary(db, current_user.id)


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_one(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    transaction = get_transaction_by_id(db, current_user.id, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.patch("/{transaction_id}", response_model=TransactionOut)
def update_trans(
    transaction_id: int,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(role_validation("admin")),
):
    transaction = get_transaction_by_id(db, current_user.id, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return update_transaction(db, transaction, data)


@router.delete("/{transaction_id}", status_code=204)
def delete_trans(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(role_validation("admin")),
):
    transaction = get_transaction_by_id(db, current_user.id, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    delete_transaction(db, transaction)
