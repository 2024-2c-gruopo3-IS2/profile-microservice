from sqlalchemy import Column, String, Date, Text
from configs.db import Base

class Profile(Base):
    __tablename__ = 'profiles'

    email = Column(String, primary_key=True, index=True, unique=True)
    username = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String)
    surname = Column(String)
    location = Column(String)
    description = Column(Text)
    date_of_birth = Column(Date)
    interests = Column(Text)

class Follows(Base):
    __tablename__ = 'follows'

    follower = Column(String, primary_key=True, index=True)
    followed = Column(String, primary_key=True, index=True)

