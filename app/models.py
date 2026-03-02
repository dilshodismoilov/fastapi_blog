from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

    id: int = Field(primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    hashed_password: str