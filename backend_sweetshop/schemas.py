from pydantic import BaseModel

# User schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: int = 0

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        orm_mode = True

# Sweet schemas
class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int

class SweetResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    quantity: int
    class Config:
        orm_mode = True
