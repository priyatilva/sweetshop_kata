from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from auth import router as auth_router
from sweets import router as sweets_router

models.Base.metadata.create_all(bind=engine)

# 1? Create FastAPI app instance first
app = FastAPI()

# 2? Add middleware AFTER app is defined
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3? Include routers
app.include_router(auth_router)
app.include_router(sweets_router)

@app.get("/")
def root():
    return {"message": "Sweet Shop API running!"}
