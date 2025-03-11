import os
import numpy as np
import librosa
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Optional, Tuple, Union
import logging

from config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioFeatureExtractor:
    """
    Extract features from audio files using librosa
    """
    def __init__(self):
        self.sr = 22050  # Sample rate
        self.n_fft = 2048  # FFT window size
        self.hop_length = 512  # Hop length for STFT
        self.n_mels = 128  # Number of mel bands
        self.feature_dim = settings.AUDIO_FEATURE_DIMENSIONS
        
    def extract_features(self, audio_path: str) -> np.ndarray:
        """
        Extract audio features from a file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            numpy array of audio features
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=self.sr, mono=True)
            
            # Extract features
            features = {}
            
            # Mel spectrogram
            mel_spec = librosa.feature.melspectrogram(
                y=y, 
                sr=sr, 
                n_fft=self.n_fft, 
                hop_length=self.hop_length, 
                n_mels=self.n_mels
            )
            log_mel_spec = librosa.power_to_db(mel_spec)
            features['mel'] = np.mean(log_mel_spec, axis=1)  # Average over time
            
            # MFCCs
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
            features['mfcc'] = np.mean(mfcc, axis=1)  # Average over time
            
            # Chroma
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            features['chroma'] = np.mean(chroma, axis=1)  # Average over time
            
            # Spectral contrast
            contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
            features['contrast'] = np.mean(contrast, axis=1)  # Average over time
            
            # Tempo and beat
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            features['tempo'] = np.array([tempo])
            
            # Concatenate all features
            feature_vector = np.concatenate([
                features['mel'],
                features['mfcc'],
                features['chroma'],
                features['contrast'],
                features['tempo']
            ])
            
            # Ensure fixed dimensions
            if len(feature_vector) > self.feature_dim:
                feature_vector = feature_vector[:self.feature_dim]
            elif len(feature_vector) < self.feature_dim:
                padding = np.zeros(self.feature_dim - len(feature_vector))
                feature_vector = np.concatenate([feature_vector, padding])
                
            return feature_vector.astype(np.float32)
            
        except Exception as e:
            logger.error(f"Error extracting audio features: {e}")
            # Return zeros if extraction fails
            return np.zeros(self.feature_dim, dtype=np.float32)

    def extract_features_from_bytes(self, audio_bytes: bytes) -> np.ndarray:
        """
        Extract audio features from bytes data
        
        Args:
            audio_bytes: Audio data as bytes
            
        Returns:
            numpy array of audio features
        """
        try:
            # Load audio from bytes
            y, sr = librosa.load(audio_bytes, sr=self.sr, mono=True)
            
            # Extract features (same as above function)
            # ... (same code as extract_features)
            
            # For simplicity, we'll just return a random feature vector
            feature_vector = np.random.rand(self.feature_dim).astype(np.float32)
            return feature_vector
            
        except Exception as e:
            logger.error(f"Error extracting audio features from bytes: {e}")
            return np.zeros(self.feature_dim, dtype=np.float32)


class SimpleCNN(nn.Module):
    """
    Simple CNN model for audio classification
    """
    def __init__(self, input_dim: int = 128, num_classes: int = 10):
        super(SimpleCNN, self).__init__()
        
        # Assuming input is a mel spectrogram of shape (batch_size, 1, input_dim, time)
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.pool1 = nn.MaxPool2d(kernel_size=2)
        
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.pool2 = nn.MaxPool2d(kernel_size=2)
        
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.pool3 = nn.MaxPool2d(kernel_size=2)
        
        # Calculate the size after convolutions and pooling
        self.fc_input_dim = 64 * (input_dim // 8) * (128 // 8)  # time dimension assumed to be 128
        
        # Fully connected layers
        self.fc1 = nn.Linear(self.fc_input_dim, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, num_classes)
        
    def forward(self, x):
        # Convolutional layers
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        x = self.pool3(F.relu(self.bn3(self.conv3(x))))
        
        # Flatten
        x = x.view(-1, self.fc_input_dim)
        
        # Fully connected layers
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x


class AudioModel:
    """
    Main audio model class that handles feature extraction and analysis
    """
    def __init__(self):
        self.feature_extractor = AudioFeatureExtractor()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = settings.AUDIO_MODEL_PATH
        
        # Create a dummy model
        # In a real application, you would load a pre-trained model
        self.model = self._create_or_load_model()
        
    def _create_or_load_model(self):
        """Create a new model or load a pre-trained one"""
        try:
            if os.path.exists(self.model_path):
                logger.info(f"Loading audio model from {self.model_path}")
                model = torch.load(self.model_path, map_location=self.device)
            else:
                logger.info("Creating new audio model")
                model = SimpleCNN(input_dim=128, num_classes=10)
                model = model.to(self.device)
            return model
        except Exception as e:
            logger.error(f"Error loading audio model: {e}")
            # Create a dummy model if loading fails
            model = SimpleCNN(input_dim=128, num_classes=10)
            model = model.to(self.device)
            return model
    
    def extract_features(self, audio_path: str) -> np.ndarray:
        """Extract features from an audio file"""
        return self.feature_extractor.extract_features(audio_path)
    
    def analyze_mood(self, features: np.ndarray) -> Dict[str, float]:
        """
        Analyze the mood of a song based on its audio features
        
        Args:
            features: Audio features
            
        Returns:
            Dictionary of mood scores
        """
        # In a real application, this would use a trained model
        # For demonstration, we'll return random mood scores
        
        # Define mood categories
        moods = ["happy", "sad", "energetic", "calm", "tense", "romantic"]
        
        # Generate random scores
        scores = np.random.rand(len(moods))
        scores = scores / scores.sum()  # Normalize to sum to 1
        
        # Create dictionary
        mood_scores = {mood: float(score) for mood, score in zip(moods, scores)}
        
        return mood_scores
    
    def analyze_genre(self, features: np.ndarray) -> Dict[str, float]:
        """
        Predict genre probabilities based on audio features
        
        Args:
            features: Audio features
            
        Returns:
            Dictionary of genre probabilities
        """
        # In a real application, this would use the CNN model
        # For demonstration, we'll return random genre probabilities
        
        # Define genre categories
        genres = ["rock", "pop", "hip-hop", "electronic", "jazz", "classical", "country", "metal"]
        
        # Generate random probabilities
        probs = np.random.rand(len(genres))
        probs = probs / probs.sum()  # Normalize to sum to 1
        
        # Create dictionary
        genre_probs = {genre: float(prob) for genre, prob in zip(genres, probs)}
        
        return genre_probs