from fastapi import HTTPException
import requests
from sqlalchemy.orm import Session

from repositories.repository import ProfileRepository
from schemas.schema import ProfileCreate
from main import logger

class ProfileService:

    def __init__(self, auth_service_url: str):
        self.auth_service_url = auth_service_url

    def get_user_email_from_token(self, token: str) -> str:
        logger.info(f"Getting user email from token {token}")
        response = requests.get(f"{self.auth_service_url}/auth/get-email", headers={"Authorization": token})
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
