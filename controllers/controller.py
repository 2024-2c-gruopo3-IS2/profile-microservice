from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from db import get_db
from schemas.schema import ProfileCreate, ProfileResponse
from services.service import ProfileService
from config import Settings
from main import logger

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/", response_model=ProfileResponse)
def create_profile(profile_data: ProfileCreate, token: str = Header(None), db: Session = Depends(get_db)):
    """
    Create a profile.
    """
    logger.info(f"Creating profile with data {profile_data.dict()}")
    service = ProfileService(auth_service_url=Settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Creating profile with data {profile_data.dict()}")
        user_profile = service.create_profile(db, profile_data, token)
        logger.info(f"Profile created successfully")
        return {"message": "Profile created successfully", "profile": user_profile}
    except Exception as e:
        logger.error(f"Error creating profile: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
