from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.transactions import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


def create_transaction(db: Session, data: TransactionCreate, user_id: int):
    transaction = Transaction(**data.model_dump(), user_id=user_id)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def get_transactions(
    db: Session, user_id: int, type=None, category=None, date_from=None, date_to=None
):
    query = db.query(Transaction).filter(Transaction.user_id == user_id)

    if type:
        query = query.filter(Transaction.type == type)
    if date_from:
        query = query.filter(Transaction.date >= date_from)
    if date_to:
        query = query.filter(Transaction.date <= date_to)
    if category:
        query = query.filter(Transaction.category == category)

    return query.all()


def get_transaction_by_id(db: Session, user_id: int, transaction_id: int):
    query = db.query(Transaction).filter(
        Transaction.id == transaction_id, Transaction.user_id == user_id
    )
    return query.first()


def update_transaction(db: Session, transaction: Transaction, data: TransactionUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(transaction, field, value)
    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(db: Session, transaction: Transaction):
    db.delete(transaction)
    db.commit()


def get_summary(db: Session, user_id: int):
    total_income = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(Transaction.user_id == user_id, Transaction.type == "income")
        .scalar()
    )

    total_expense = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(Transaction.user_id == user_id, Transaction.type == "expense")
        .scalar()
    )

    balance = total_income - total_expense

    recent = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.date.desc())
        .limit(5)
        .all()
    )

    category_totals = (
        db.query(Transaction.category, func.sum(Transaction.amount).label("total"))
        .filter(Transaction.user_id == user_id)
        .group_by(Transaction.category)
        .all()
    )
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "recent": [
            {
                "id": t.id,
                "amount": t.amount,
                "type": t.type,
                "category": t.category,
                "date": str(t.date),
                "notes": t.notes,
            }
            for t in recent
        ],
        "category": [
            {"category": row.category, "total": row.total} for row in category_totals
        ],
    }
