from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI()

data = [
    {'id': 1, 'title': 'News 1', 'text': 'Text 1'},
    {'id': 2, 'title': 'News 2', 'text': 'Text 2'},
    {'id': 3, 'title': 'News 3', 'text': 'Text 3'}
]


class Item(BaseModel):
    id: int
    title: str
    text: str


@app.get("/items")
async def get_items() -> List[Item]:
    return [Item(**post) for post in data]


@app.get("/items/{id}")
async def get_item(id: int) -> Item:
    for post in data:
        if post['id'] == id:
            return Item(**post)

    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/search")
async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Item]]:
    if post_id:
        for post in data:
            if post['id'] == post_id:
                return {'data': Item(**post)}

        raise HTTPException(status_code=404, detail="Item not found")

    else:
        return {'data': None}
