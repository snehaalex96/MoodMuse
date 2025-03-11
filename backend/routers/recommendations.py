from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import numpy as np
import io

from database.db import get_db, get_song_by_id
from models.recommender import Recommender
from models.image_model import ImageModel
from config import settings

router = APIRouter()

@router.get("/song/{song_id}")
def get_recommendations_by_song(
    song_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """
    Get recommendations based on a seed song
    """
    # Check if song exists
    song = get_song_by_id(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Initialize recommender
    recommender = Recommender(db)
    
    # Get recommendations
    recommendations = recommender.get_content_based_recommendations(song_id, limit)
    
    return {
        "seed_song": {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "album": song.album
        },
        "recommendations": recommendations
    }

@router.get("/mood/{mood}")
def get_recommendations_by_mood(
    mood: str,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """
    Get recommendations based on mood
    """
    # Validate mood
    valid_moods = ["happy", "sad", "energetic", "calm", "romantic", "melancholic"]
    if mood.lower() not in valid_moods:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid mood. Valid options are: {', '.join(valid_moods)}"
        )
    
    # Initialize recommender
    recommender = Recommender(db)
    
    # Get recommendations
    recommendations = recommender.get_mood_based_recommendations(mood, limit)
    
    return {
        "mood": mood,
        "recommendations": recommendations
    }

@router.post("/image")
async def get_recommendations_by_image(
    file: UploadFile = File(...),
    limit: int = Form(5),
    db: Session = Depends(get_db)
):
    """
    Get recommendations based on an uploaded image
    """
    # Check file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )
    
    try:
        # Read image file
        contents = await file.read()
        
        # Initialize image model
        image_model = ImageModel()
        
        # Extract features
        image_features = image_model.feature_extractor.extract_features_from_bytes(contents)
        
        # Initialize recommender
        recommender = Recommender(db)
        
        # Get recommendations
        recommendations = recommender.get_image_based_recommendations(image_features, limit)
        
        # Get image analysis
        image_analysis = image_model.analyze_mood(image_features)
        
        return {
            "image_analysis": image_analysis,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

@router.get("/user/{user_id}")
def get_recommendations_for_user(
    user_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """
    Get personalized recommendations for a user
    """
    # Initialize recommender
    recommender = Recommender(db)
    
    # Get recommendations
    recommendations = recommender.get_personalized_recommendations(user_id, limit)
    
    return {
        "user_id": user_id,
        "recommendations": recommendations
    }

@router.get("/popular")
def get_popular_songs(
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """
    Get popular songs
    """
    # Initialize recommender
    recommender = Recommender(db)
    
    # Get popular songs
    popular_songs = recommender.get_popular_songs(limit)
    
    return {
        "popular_songs": popular_songs
    }

@router.post("/feedback")
def submit_recommendation_feedback(
    song_id: int,
    user_id: int,
    liked: bool,
    db: Session = Depends(get_db)
):
    """
    Submit feedback on a recommendation
    """
    # In a real application, you would store this feedback
    # and use it to improve recommendations
    
    return {
        "status": "success",
        "message": "Feedback received"
    }