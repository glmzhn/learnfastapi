from fastapi import FastAPI, HTTPException, Path, Query, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Annotated

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int


class Item(BaseModel):
    id: int
    title: str
    text: str
    author: User


class CreateItem(BaseModel):
    title: str
    text: str
    author_id: int


class CreateUser(BaseModel):
    name: Annotated[str, Field(..., title="User's name", min_length=2, max_length=255)]
    age: Annotated[int, Field(..., title="User's age", ge=1, le=130)]


users = [
    {'id': 1, 'name': 'Oskar', 'age': 23},
    {'id': 2, 'name': 'Joanne', 'age': 45},
    {'id': 3, 'name': 'Socrates', 'age': 37},
]


posts = [
    {'id': 1, 'title': 'Portrait of Dorian Gray', 'text': 'Text 1', 'author': users[0]},
    {'id': 2, 'title': 'Harry Potter', 'text': 'Text 2', 'author': users[1]},
    {'id': 3, 'title': 'I Know Nothing', 'text': 'Text 3', 'author': users[2]},
]


@app.get("/items")
async def get_items() -> List[Item]:
    return [Item(**post) for post in posts]


@app.post("/items/create")
async def create_item(item: CreateItem) -> Item:
    author = next((user for user in users if user['id'] == item.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_item_id = len(posts) + 1
    new_post = {'id': new_item_id, 'title': item.title, 'text': item.text, 'author': author}
    posts.append(new_post)
    return Item(**new_post)


@app.get("/items/{id}")
async def get_item(id: Annotated[int, Path(..., title="You Have to Specify Item's id", ge=1)]) -> Item:
    for post in posts:
        if post['id'] == id:
            return Item(**post)

    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/users/create")
async def create_user(user: Annotated[CreateUser, Body(..., example={"name": "InstanceName", "age": "23"})]) -> User:
    new_user_id = len(users) + 1
    new_user = {'id': new_user_id, 'name': user.name, 'age': user.age}
    posts.append(new_user)
    return User(**new_user)


@app.get("/search")
async def search(post_id: Annotated[Optional[int], Query(title="Specify Item's id to search for it", ge=1)]) -> Dict[str, Optional[Item]]:
    if post_id:
        for post in posts:
            if post['id'] == post_id:
                return {'data': Item(**post)}

        raise HTTPException(status_code=404, detail="Item not found")

    else:
        return {'data': None}
