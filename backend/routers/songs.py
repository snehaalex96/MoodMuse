from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import numpy as np
import json
import shutil
import os
from pathlib import Path

from database.db import get_db, Song, get_song_by_id, serialize_features
from models.audio_model import AudioModel
from models.image_model import ImageModel
from models.text_model import TextModel
from utils.preprocessor import FileManager
from config import settings

router = APIRouter()

@router.get("/")
def get_all_songs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all songs
    """
    songs = db.query(Song).offset(skip).limit(limit).all()
    
    # Convert to list of dictionaries
    result = []
    for song in songs:
        result.append({
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "album": song.album,
            "genre": song.genre,
            "year": song.year,
            "duration": song.duration
        })
    
    return result

@router.get("/{song_id}")
def get_song(
    song_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific song by ID
    """
    song = get_song_by_id(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "album": song.album,
        "genre": song.genre,
        "year": song.year,
        "duration": song.duration,
        "path": song.path,
        "image_path": song.image_path,
        "lyrics": song.lyrics
    }

@router.get("/artist/{artist}")
def get_songs_by_artist(
    artist: str,
    db: Session = Depends(get_db)
):
    """
    Get all songs by a specific artist
    """
    songs = db.query(Song).filter(Song.artist == artist).all()
    
    # Convert to list of dictionaries
    result = []
    for song in songs:
        result.append({
            "id": song.id,
            "title": song.title,
            "album": song.album,
            "genre": song.genre,
            "year": song.year,
            "duration": song.duration
        })
    
    return result

@router.post("/")
async def add_song(
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(...),
    genre: str = Form(...),
    year: int = Form(...),
    duration: float = Form(...),
    lyrics: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None),
    image_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Add a new song to the database
    """
    # Initialize file manager
    file_manager = FileManager()
    
    # Handle audio file
    audio_path = ""
    if audio_file:
        # Read file content
        audio_content = await audio_file.read()
        
        # Save file
        audio_path = file_manager.save_uploaded_file(
            audio_content,
            audio_file.filename,
            'audio'
        )
    
    # Handle image file
    image_path = ""
    if image_file:
        # Read file content
        image_content = await image_file.read()
        
        # Save file
        image_path = file_manager.save_uploaded_file(
            image_content,
            image_file.filename,
            'image'
        )
    
    # Initialize models
    audio_model = AudioModel()
    image_model = ImageModel()
    text_model = TextModel()
    
    # Extract features
    audio_features = np.zeros(settings.AUDIO_FEATURE_DIMENSIONS, dtype=np.float32)
    if audio_path:
        audio_features = audio_model.extract_features(audio_path)
    
    image_features = np.zeros(settings.IMAGE_FEATURE_DIMENSIONS, dtype=np.float32)
    if image_path:
        image_features = image_model.extract_features(image_path)
    
    text_features = np.zeros(settings.TEXT_FEATURE_DIMENSIONS, dtype=np.float32)
    if lyrics:
        text_features = text_model.extract_features(lyrics)
    
    # Create new song
    song = Song(
        title=title,
        artist=artist,
        album=album,
        genre=genre,
        year=year,
        duration=duration,
        path=audio_path,
        image_path=image_path,
        lyrics=lyrics,
        audio_features=serialize_features(audio_features),
        image_features=serialize_features(image_features),
        text_features=serialize_features(text_features)
    )
    
    # Add to database
    db.add(song)
    db.commit()
    db.refresh(song)
    
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "message": "Song added successfully"
    }

@router.put("/{song_id}")
async def update_song(
    song_id: int,
    title: Optional[str] = Form(None),
    artist: Optional[str] = Form(None),
    album: Optional[str] = Form(None),
    genre: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    duration: Optional[float] = Form(None),
    lyrics: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None),
    image_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Update an existing song
    """
    # Get song
    song = get_song_by_id(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Initialize file manager
    file_manager = FileManager()
    
    # Initialize models
    audio_model = AudioModel()
    image_model = ImageModel()
    text_model = TextModel()
    
    # Update song attributes
    if title:
        song.title = title
    if artist:
        song.artist = artist
    if album:
        song.album = album
    if genre:
        song.genre = genre
    if year:
        song.year = year
    if duration:
        song.duration = duration
    
    # Update lyrics and text features
    if lyrics:
        song.lyrics = lyrics
        text_features = text_model.extract_features(lyrics)
        song.text_features = serialize_features(text_features)
    
    # Handle audio file
    if audio_file:
        # Read file content
        audio_content = await audio_file.read()
        
        # Save file
        audio_path = file_manager.save_uploaded_file(
            audio_content,
            audio_file.filename,
            'audio'
        )
        
        # Update song path
        song.path = audio_path
        
        # Extract features
        audio_features = audio_model.extract_features(audio_path)
        song.audio_features = serialize_features(audio_features)
    
    # Handle image file
    if image_file:
        # Read file content
        image_content = await image_file.read()
        
        # Save file
        image_path = file_manager.save_uploaded_file(
            image_content,
            image_file.filename,
            'image'
        )
        
        # Update song path
        song.image_path = image_path
        
        # Extract features
        image_features = image_model.extract_features(image_path)
        song.image_features = serialize_features(image_features)
    
    # Commit changes
    db.commit()
    db.refresh(song)
    
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "message": "Song updated successfully"
    }

