from pydantic import BaseModel, EmailStr, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class UserList(BaseModel):
    users: list[UserPublic]
