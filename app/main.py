from fastapi import FastAPI, HTTPException, Path, Query
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field

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

class PostSchema(BaseModel):
    title: str = Field(min_length=5)
    content: str = Field(min_length=20)
    author: str = Field(pattern="^[a-zA-Z0-9]+$")
    category: CategoryType
    published: bool = False

class PostCreate(PostSchema):
    pass

class PostUpdate(PostSchema):
    pass

class Post(PostSchema):
    id: int

posts = [
    Post(id = 1, author = "johndoe",category = CategoryType.football, title="Dummy title1", content = "Football content by john doe"),
    Post(id = 2, author = "admin",category = CategoryType.basketball, title="Dummy title2", content = "Baskteball content by admin"),
    Post(id = 3, author = "johndoe",category = CategoryType.hockey, title="Dummy title3", content = "Hockey content by john doe"),
    Post(id = 4, author = "johndoe",category = CategoryType.football, title="Dummy title4", content = "Football content by john doe"),
    Post(id = 5, author = "admin",category = CategoryType.basketball, title="Dummy title5", content = "Baskteball content by admin"),
    Post(id = 6, author = "admin",category = CategoryType.basketball, title="Dummy title6", content = "Baskteball content by admin")
]


@app.post("/posts/")
async def create_post(post_create: PostCreate) -> Post:
    post = Post(**post_create.model_dump())
    posts.append(
        post
    )
    return post

@app.put("/posts/{post_id}")
async def update_post(post_id: Annotated[int, Path(ge=0)], post_update: PostUpdate):
    filtered_posts = [[i, post] for i, post in enumerate(posts) if post.id == post_id]
    if len(filtered_posts) == 0:
        raise HTTPException(status_code=404, detail="Not found")
    index, _ = filtered_posts[0]
    posts[index] = Post(**post_update.model_dump(), id=post_id)
    return posts[index]


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
