from core.schemas import BaseModel
from uuid import UUID
from pydantic import EmailStr




class AuthNotifyForm(BaseModel):
    operation_id : UUID
    email : EmailStr
    