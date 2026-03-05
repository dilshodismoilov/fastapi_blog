from fastapi import FastAPI, HTTPException, Path, Query, Body
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

class PostPartialUpdate(PostSchema):
    title: str | None = Field(default = None, min_length=5)
    content: str | None = Field(default = None, min_length=20)
    author: str | None = Field(default = None, pattern="^[a-zA-Z0-9]+$")
    category: CategoryType | None = None
    published: bool | None = None

posts = {
    1: Post(id = 1, author = "johndoe",category = CategoryType.football, title="Dummy title1", content = "Football content by john doe"),
    2: Post(id = 2, author = "admin",category = CategoryType.basketball, title="Dummy title2", content = "Baskteball content by admin"),
    3: Post(id = 3, author = "johndoe",category = CategoryType.hockey, title="Dummy title3", content = "Hockey content by john doe"),
    4: Post(id = 4, author = "johndoe",category = CategoryType.football, title="Dummy title4", content = "Football content by john doe"),
    5: Post(id = 5, author = "admin",category = CategoryType.basketball, title="Dummy title5", content = "Baskteball content by admin"),
    6: Post(id = 6, author = "admin",category = CategoryType.basketball, title="Dummy title6", content = "Baskteball content by admin")
}


@app.post("/posts/")
async def create_post(post_create: PostCreate) -> Post:
    post_id = len(posts) + 1
    post = Post(**post_create.model_dump(), id=post_id)
    posts.update({post_id: post})
    return post

@app.put("/posts/{post_id}")
async def update_post(post_id: Annotated[int, Path(ge=0)], post_update: PostUpdate):
    post = posts.get(post_id, None)
    if post is None:
        raise HTTPException(status_code=404, detail="Not found")
    new_post = Post(**post_update.model_dump(), id=post_id)
    posts[post.id] = new_post
    return new_post

@app.patch("/posts/{post_id}")
async def partial_update_post(post_id: Annotated[int, Path(ge=0)], post_partial_update: Annotated[PostPartialUpdate, Body()]):
    post = posts.get(post_id, None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    update_data = post_partial_update.model_dump(exclude_unset=True)
    updated_post = post.model_copy(update=update_data)
    posts[post_id] = updated_post
    return updated_post


@app.get("/posts/")
async def read_posts(
    author: str | None = None, 
    limit: Annotated[int | None, Query(ge=0)] = None,
    offset: Annotated[int | None, Query(ge=0)] = None,
    categories: Annotated[list[CategoryType] | None, Query()] = None    
):
    returning_posts = list(posts.values())
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
    if post_id not in posts:
        raise HTTPException(status_code = 404, detail = "Post not found")
    return {"post_id": post_id, "content": posts[post_id]}
