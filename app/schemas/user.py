from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from app.models.users import UserRole


class UserCreate(BaseModel):
    name: Annotated[str, Field(max_length=50)]
    email: EmailStr
    password: str
    role: UserRole = UserRole.viewer


class UserOut(BaseModel):
    id: int
    name: Annotated[str, Field(max_length=50)]
    email: EmailStr
    role: UserRole
    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
