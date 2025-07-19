
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    uid: str
    name: str
    email: EmailStr
    created_at: datetime

class ProductCreate(BaseModel):
    amazon_url: str
    target_price: float

class Product(BaseModel):
    id: str
    user_id: str
    amazon_url: str
    product_name: str
    current_price: float
    target_price: float
    lowest_price: float
    image_url: str
    asin: str
    created_at: datetime
    is_active: bool = True

class ProductResponse(BaseModel):
    id: Optional[str] = None
    product_name: str
    current_price: float
    image_url: str
    asin: str
    amazon_url: str
    availability: str = "In Stock"

class PriceAlert(BaseModel):
    product_id: str
    user_email: str
    product_name: str
    current_price: float
    target_price: float
    lowest_price: float
    image_url: str
    amazon_url: str

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
