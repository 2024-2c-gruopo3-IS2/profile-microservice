import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    AUTH_SERVICE_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    def __init__(self):
        self.AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_NAME")

settings = Settings()