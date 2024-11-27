import logging
from fastapi import Header
import requests
from sqlalchemy.orm import Session

from repositories.repository import ProfileRepository
from schemas.schema import ProfileCreate

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ProfileService:

    def __init__(self, auth_service_url: str):
        self.auth_service_url = auth_service_url

    def create_profile(self, db: Session, profile_data: ProfileCreate, email: str):
        logger.info(f"Creating profile with data {profile_data.model_dump()}")
        existing_profile = ProfileRepository.get_by_email(db, email)
        if existing_profile:
            logger.error(f"Profile for email {email} already exists.")
            raise Exception(f"Profile for email {email} already exists.")
        logger.info(f"Creating profile for email {email}")
        return ProfileRepository.create_profile(db, profile_data, email)
    
    def get_profile(self, db: Session, email: str):
        logger.info(f"Getting profile")
        profile = ProfileRepository.get_by_email(db, email)
        profile = profile.__dict__
        profile["interests"] = profile.get("interests", "").split(",")
        if not profile:
            logger.error(f"Profile for email {email} not found.")
            raise Exception(f"Profile for email {email} not found.")
        logger.info(f"Profile for email {email} retrieved")
        return profile
    
    def update_profile(self, db: Session, profile_data: ProfileCreate, email: str):
        logger.info(f"Updating profile with data {profile_data.model_dump()}")
        profile = ProfileRepository.get_by_email(db, email)
        if not profile:
            logger.error(f"Profile for email {email} not found.")
            raise Exception(f"Profile for email {email} not found.")
        logger.info(f"Updating profile for email {email}")
        return ProfileRepository.update_profile(db, profile, profile_data)
    
    def delete_profile(self, db: Session, email: str):
        logger.info(f"Deleting profile")
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

    def get_profile_by_email(self, db: Session, email: str):
        logger.info(f"Getting profiles by email {email}")
        profile =  ProfileRepository.get_by_email(db, email)

        if not profile:
            logger.error(f"Profile for email {email} not found.")
            raise Exception(f"Profile for email {email} not found.")
        
        profile = profile.__dict__
        profile["interests"] = profile.get("interests", "").split(",")
        logger.info(f"Profile for email {email} retrieved")
        return profile
    
    def follow_user(self, db: Session, follower_email: str, followed: str):
        logger.info(f"Following user {followed}")

        followed_profile = ProfileRepository.get_profile_by_username(db, followed)

        if not followed_profile:
            logger.error(f"Profile for username {followed} not found.")

            raise Exception(f"User with username {followed} not found.")
        
        follower_username = ProfileRepository.get_by_email(db, follower_email).username

        if follower_username == followed:
            logger.error(f"Cannot follow yourself.")
            raise Exception(f"Cannot follow yourself.")
        
        all_followed = ProfileRepository.get_all_followed(db, follower_username)

        if followed in all_followed:
            logger.error(f"User with username {followed} is already followed by user with username {follower_username}")
            raise Exception(f"User with username {followed} is already followed by user with username {follower_username}")


        return ProfileRepository.follow_user(db, follower_username, followed)
    
    def unfollow_user(self, db: Session, follower_email: str, followed: str):
        logger.info(f"Unfollowing user {followed}")

        followed_profile = ProfileRepository.get_profile_by_username(db, followed)

        if not followed_profile:
            logger.error(f"Profile for username {followed} not found.")
            raise Exception(f"User with username {followed} not found.")
        
        follower_username = ProfileRepository.get_by_email(db, follower_email).username
        
        all_followed = ProfileRepository.get_all_followed(db, follower_username)

        if followed not in all_followed:
            logger.error(f"User with username {followed} is not followed by user with username {follower_username}")
            raise Exception(f"User with username {followed} is not followed by user with username {follower_username}")

        return ProfileRepository.unfollow_user(db, follower_username, followed)
    
    def get_followed(self, db: Session, username: str, user_email: str):
        logger.info(f"Getting followed")

        token_username = ProfileRepository.get_by_email(db, user_email).username

        if token_username == username:
            return ProfileRepository.get_all_followed(db, username)
        else:
            username_followed = ProfileRepository.get_all_followed(db, username)
            token_username_followed = ProfileRepository.get_all_followed(db, token_username)

            if token_username in username_followed and username in token_username_followed:
                return username_followed
            else:
                raise Exception(f"User {token_username} is not authorized to view followed of user {username}")
    
    def get_followers(self, db: Session, username: str, user_email: str):
        logger.info(f"Getting followers")

        token_username = ProfileRepository.get_by_email(db, user_email).username

        if token_username == username:
            return ProfileRepository.get_all_followers(db, username)
        else:
            username_followers = ProfileRepository.get_all_followers(db, username)
            token_username_followers = ProfileRepository.get_all_followers(db, token_username)

            if token_username in username_followers and username in token_username_followers:
                return username_followers
            else:
                raise Exception(f"User {token_username} is not authorized to view followers of user {username}")
            
    def get_followers_with_time(self, db: Session, username: str, user_email: str):
        logger.info(f"Getting followers with timestamp")

        token_username = ProfileRepository.get_by_email(db, user_email).username

        if token_username == username:
            return ProfileRepository.get_all_followers_with_timestamp(db, username)
        else:
            username_followers = ProfileRepository.get_all_followers_with_timestamp(db, username)
            token_username_followers = ProfileRepository.get_all_followers_with_timestamp(db, token_username)

            if token_username in username_followers and username in token_username_followers:
                return username_followers
            else:
                raise Exception(f"User {token_username} is not authorized to view followers of user {username}")
    
    def verify_user(self, db, username):
        logger.info(f"Verifying user {username}")
        return ProfileRepository.verify_user(db, username)
    
    def unverify_user(self, db, username):
        logger.info(f"Unverifying user {username}")
        return ProfileRepository.unverify_user(db, username)
    
    def get_all_users(self, db):
        logger.info(f"Getting all users")
        return ProfileRepository.get_all_users(db)
    
    def get_verified_users(self, db):
        logger.info(f"Getting verified users")
        return ProfileRepository.get_verified_users(db)

    
