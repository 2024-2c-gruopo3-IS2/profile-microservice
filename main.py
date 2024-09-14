from fastapi import FastAPI
from .config import Settings
from .controllers.controller import router
import logging

app = FastAPI()

settings = Settings()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Profile Microservice Running!"}
