from sqlalchemy import text
from sqlalchemy.orm import Session
import logging
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
    def search_users_by_name(db: Session, first_name: str, offset: int = 0, amount: int = 5):
        """
        Search for users by their first_name. 
        First look for users whose first_name starts with the given prefix,
        then look for users whose first_name contains the given prefix if needed.
        """
        logger.info(f"Searching for users with first name {first_name}")
        starts_with_query = db.query(Profile).filter(Profile.name.ilike(f"{first_name}%")).offset(offset).limit(amount).all()

        if len(starts_with_query) < amount:
            
            remaining = amount - len(starts_with_query)

    
            contains_query = (
                db.query(Profile)
                .filter(Profile.name.ilike(f"%{first_name}%"))
                .offset(offset)
                .limit(remaining)
                .all()
            )

            return starts_with_query + contains_query
        
        logger.info(f"Found {len(starts_with_query)} users with first name {first_name}")

        return starts_with_query
    
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
        query = text("INSERT INTO follows (follower, followed) VALUES (:follower, :followed)")
        db.execute(query, {"follower": follower, "followed": followed})
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