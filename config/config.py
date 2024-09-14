from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "admin"
    DB_PASSWORD: str = "admin123"
    DB_NAME: str = "profile_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    AUTH_SERVICE_URL: str = "http://auth-service-url"
    
    class Config:
        env_file = ".env"
