import os
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from typing import Dict, List, Tuple, Optional, Union
import logging
from io import BytesIO

from config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageFeatureExtractor:
    """
    Extract features from images using pre-trained models
    """
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Set up image transforms
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        # Load pre-trained model
        self.model = self._load_model()
        self.feature_dim = settings.IMAGE_FEATURE_DIMENSIONS
        
    def _load_model(self):
        """Load a pre-trained model"""
        try:
            # Load ResNet model
            model = models.resnet50(pretrained=True)
            
            # Remove the classification layer to get features
            model = nn.Sequential(*list(model.children())[:-1])
            
            # Set to evaluation mode
            model = model.to(self.device)
            model.eval()
            
            return model
        except Exception as e:
            logger.error(f"Error loading image model: {e}")
            return None
    
    def extract_features(self, image_path: str) -> np.ndarray:
        """
        Extract features from an image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            numpy array of image features
        """
        try:
            # Load and preprocess image
            img = Image.open(image_path).convert('RGB')
            img_tensor = self.transform(img).unsqueeze(0).to(self.device)
            
            # Extract features
            with torch.no_grad():
                features = self.model(img_tensor)
                
            # Reshape and convert to numpy
            features = features.squeeze().cpu().numpy()
            
            # Ensure fixed dimensions
            if len(features) > self.feature_dim:
                features = features[:self.feature_dim]
            elif len(features) < self.feature_dim:
                padding = np.zeros(self.feature_dim - len(features))
                features = np.concatenate([features, padding])
                
            return features.astype(np.float32)
            
        except Exception as e:
            logger.error(f"Error extracting image features: {e}")
            # Return zeros if extraction fails
            return np.zeros(self.feature_dim, dtype=np.float32)
    
    def extract_features_from_bytes(self, image_bytes: bytes) -> np.ndarray:
        """
        Extract features from image bytes
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            numpy array of image features
        """
        try:
            # Load image from bytes
            img = Image.open(BytesIO(image_bytes)).convert('RGB')
            img_tensor = self.transform(img).unsqueeze(0).to(self.device)
            
            # Extract features
            with torch.no_grad():
                features = self.model(img_tensor)
                
            # Reshape and convert to numpy
            features = features.squeeze().cpu().numpy()
            
            # Ensure fixed dimensions
            if len(features) > self.feature_dim:
                features = features[:self.feature_dim]
            elif len(features) < self.feature_dim:
                padding = np.zeros(self.feature_dim - len(features))
                features = np.concatenate([features, padding])
                
            return features.astype(np.float32)
            
        except Exception as e:
            logger.error(f"Error extracting image features from bytes: {e}")
            # Return zeros if extraction fails
            return np.zeros(self.feature_dim, dtype=np.float32)

class ImageModel:
    """
    Main image model class that handles feature extraction and analysis
    """
    def __init__(self):
        self.feature_extractor = ImageFeatureExtractor()
        
    def extract_features(self, image_path: str) -> np.ndarray:
        """Extract features from an image file"""
        return self.feature_extractor.extract_features(image_path)
    
    def extract_features_from_bytes(self, image_bytes: bytes) -> np.ndarray:
        """Extract features from image bytes"""
        return self.feature_extractor.extract_features_from_bytes(image_bytes)
    
    def analyze_colors(self, image_path: str) -> Dict[str, List[Tuple[int, int, int]]]:
        """
        Analyze the color palette of an image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with dominant colors
        """
        try:
            # Load image
            img = Image.open(image_path).convert('RGB')
            img = img.resize((150, 150))  # Resize for faster processing
            
            # Convert to numpy array
            img_array = np.array(img)
            
            # Reshape to list of pixels
            pixels = img_array.reshape(-1, 3)
            
            # Simple clustering to find dominant colors
            # In a real application, you would use k-means
            # For simplicity, we'll just sample random pixels
            num_colors = 5
            indices = np.random.choice(len(pixels), num_colors, replace=False)
            dominant_colors = pixels[indices]
            
            # Convert to tuples
            dominant_colors = [tuple(color) for color in dominant_colors]
            
            return {"dominant_colors": dominant_colors}
            
        except Exception as e:
            logger.error(f"Error analyzing image colors: {e}")
            return {"dominant_colors": [(0, 0, 0)]}  # Default to black
    
    def analyze_mood(self, features: np.ndarray) -> Dict[str, float]:
        """
        Analyze the mood of an image based on its features
        
        Args:
            features: Image features
            
        Returns:
            Dictionary of mood scores
        """
        # In a real application, this would use a trained model
        # For demonstration, we'll return random mood scores
        
        # Define mood categories
        moods = ["happy", "sad", "energetic", "calm", "dramatic", "romantic"]
        
        # Generate random scores
        scores = np.random.rand(len(moods))
        scores = scores / scores.sum()  # Normalize to sum to 1
        
        # Create dictionary
        mood_scores = {mood: float(score) for mood, score in zip(moods, scores)}
        
        return mood_scores