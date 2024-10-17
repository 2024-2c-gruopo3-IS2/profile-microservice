from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datadog import statsd

from configs.db import get_db
from schemas.schema import ProfileCreate, ProfileResponse
from services.service import ProfileService
from configs.env import settings
import logging
from controllers.authentication import get_user_from_token

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/")
def create_profile(profile_data: ProfileCreate, user_email: callable = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Create a profile.
    """
    statsd.increment('profile.create_profile')
    logger.info(f"Creating profile with data {profile_data.model_dump()}")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Creating profile with data {profile_data.model_dump()}")
        service.create_profile(db, profile_data, user_email)
        logger.info(f"Profile created successfully")
        return {"message": "Profile created successfully"}
                
    except Exception as e:
        logger.error(f"Error creating profile: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=ProfileResponse)
def get_profile(user_email: callable = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Get a profile.
    """
    logger.info(f"Getting profile")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Getting profile")
        profile = service.get_profile(db, user_email)
        logger.info(f"Profile retrieved successfully")
        return ProfileResponse(**profile)
                
    except Exception as e:
        logger.error(f"Error getting profile: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/")
def update_profile(profile_data: ProfileCreate, user_email: callable = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Update a profile.
    """
    logger.info(f"Updating profile with data {profile_data.model_dump()}")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Updating profile with data {profile_data.model_dump()}")
        service.update_profile(db, profile_data, user_email)
        logger.info(f"Profile updated successfully")
        return {"message": "Profile updated successfully"}
                
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/")
def delete_profile(user_email: callable = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Delete a profile.
    """
    logger.info(f"Deleting profile")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Deleting profile")
        service.delete_profile(db, user_email)
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
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/by-email", response_model=ProfileResponse)
def get_profile_by_email(email: str, db: Session = Depends(get_db)):
    """
    Get a profile by email.
    """
    logger.info(f"Getting profile by email {email}")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Getting profile by email {email}")
        profile = service.get_profile_by_email(db, email)
        logger.info(f"Profile retrieved successfully")
        return ProfileResponse(**profile)
                
    except Exception as e:
        logger.error(f"Error getting profile by email: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/follow")
def follow_user(username: str, user_email: callable = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Follow a user.
    """
    logger.info(f"Following user {username}")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Following user {username}")
        service.follow_user(db, user_email, username)
        logger.info(f"User followed successfully")
        return {"message": "User followed successfully"}
                
    except Exception as e:
        logger.error(f"Error following user: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/unfollow")
def unfollow_user(username: str, user_email: callable = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Unfollow a user.
    """
    logger.info(f"Unfollowing user {username}")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Unfollowing user {username}")
        service.unfollow_user(db, user_email, username)
        logger.info(f"User unfollowed successfully")
        return {"message": "User unfollowed successfully"}
                
    except Exception as e:
        logger.error(f"Error unfollowing user: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/followers")
def get_followers(username: str, user_email: callable = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Get followers of a user.
    """
    logger.info(f"Getting followers for {username}")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Getting followers for {username}")
        followers = service.get_followers(db, username, user_email)
        logger.info(f"Followers retrieved successfully")
        return followers
                
    except Exception as e:
        logger.error(f"Error getting followers: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/followed")
def get_followed(username: str, user_email: callable = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Get users followed by a user.
    """
    logger.info(f"Getting followed")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Getting followed")
        followed = service.get_followed(db, username, user_email)
        logger.info(f"Followed retrieved successfully")
        return followed
                
    except Exception as e:
        logger.error(f"Error getting followed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/followed-emails")
def get_followed_emails(username: str, user_email: callable = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Get emails of users followed by a user.
    """
    logger.info(f"Getting followed emails")
    service = ProfileService(auth_service_url=settings.AUTH_SERVICE_URL)
    try:
        logger.info(f"Getting followed emails")
        followed_usernames = service.get_followed(db, username, user_email)
        logger.info(f"Followed emails retrieved successfully")
        followed_emails = []
        for followed_username in followed_usernames:
            followed_profile = service.get_profile_by_username(db, followed_username)
            followed_emails.append(followed_profile["email"])
        return followed_emails
                
    except Exception as e:
        logger.error(f"Error getting followed emails: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


