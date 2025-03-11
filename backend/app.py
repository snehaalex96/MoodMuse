import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional

# Local imports
from database.db import get_db, init_db
from routers import recommendations, songs, users
from config import settings

# Create FastAPI app
app = FastAPI(
    title="Multimodal Music Recommender API",
    description="API for a music recommendation system that uses audio, visual, and text features",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(songs.router, prefix="/api/songs", tags=["songs"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Multimodal Music Recommender API"}

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Startup event
@app.on_event("startup")
async def startup_event():
    # Initialize database
    init_db()
    print("Database initialized")

if __name__ == "__main__":
    # Run the API with uvicorn
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )