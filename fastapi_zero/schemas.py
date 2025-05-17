from pydantic import BaseModel, EmailStr

class message(BaseModel):
    message: str


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
