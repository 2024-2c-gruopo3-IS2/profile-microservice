from fastapi import FastAPI
from controllers.controller import router
from configs.db import Base, engine
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app.include_router(router, prefix="/profiles", tags=["profiles"])

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Profile Microservice Running!"}
