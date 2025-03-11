import numpy as np
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Tuple, Union
import logging
from sklearn.metrics.pairwise import cosine_similarity

from database.db import Song, User, deserialize_features
from models.audio_model import AudioModel
from models.image_model import ImageModel
from models.text_model import TextModel
from config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeatureFusion:
    """
    Combine features from different modalities
    """
    def __init__(self):
        # Feature weighting
        self.audio_weight = 0.5
        self.image_weight = 0.3
        self.text_weight = 0.2
        
    def combine_features(self, 
                         audio_features: np.ndarray, 
                         image_features: np.ndarray, 
                         text_features: np.ndarray) -> np.ndarray:
        """
        Combine features from multiple modalities
        
        Args:
            audio_features: Audio features
            image_features: Image features
            text_features: Text features
            
        Returns:
            Combined feature vector
        """
        # Normalize each feature vector
        audio_norm = self._normalize(audio_features)
        image_norm = self._normalize(image_features)
        text_norm = self._normalize(text_features)
        
        # Apply weights
        weighted_audio = audio_norm * self.audio_weight
        weighted_image = image_norm * self.image_weight
        weighted_text = text_norm * self.text_weight
        
        # Concatenate features
        combined = np.concatenate([weighted_audio, weighted_image, weighted_text])
        
        return combined
    
    def _normalize(self, features: np.ndarray) -> np.ndarray:
        """Normalize feature vector to unit length"""
        norm = np.linalg.norm(features)
        if norm > 0:
            return features / norm
        return features

