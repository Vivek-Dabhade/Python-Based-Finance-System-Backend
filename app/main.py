from fastapi import FastAPI

from app.api import auth
from app.api import transactions as transaction_routes
from app.api import users as user_routes
from app.core.database import Base
from app.core.database import pg_db as engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Tracking System")

app.include_router(auth.router)
app.include_router(transaction_routes.router)
app.include_router(user_routes.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Finance System API is running"}
