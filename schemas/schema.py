from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ProfileCreate(BaseModel):
    name: str
    username: str
    surname: str
    location: Optional[str]
    description: Optional[str]
    date_of_birth: Optional[date]
    interests: Optional[List[str]]
class ProfileUpdate(ProfileCreate):
    pass

class ProfileResponse(ProfileCreate):
    email: str
    
    class Config:
        orm_mode = True