class Recommender:
    """
    Music recommendation system using multimodal features
    """
    def __init__(self, db: Session):
        self.db = db
        self.audio_model = AudioModel()
        self.image_model = ImageModel()
        self.text_model = TextModel()
        self.feature_fusion = FeatureFusion()
        
    def get_song_features(self, song_id: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get features for a specific song
        
        Args:
            song_id: ID of the song
            
        Returns:
            Tuple of (audio_features, image_features, text_features)
        """
        song = self.db.query(Song).filter(Song.id == song_id).first()
        if not song:
            return (
                np.zeros(settings.AUDIO_FEATURE_DIMENSIONS),
                np.zeros(settings.IMAGE_FEATURE_DIMENSIONS),
                np.zeros(settings.TEXT_FEATURE_DIMENSIONS)
            )
            
        # Deserialize features
        audio_features = deserialize_features(
            song.audio_features, 
            (settings.AUDIO_FEATURE_DIMENSIONS,)
        )
        
        image_features = deserialize_features(
            song.image_features, 
            (settings.IMAGE_FEATURE_DIMENSIONS,)
        )
        
        text_features = deserialize_features(
            song.text_features, 
            (settings.TEXT_FEATURE_DIMENSIONS,)
        )
        
        return audio_features, image_features, text_features
    
    def get_content_based_recommendations(self, song_id: int, n_recommendations: int = 5) -> List[Dict]:
        """
        Get content-based recommendations based on a seed song
        
        Args:
            song_id: ID of the seed song
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended songs with similarity scores
        """
        # Get seed song features
        seed_audio, seed_image, seed_text = self.get_song_features(song_id)
        
        # Combine features
        seed_combined = self.feature_fusion.combine_features(seed_audio, seed_image, seed_text)
        
        # Get all songs
        songs = self.db.query(Song).all()
        
        # Calculate similarity with all songs
        similarities = []
        
        for song in songs:
            # Skip the seed song
            if song.id == song_id:
                continue
                
            # Get song features
            audio_features = deserialize_features(
                song.audio_features, 
                (settings.AUDIO_FEATURE_DIMENSIONS,)
            )
            
            image_features = deserialize_features(
                song.image_features, 
                (settings.IMAGE_FEATURE_DIMENSIONS,)
            )
            
            text_features = deserialize_features(
                song.text_features, 
                (settings.TEXT_FEATURE_DIMENSIONS,)
            )
            
            # Combine features
            combined = self.feature_fusion.combine_features(
                audio_features, 
                image_features, 
                text_features
            )
            
            # Calculate similarity
            similarity = cosine_similarity([seed_combined], [combined])[0][0]
            
            similarities.append({
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "album": song.album,
                "similarity": float(similarity)
            })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Return top N recommendations
        return similarities[:n_recommendations]
    
    def get_mood_based_recommendations(self, mood: str, n_recommendations: int = 5) -> List[Dict]:
        """
        Get recommendations based on mood
        
        Args:
            mood: Target mood (e.g., "happy", "sad", "energetic")
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended songs
        """
        # Get all songs
        songs = self.db.query(Song).all()
        
        # For demonstration, we'll generate random mood scores
        # In a real application, you would analyze the audio and lyrics
        
        recommendations = []
        
        for song in songs:
            # Generate random mood match score
            mood_match = np.random.rand()
            
            recommendations.append({
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "album": song.album,
                "mood_match": float(mood_match)
            })
        
        # Sort by mood match
        recommendations.sort(key=lambda x: x["mood_match"], reverse=True)
        
        # Return top N recommendations
        return recommendations[:n_recommendations]
    
    def get_image_based_recommendations(self, image_features: np.ndarray, n_recommendations: int = 5) -> List[Dict]:
        """
        Get recommendations based on an uploaded image
        
        Args:
            image_features: Features extracted from the uploaded image
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended songs
        """
        # Get all songs
        songs = self.db.query(Song).all()
        
        # Calculate similarity with all songs based on image features
        similarities = []
        
        for song in songs:
            # Get song image features
            song_image_features = deserialize_features(
                song.image_features,
                (settings.IMAGE_FEATURE_DIMENSIONS,)
            )
            
            # Calculate similarity
            similarity = cosine_similarity([image_features], [song_image_features])[0][0]
            
            similarities.append({
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "album": song.album,
                "similarity": float(similarity)
            })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Return top N recommendations
        return similarities[:n_recommendations]
    
    def get_personalized_recommendations(self, user_id: int, n_recommendations: int = 5) -> List[Dict]:
        """
        Get personalized recommendations for a user
        
        Args:
            user_id: ID of the user
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended songs
        """
        # Get user
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
            
        # Get user's liked songs
        liked_songs = user.liked_songs
        
        # If user has no liked songs, return popular songs
        if not liked_songs:
            return self.get_popular_songs(n_recommendations)
            
        # Get features of liked songs
        liked_song_features = []
        
        for song in liked_songs:
            audio_features, image_features, text_features = self.get_song_features(song.id)
            combined = self.feature_fusion.combine_features(
                audio_features,
                image_features,
                text_features
            )
            liked_song_features.append(combined)
            
        # Average features to create user profile
        user_profile = np.mean(liked_song_features, axis=0)
        
        # Get all songs
        all_songs = self.db.query(Song).all()
        
        # Calculate similarity with all songs
        similarities = []
        
        for song in all_songs:
            # Skip songs user has already liked
            if song in liked_songs:
                continue
                
            # Get song features
            audio_features, image_features, text_features = self.get_song_features(song.id)
            combined = self.feature_fusion.combine_features(
                audio_features,
                image_features,
                text_features
            )
            
            # Calculate similarity with user profile
            similarity = cosine_similarity([user_profile], [combined])[0][0]
            
            similarities.append({
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "album": song.album,
                "similarity": float(similarity)
            })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Return top N recommendations
        return similarities[:n_recommendations]
    
    def get_popular_songs(self, n_recommendations: int = 5) -> List[Dict]:
        """
        Get popular songs
        
        Args:
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of popular songs
        """
        # In a real application, you would calculate popularity based on listen counts
        # For demonstration, we'll return random songs
        
        songs = self.db.query(Song).all()
        
        # Shuffle songs
        np.random.shuffle(songs)
        
        # Return top N songs
        popular_songs = []
        for song in songs[:n_recommendations]:
            popular_songs.append({
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "album": song.album,
                "popularity": float(np.random.rand())  # Random popularity score
            })
            
        return popular_songs