from sqlalchemy.orm import Session

from models.model import Profile
from schemas.schema import ProfileCreate

class ProfileRepository:

    @staticmethod
    def get_by_email(db: Session, email: str):
        """
        Get a profile by email.
        """
        return db.query(Profile).filter(Profile.email == email).first()

    @staticmethod
    def create_profile(db: Session, profile_data: ProfileCreate, email: str):
        """
        Create a profile in the database.
        """
        db_profile = Profile(**profile_data.dict(), email=email)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile
    
    @staticmethod
    def update_profile(db: Session, profile: Profile, profile_data: ProfileCreate):
        """
        Update a profile in the database.
        """
        for key, value in profile_data.dict().items():
            setattr(profile, key, value)
        db.commit()
        db.refresh(profile)
        return profile
    
    @staticmethod
    def delete_profile(db: Session, profile: Profile):
        """
        Delete a profile from the database.
        """
        db.delete(profile)
        db.commit()
        return profile
    
    @staticmethod
    def search_users_by_name(db: Session, first_name: str, offset: int = 0, amount: int = 5):
        """
        Search for users by their first_name. 
        First look for users whose first_name starts with the given prefix,
        then look for users whose first_name contains the given prefix if needed.
        """
        
        starts_with_query = db.query(Profile).filter(Profile.first_name.ilike(f"{first_name}%")).offset(offset).limit(amount).all()

        if len(starts_with_query) < amount:
            
            remaining = amount - len(starts_with_query)

    
            contains_query = (
                db.query(Profile)
                .filter(Profile.first_name.ilike(f"%{first_name}%"))
                .offset(offset)
                .limit(remaining)
                .all()
            )

            return starts_with_query + contains_query

        return starts_with_query
