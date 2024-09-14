from fastapi import FastAPI
from .config import Settings
from .controllers.controller import router

app = FastAPI()

settings = Settings()

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Profile Microservice Running!"}
