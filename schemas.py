from typing import Annotated
from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    name: str
    age: int


class User(BaseUser):
    id: int

    class Config:
        from_attributes = True


class CreateUser(BaseUser):
    pass


class BasePost(BaseModel):
    title: str
    body: str


class PostResponse(BasePost):
    id: int
    author: User

    class Config:
        from_attributes = True


class CreatePost(BasePost):
    pass
