from sqlalchemy import text
from sqlalchemy.orm import Session
import logging
import datetime
from models.model import Follows, Profile
from schemas.schema import ProfileCreate

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ProfileRepository:

    @staticmethod
    def get_by_email(db: Session, email: str):
        """
        Get a profile by email.
        """
        logger.info(f"Getting profile with email {email}")
        return db.query(Profile).filter(Profile.email == email).first()

    @staticmethod
    def create_profile(db: Session, profile_data: ProfileCreate, email: str):
        """
        Create a profile in the database.
        """
        profile_data = profile_data.model_dump()
        profile_data["interests"] = ",".join(profile_data.get("interests", []))

        logger.info(f"Creating profile with data {profile_data}")
        db_profile = Profile(**profile_data, email=email)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        logger.info(f"Profile created with email {db_profile.email}")
        return db_profile
    
    @staticmethod
    def update_profile(db: Session, profile: Profile, profile_data: ProfileCreate):
        """
        Update a profile in the database.
        """
        logger.info(f"Updating profile with data {profile_data.model_dump()}")
        for key, value in profile_data.model_dump().items():
            if key == "interests":
                value = ",".join(value)
            setattr(profile, key, value)
        db.commit()
        db.refresh(profile)
        logger.info(f"Profile updated with email {profile.email}")
        return profile
    
    @staticmethod
    def delete_profile(db: Session, profile: Profile):
        """
        Delete a profile from the database.
        """
        logger.info(f"Deleting profile with email {profile.email}")
        db.delete(profile)
        db.commit()
        logger.info(f"Profile deleted with email {profile.email}")
        return profile
    
    @staticmethod
    def get_all_usernames(db: Session):
        """
        Get all usernames.
        """
        logger.info(f"Getting all usernames")
        return [username[0] for username in db.query(Profile.username).all()]
    
    @staticmethod
    def get_profile_by_username(db: Session, username: str):
        """
        Get a profile by username.
        """
        logger.info(f"Getting profile with username {username}")
        return db.query(Profile).filter(Profile.username == username).first()
    
    @staticmethod
    def follow_user(db: Session, follower: str, followed: str):
        """
        Follow a user.
        """
        logger.info(f"Following user {followed}")
        created_at = datetime.datetime.now()
        query = text("INSERT INTO follows (follower, followed, created_at) VALUES (:follower, :followed, :created_at)")
        db.execute(query, {"follower": follower, "followed": followed, "created_at": created_at})
        db.commit()
        logger.info(f"User {followed} followed successfully")

    @staticmethod
    def unfollow_user(db: Session, follower: str, followed: str):
        """
        Unfollow a user.
        """
        logger.info(f"Unfollowing user {followed}")
        query = text("DELETE FROM follows WHERE follower = :follower AND followed = :followed")
        db.execute(query, {"follower": follower, "followed": followed})
        db.commit()
        logger.info(f"User {followed} unfollowed successfully")
    
    @staticmethod
    def get_all_followed(db: Session, follower: str):
        """
        Get all users followed by a user.
        """
        logger.info(f"Getting all users followed by {follower}")
        return [followed[0] for followed in db.query(Follows.followed).filter(Follows.follower == follower).all()]
    
    @staticmethod
    def get_all_followers(db: Session, followed: str):
        """
        Get all users following a user.
        """
        logger.info(f"Getting all users following {followed}")
        return [follower[0] for follower in db.query(Follows.follower).filter(Follows.followed == followed).all()]
    
    @staticmethod
    def get_all_followers_with_timestamp(db: Session, followed: str):
        """
        Get all users following a user with timestamp.
        """
        logger.info(f"Getting all users following {followed} with timestamp")
        return [{"follower": follower[0], "created_at": follower[1]} for follower in db.query(Follows.follower, Follows.created_at).filter(Follows.followed == followed).all()]
    
    @staticmethod
    def verify_user(db:Session, username: str):
        """
        Verify a user.
        """
        logger.info(f"Verifying user {username}")
        query = text("UPDATE profiles SET is_verified = TRUE WHERE username = :username")
        db.execute(query, {"username": username})
        db.commit()
        logger.info(f"User {username} verified successfully")

    @staticmethod
    def unverify_user(db:Session, username: str):
        """
        Unverify a user.
        """
        logger.info(f"Unverifying user {username}")
        query = text("UPDATE profiles SET is_verified = FALSE WHERE username = :username")
        db.execute(query, {"username": username})
        db.commit()
        logger.info(f"User {username} unverified successfully")

    @staticmethod
    def get_all_users(db: Session):
        """
        Get all users.
        """
        logger.info(f"Getting all users")
        return [profile for profile in db.query(Profile).all()]