from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Role(str, Enum):
    admin = "admin"
    user = "user"


class UserModel(BaseModel):
    username: str
    password: str
    full_name: str
    role: Role
    cart: list[str]
    avatar_url: Optional[str]


class UserCreateModel(BaseModel):
    email: str
    username: str
    password: str
    full_name: str
    role: Role


class UserUpdateModel(BaseModel):
    username: Optional[str]
    full_name: Optional[str]
    role: Optional[Role]
    avatar_url: Optional[str]


class UserLoginModel(BaseModel):
    username: str
    password: str


class UserChangePasswordModel(BaseModel):
    password: str
    new_password: str


class CartModel(BaseModel):
    book_id: str
    booksnum: int
