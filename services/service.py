import logging
from fastapi import HTTPException
import requests
from sqlalchemy.orm import Session

from repositories.repository import ProfileRepository
from schemas.schema import ProfileCreate

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ProfileService:

    def __init__(self, auth_service_url: str):
        self.auth_service_url = auth_service_url

    def get_user_email_from_token(self, token: str) -> str:
        logger.info(f"Getting user email from token {token}")
        response = requests.get(
            self.auth_service_url + "/auth/get-email-from-token",
            headers={"Content-Type": "application/json"},
            json={"token": token}
        )
        if response.status_code == 200:
            logger.info(f"User email: {response.json().get('email')}")
            return response.json().get("email")
        raise HTTPException(status_code=401, detail="Invalid token")

    def create_profile(self, db: Session, profile_data: ProfileCreate, token: str):
        logger.info(f"Creating profile with data {profile_data.dict()}")
        email = self.get_user_email_from_token(token)
        existing_profile = ProfileRepository.get_by_email(db, email)
        if existing_profile:
            logger.error(f"Profile for email {email} already exists.")
            raise Exception(f"Profile for email {email} already exists.")
        logger.info(f"Creating profile for email {email}")
        return ProfileRepository.create_profile(db, profile_data, email)
    
    def get_profile(self, db: Session, token: str):
        logger.info(f"Getting profile")
        email = self.get_user_email_from_token(token)
        profile = ProfileRepository.get_by_email(db, email)
        profile = profile.__dict__
        profile["interests"] = profile.get("interests", "").split(",")
        if not profile:
            logger.error(f"Profile for email {email} not found.")
            raise Exception(f"Profile for email {email} not found.")
        logger.info(f"Profile for email {email} retrieved")
        return profile
    
    def update_profile(self, db: Session, profile_data: ProfileCreate, token: str):
        logger.info(f"Updating profile with data {profile_data.dict()}")
        email = self.get_user_email_from_token(token)
        profile = ProfileRepository.get_by_email(db, email)
        if not profile:
            logger.error(f"Profile for email {email} not found.")
            raise Exception(f"Profile for email {email} not found.")
        logger.info(f"Updating profile for email {email}")
        return ProfileRepository.update_profile(db, profile, profile_data)
    
    def delete_profile(self, db: Session, token: str):
        logger.info(f"Deleting profile")
        email = self.get_user_email_from_token(token)
        profile = ProfileRepository.get_by_email(db, email)
        if not profile:
            logger.error(f"Profile for email {email} not found.")
            raise Exception(f"Profile for email {email} not found.")
        logger.info(f"Deleting profile for email {email}")
        return ProfileRepository.delete_profile(db, profile)
    
    def get_all_usernames(self, db: Session):
        logger.info(f"Getting all usernames")
        return ProfileRepository.get_all_usernames(db)
    
    def get_profile_by_username(self, db: Session, username: str):
        logger.info(f"Getting profiles by username {username}")
        profile =  ProfileRepository.get_profile_by_username(db, username)

        if not profile:
            logger.error(f"Profile for username {username} not found.")
            raise Exception(f"Profile for username {username} not found.")
        
        profile = profile.__dict__
        profile["interests"] = profile.get("interests", "").split(",")
        logger.info(f"Profile for username {username} retrieved")
        return profile
