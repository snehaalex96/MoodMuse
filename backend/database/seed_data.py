import json
import os
import numpy as np
from sqlalchemy.orm import Session
from pathlib import Path

from database.db import Song, User, serialize_features, engine, SessionLocal
from config import settings
from passlib.context import CryptContext

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)

def seed_database():
    """Seed the database with initial data"""
    db = SessionLocal()
    
    # Seed sample users if they don't exist
    if db.query(User).count() == 0:
        seed_users(db)
        print("Users seeded successfully")
    
    # Seed sample songs if they don't exist
    if db.query(Song).count() == 0:
        seed_songs(db)
        print("Songs seeded successfully")
    
    db.close()

def seed_users(db: Session):
    """Seed sample users"""
    sample_users = [
        {
            "username": "user1",
            "email": "user1@example.com",
            "password": "password123"
            "title": "Imagine",
            "artist": "John Lennon",
            "album": "Imagine",
            "genre": "Rock",
            "year": 1971,
            "duration": 183.0,
            "path": "../data/audio_samples/imagine.mp3",
            "image_path": "../data/images/imagine.jpg",
            "lyrics": "Imagine there's no heaven, it's easy if you try, no hell below us, above us only sky..."
        },
        {
            "title": "Shake It Off",
            "artist": "Taylor Swift",
            "album": "1989",
            "genre": "Pop",
            "year": 2014,
            "duration": 219.0,
            "path": "../data/audio_samples/shake_it_off.mp3",
            "image_path": "../data/images/1989.jpg",
            "lyrics": "I stay out too late, got nothing in my brain, that's what people say, mmm-mmm, that's what people say, mmm-mmm..."
        },
        {
            "title": "Uptown Funk",
            "artist": "Mark Ronson ft. Bruno Mars",
            "album": "Uptown Special",
            "genre": "Funk",
            "year": 2014,
            "duration": 270.0,
            "path": "../data/audio_samples/uptown_funk.mp3",
            "image_path": "../data/images/uptown_special.jpg",
            "lyrics": "This hit, that ice cold, Michelle Pfeiffer, that white gold, this one for them hood girls, them good girls straight masterpieces..."
        }
    ]

if __name__ == "__main__":
    seed_database()
            "username": "user2",
            "email": "user2@example.com",
            "password": "password123"
        },
        {
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123"
        }
    ]
    
    for user_data in sample_users:
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hash_password(user_data["password"])
        )
        db.add(user)
    
    db.commit()

def seed_songs(db: Session):
    """Seed sample songs with metadata and random feature vectors"""
    # Check if metadata file exists
    metadata_file = Path(settings.METADATA_DIR) / "songs.json"
    
    if not metadata_file.exists():
        print(f"Metadata file not found: {metadata_file}")
        # Create sample metadata if file doesn't exist
        sample_songs = generate_sample_songs()
    else:
        # Load songs from metadata file
        with open(metadata_file, "r") as f:
            sample_songs = json.load(f)
    
    # Add songs to database
    for song_data in sample_songs:
        # Generate random feature vectors for demonstration
        audio_features = np.random.rand(settings.AUDIO_FEATURE_DIMENSIONS).astype(np.float32)
        image_features = np.random.rand(settings.IMAGE_FEATURE_DIMENSIONS).astype(np.float32)
        text_features = np.random.rand(settings.TEXT_FEATURE_DIMENSIONS).astype(np.float32)
        
        song = Song(
            title=song_data["title"],
            artist=song_data["artist"],
            album=song_data["album"],
            genre=song_data["genre"],
            year=song_data["year"],
            duration=song_data["duration"],
            path=song_data.get("path", ""),
            image_path=song_data.get("image_path", ""),
            lyrics=song_data.get("lyrics", ""),
            audio_features=serialize_features(audio_features),
            image_features=serialize_features(image_features),
            text_features=serialize_features(text_features)
        )
        db.add(song)
    
    db.commit()

def generate_sample_songs():
    """Generate sample song data if metadata file doesn't exist"""
    return [
        {
            "title": "Bohemian Rhapsody",
            "artist": "Queen",
            "album": "A Night at the Opera",
            "genre": "Rock",
            "year": 1975,
            "duration": 354.0,
            "path": "../data/audio_samples/bohemian_rhapsody.mp3",
            "image_path": "../data/images/a_night_at_the_opera.jpg",
            "lyrics": "Is this the real life? Is this just fantasy? Caught in a landslide, no escape from reality..."
        },
        {
            "title": "Billie Jean",
            "artist": "Michael Jackson",
            "album": "Thriller",
            "genre": "Pop",
            "year": 1982,
            "duration": 294.0,
            "path": "../data/audio_samples/billie_jean.mp3",
            "image_path": "../data/images/thriller.jpg",
            "lyrics": "She was more like a beauty queen from a movie scene, I said don't mind, but what do you mean..."
        },
        {