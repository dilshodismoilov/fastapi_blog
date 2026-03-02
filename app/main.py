from fastapi import FastAPI
from schemas import UserCreate, UserLogin, UserResponse
from auth import hash_password, verify_jwt_token, create_jwt_token, verify_password
app = FastAPI()

@app.post('/register')
def register_user(user_create: UserCreate) -> UserResponse:
    
    return UserResponse(1, user_create.username, user_create.email)