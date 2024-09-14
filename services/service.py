from fastapi import HTTPException
import requests
from sqlalchemy.orm import Session

from repositories.repository import ProfileRepository
from schemas.schema import ProfileCreate

class ProfileService:

    def __init__(self, auth_service_url: str):
        self.auth_service_url = auth_service_url

    def get_user_email_from_token(self, token: str) -> str:
        response = requests.get(f"{self.auth_service_url}/get-email", headers={"Authorization": token})
        if response.status_code == 200:
            return response.json().get("email")
        raise HTTPException(status_code=401, detail="Invalid token")

    def create_profile(self, db: Session, profile_data: ProfileCreate, token: str):
        email = self.get_user_email_from_token(token)
        existing_profile = ProfileRepository.get_by_email(db, email)
        if existing_profile:
            raise Exception(f"Profile for email {email} already exists.")
        return ProfileRepository.create_profile(db, profile_data, email)
