from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, Boolean, Text, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

import numpy as np
import json
import os
from typing import List, Optional, Dict, Any

from config import settings

# Create SQLAlchemy engine and session
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define association tables
user_song_likes = Table(
    "user_song_likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("song_id", Integer, ForeignKey("songs.id"))
)

user_song_history = Table(
    "user_song_history",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("song_id", Integer, ForeignKey("songs.id")),
    Column("listen_count", Integer, default=1),
    Column("last_listened", String)
)

# Define SQLAlchemy ORM models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    liked_songs = relationship("Song", secondary=user_song_likes, back_populates="liked_by")
    listened_songs = relationship("Song", secondary=user_song_history, back_populates="listeners")

class Song(Base):
    __tablename__ = "songs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String, index=True)
    album = Column(String)
    genre = Column(String)
    year = Column(Integer)
    duration = Column(Float)  # in seconds
    path = Column(String)  # path to audio file
    image_path = Column(String)  # path to album artwork
    lyrics = Column(Text, nullable=True)
    
    # Feature vectors (stored as binary)
    audio_features = Column(LargeBinary, nullable=True)
    image_features = Column(LargeBinary, nullable=True)
    text_features = Column(LargeBinary, nullable=True)
    
    # Relationships
    liked_by = relationship("User", secondary=user_song_likes, back_populates="liked_songs")
    listeners = relationship("User", secondary=user_song_history, back_populates="listened_songs")

# Helper functions for database interactions
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)

# Feature vector helper functions
def serialize_features(features: np.ndarray) -> bytes:
    """Convert numpy array to binary format for database storage"""
    return features.tobytes()

def deserialize_features(binary_data: bytes, shape: tuple) -> np.ndarray:
    """Convert binary data back to numpy array"""
    return np.frombuffer(binary_data, dtype=np.float32).reshape(shape)

# Database utility functions
def get_songs(db: Session, skip: int = 0, limit: int = 100) -> List[Song]:
    """Get all songs from the database"""
    return db.query(Song).offset(skip).limit(limit).all()

def get_song_by_id(db: Session, song_id: int) -> Optional[Song]:
    """Get a song by its ID"""
    return db.query(Song).filter(Song.id == song_id).first()

def get_songs_by_artist(db: Session, artist: str) -> List[Song]:
    """Get all songs by a specific artist"""
    return db.query(Song).filter(Song.artist == artist).all()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get a user by username"""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    return db.query(User).filter(User.email == email).first()

def add_song_to_user_history(db: Session, user_id: int, song_id: int):
    """Add or update a song in user's listening history"""
    # Check if song exists in history
    stmt = user_song_history.select().where(
        (user_song_history.c.user_id == user_id) & 
        (user_song_history.c.song_id == song_id)
    )
    result = db.execute(stmt).first()
    
    if result:
        # Update listen count
        listen_count = result.listen_count + 1
        stmt = user_song_history.update().where(
            (user_song_history.c.user_id == user_id) & 
            (user_song_history.c.song_id == song_id)
        ).values(
            listen_count=listen_count,
            last_listened=db.func.current_timestamp()
        )
        db.execute(stmt)
    else:
        # Add new entry
        stmt = user_song_history.insert().values(
            user_id=user_id,
            song_id=song_id,
            listen_count=1,
            last_listened=db.func.current_timestamp()
        )
        db.execute(stmt)
    
    db.commit()