@router.delete("/{song_id}")
def delete_song(
    song_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a song
    """
    # Get song
    song = get_song_by_id(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Delete song from database
    db.delete(song)
    db.commit()
    
    return {
        "message": f"Song '{song.title}' deleted successfully"
    }

@router.get("/{song_id}/features")
def get_song_features(
    song_id: int,
    db: Session = Depends(get_db)
):
    """
    Get feature vectors for a song
    """
    # Get song
    song = get_song_by_id(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Use audio features to analyze mood and genre
    audio_model = AudioModel()
    
    # Deserialize features
    audio_features = np.frombuffer(song.audio_features, dtype=np.float32)
    audio_features = audio_features.reshape((settings.AUDIO_FEATURE_DIMENSIONS,))
    
    # Analyze audio
    mood = audio_model.analyze_mood(audio_features)
    genre = audio_model.analyze_genre(audio_features)
    
    # Use text features to analyze sentiment and themes
    text_model = TextModel()
    
    # Analyze lyrics
    sentiment = {}
    themes = []
    if song.lyrics:
        sentiment = text_model.analyze_sentiment(song.lyrics)
        themes = text_model.extract_themes(song.lyrics)
    
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "analysis": {
            "mood": mood,
            "genre": genre,
            "sentiment": sentiment,
            "themes": themes
        }
    }

@router.post("/batch")
async def add_songs_batch(
    songs: List[Dict] = Body(...),
    db: Session = Depends(get_db)
):
    """
    Add multiple songs in a batch
    """
    added_songs = []
    
    for song_data in songs:
        try:
            # Create random feature vectors for demonstration
            audio_features = np.random.rand(settings.AUDIO_FEATURE_DIMENSIONS).astype(np.float32)
            image_features = np.random.rand(settings.IMAGE_FEATURE_DIMENSIONS).astype(np.float32)
            text_features = np.random.rand(settings.TEXT_FEATURE_DIMENSIONS).astype(np.float32)
            
            # Create song
            song = Song(
                title=song_data.get("title", "Unknown"),
                artist=song_data.get("artist", "Unknown"),
                album=song_data.get("album", "Unknown"),
                genre=song_data.get("genre", "Unknown"),
                year=song_data.get("year", 2000),
                duration=song_data.get("duration", 0.0),
                path=song_data.get("path", ""),
                image_path=song_data.get("image_path", ""),
                lyrics=song_data.get("lyrics", ""),
                audio_features=serialize_features(audio_features),
                image_features=serialize_features(image_features),
                text_features=serialize_features(text_features)
            )
            
            # Add to database
            db.add(song)
            db.commit()
            db.refresh(song)
            
            added_songs.append({
                "id": song.id,
                "title": song.title,
                "artist": song.artist
            })
            
        except Exception as e:
            # Log error and continue with next song
            print(f"Error adding song: {e}")
    
    return {
        "message": f"Added {len(added_songs)} songs",
        "songs": added_songs
    }