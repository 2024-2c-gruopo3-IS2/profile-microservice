from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProfileCreate(BaseModel):
    name: str
    surname: str
    location: Optional[str]
    description: Optional[str]
    date_of_birth: Optional[date]
class ProfileUpdate(ProfileCreate):
    pass

class ProfileResponse(ProfileCreate):
    email: str
    
    class Config:
        orm_mode = True
