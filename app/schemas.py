from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    message: str
    user: UserRead


class CalculationCreate(BaseModel):
    expression: str = Field(..., min_length=1)
    result: float


class CalculationUpdate(BaseModel):
    expression: Optional[str] = Field(None, min_length=1)
    result: Optional[float] = None


class CalculationRead(BaseModel):
    id: int
    expression: str
    result: float
    owner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)