from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from configs.db import get_db
from schemas.schema import ProfileCreate, ProfileResponse
from services.service import ProfileService
from configs.env import settings
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/")
def create_profile( token: str, profile_data: ProfileCreate, db: Session = Depends(get_db)):
    """
    Create a profile.
    """
    logger.info(f"Creating profile with data {profile_data.dict()}")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Creating profile with data {profile_data.dict()}")
        service.create_profile(db, profile_data, token)
        logger.info(f"Profile created successfully")
        return {"message": "Profile created successfully"}
                
    except Exception as e:
        logger.error(f"Error creating profile: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=ProfileResponse)
def get_profile(token: str, db: Session = Depends(get_db)):
    """
    Get a profile.
    """
    logger.info(f"Getting profile")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Getting profile")
        profile = service.get_profile(db, token)
        logger.info(f"Profile retrieved successfully")
        return ProfileResponse(**profile)
                
    except Exception as e:
        logger.error(f"Error getting profile: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/")
def update_profile(token: str, profile_data: ProfileCreate, db: Session = Depends(get_db)):
    """
    Update a profile.
    """
    logger.info(f"Updating profile with data {profile_data.dict()}")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Updating profile with data {profile_data.dict()}")
        service.update_profile(db, profile_data, token)
        logger.info(f"Profile updated successfully")
        return {"message": "Profile updated successfully"}
                
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/")
def delete_profile(token: str, db: Session = Depends(get_db)):
    """
    Delete a profile.
    """
    logger.info(f"Deleting profile")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Deleting profile")
        service.delete_profile(db, token)
        logger.info(f"Profile deleted successfully")
        return {"message": "Profile deleted successfully"}
                
    except Exception as e:
        logger.error(f"Error deleting profile: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/all-usernames")
def get_all_usernames(db: Session = Depends(get_db)):
    """
    Get all usernames.
    """
    logger.info(f"Getting all usernames")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Getting all usernames")
        usernames = service.get_all_usernames(db)
        logger.info(f"Usernames retrieved successfully")
        return usernames
                
    except Exception as e:
        logger.error(f"Error getting all usernames: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/by-username", response_model=ProfileResponse)
def get_profile_by_username(username: str, db: Session = Depends(get_db)):
    """
    Get a profile by username.
    """
    logger.info(f"Getting profile by username {username}")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Getting profile by username {username}")
        profile = service.get_profile_by_username(db, username)
        logger.info(f"Profile retrieved successfully")

        print("profile", profile)

        return ProfileResponse(**profile)
                
    except Exception as e:
        logger.error(f"Error getting profile by username: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


