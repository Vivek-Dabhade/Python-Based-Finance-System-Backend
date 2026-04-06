from datetime import date

from app.core.database import session
from app.core.security import hash_password
from app.models.transactions import Transaction, TransactionType
from app.models.users import User, UserRole


def seed():
    db = session()
    try:
        # creating 3 users — admin, analyst, viewer
        admin = User(
            name="Admin User",
            email="admin@finance.com",
            hashed_password=hash_password("admin123"),
            role=UserRole.admin,
        )

        db.add(admin)
        analyst = User(
            name="Analyst",
            email="analyst@finance.com",
            hashed_password=hash_password("anaylst123"),
            role=UserRole.analyst,
        )
        db.add(analyst)
        viewer = User(
            name="Viewer",
            email="viewer@finance.com",
            hashed_password=hash_password("viewer123"),
            role=UserRole.viewer,
        )
        db.add(viewer)
        db.flush()
        # creating 10 transactions — mix of income and expense
        transactions = [
            Transaction(
                amount=50000,
                type=TransactionType.income,
                category="salary",
                date=date(2026, 1, 1),
                notes="January salary",
                user_id=admin.id,
            ),
            Transaction(
                amount=2000,
                type=TransactionType.expense,
                category="food",
                date=date(2026, 1, 5),
                notes="Groceries",
                user_id=admin.id,
            ),
            Transaction(
                amount=80000,
                type=TransactionType.income,
                category="freelance",
                date=date(2026, 1, 10),
                notes="Client project",
                user_id=admin.id,
            ),
            Transaction(
                amount=15000,
                type=TransactionType.expense,
                category="rent",
                date=date(2026, 1, 15),
                notes="Monthly rent",
                user_id=admin.id,
            ),
            Transaction(
                amount=3000,
                type=TransactionType.expense,
                category="transport",
                date=date(2026, 2, 1),
                notes="Fuel",
                user_id=admin.id,
            ),
            Transaction(
                amount=120000,
                type=TransactionType.income,
                category="salary",
                date=date(2026, 2, 1),
                notes="February salary",
                user_id=admin.id,
            ),
            Transaction(
                amount=5000,
                type=TransactionType.expense,
                category="entertainment",
                date=date(2026, 2, 10),
                notes="Movies and dining",
                user_id=admin.id,
            ),
            Transaction(
                amount=25000,
                type=TransactionType.income,
                category="investment",
                date=date(2026, 2, 15),
                notes="Dividend",
                user_id=admin.id,
            ),
            Transaction(
                amount=8000,
                type=TransactionType.expense,
                category="utilities",
                date=date(2026, 3, 1),
                notes="Electricity and water",
                user_id=admin.id,
            ),
            Transaction(
                amount=200000,
                type=TransactionType.income,
                category="bonus",
                date=date(2026, 3, 15),
                notes="Annual bonus",
                user_id=admin.id,
            ),
        ]

        for t in transactions:
            db.add(t)

        db.commit()
        print("Seeded successfully")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
