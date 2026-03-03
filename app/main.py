from fastapi import FastAPI, HTTPException, Path, Query
from enum import Enum
from typing import Annotated
from pydantic import BaseModel

class CategoryType(str, Enum):
    football = "football"
    basketball = "basketball"
    hockey = "hockey"

app = FastAPI()
post_storage = {
    1: "first post content",
    2: "second post content",
    3: "third post content",
    4: "fourth post content",
    5: "fifth post content",
    6: "sixth post content",
}

user_storage = {
    "johndoe": "johndoe@mail.com",
    "admin": "admin@admin.com"
}

@app.get("/users/{user_name}")
async def read_user(user_name: str):
    if user_name not in user_storage:
        raise HTTPException(status_code = 404, detail = "User not found")
    return {"user_name": user_name, "email": user_storage[user_name]}

@app.get("/posts/categories/{category_type}")
async def read_posts_by_category(category_type: CategoryType):
    if category_type == CategoryType.football:
        return {"category_type": category_type, "message": "you like football?"}
    
    if category_type == CategoryType.basketball:
        return {"category_type": category_type, "message": "Aomine Daiki is my favourite basketball player"}

    return {"category_type": category_type, "message": "hockey is very cool"}

class Post(BaseModel):
    author: str
    category: CategoryType
    content: str

posts = [
    Post(author = "johndoe",category = CategoryType.football, content = "Football content by john doe"),
    Post(author = "admin",category = CategoryType.basketball, content = "Baskteball content by admin"),
    Post(author = "johndoe",category = CategoryType.hockey, content = "Hockey content by john doe"),
    Post(author = "johndoe",category = CategoryType.football, content = "Football content by john doe"),
    Post(author = "admin",category = CategoryType.basketball, content = "Baskteball content by admin"),
    Post(author = "admin",category = CategoryType.basketball, content = "Baskteball content by admin")
]

@app.get("/posts/")
async def read_posts(
    author: str | None = None, 
    limit: Annotated[int | None, Query(ge=0)] = None,
    offset: Annotated[int | None, Query(ge=0)] = None,
    categories: Annotated[list[CategoryType] | None, Query()] = None    
):
    returning_posts = posts[:]
    if author:
        returning_posts = [post for post in returning_posts if post.author == author]
    if offset is not None:
        returning_posts = returning_posts[offset:]
    if limit is not None:
        returning_posts = returning_posts[:limit]
    if categories:
        returning_posts = [post for post in returning_posts if post.category in categories]
    
    return returning_posts

@app.get("/posts/{post_id}")
async def read_post(post_id: Annotated[int, Path(gt=0)]):
    if post_id not in post_storage:
        raise HTTPException(status_code = 404, detail = "Post not found")
    return {"post_id": post_id, "content": post_storage[post_id]}
