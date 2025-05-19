from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(UserSchema):
    username: str
    email: EmailStr
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class UserDB(UserSchema):
    id: int
