from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Annotated
from sqlalchemy.orm import Session
from models import Base, User, Post
from database import engine, session_local
from schemas import CreateUser, CreatePost, PostResponse, User as DbUser

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/create/", response_model=DbUser)
async def create_user(user: CreateUser, db: Session = Depends(get_db)) -> JSONResponse:
    new_user = User(name=user.name, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(
        status_code=201,
        content={"message": "User created successfully", "user": user.model_dump()}
    )


@app.post("/posts/create/", response_model=PostResponse)
async def create_post(post: CreatePost, db: Session = Depends(get_db)) -> JSONResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return JSONResponse(
        status_code=201,
        content={"message": "Post created successfully", "post": post.model_dump()}
    )


@app.get("/posts/all/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()
