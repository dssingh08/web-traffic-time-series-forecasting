from pydantic import BaseModel, Field
from typing import Literal, Optional

from datetime import date

class PredictionRequest(BaseModel):
    model_name: Literal["arima", "arma", "auto_arima", "holt_add_seasonal", "holt_add", "simple_exp_smoothing", "cnn", "cnn_60"]
    days: int = Field(..., gt=0)

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
