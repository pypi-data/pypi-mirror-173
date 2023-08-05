from typing import Optional

from pydantic import BaseModel, constr, EmailStr


class UserLogin(BaseModel):
    email: str
    password: str


class User(BaseModel):
    first_name: Optional[constr(min_length=1, max_length=50)]
    last_name: Optional[constr(min_length=1, max_length=50)]
    email: Optional[EmailStr]
    password: Optional[constr(min_length=4)]
    scopes: Optional[list[str]]


class Token(BaseModel):
    token: str
