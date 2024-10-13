from fastapi import FastAPI
from controllers.controller import router
from configs.db import Base, engine
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app.include_router(router, prefix="/profiles", tags=["profiles"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Profile Microservice Running!"}
