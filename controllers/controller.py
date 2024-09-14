from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from db import get_db
from schemas.schema import ProfileCreate, ProfileResponse
from services.service import ProfileService
from config import Settings

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/", response_model=ProfileResponse)
def create_profile(profile_data: ProfileCreate, token: str = Header(None), db: Session = Depends(get_db)):
    service = ProfileService(auth_service_url=Settings.AUTH_SERVICE_URL)
    try:
        user_profile = service.create_profile(db, profile_data, token)
        return {"message": "Profile created successfully", "profile": user_profile}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
