import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import logging

from config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeatureFusion:
    """
    Utility class for combining features from different modalities
    """
    def __init__(self, 
                 audio_weight: float = 0.5, 
                 image_weight: float = 0.3, 
                 text_weight: float = 0.2):
        """
        Initialize feature fusion with weights for each modality
        
        Args:
            audio_weight: Weight for audio features (default: 0.5)
            image_weight: Weight for image features (default: 0.3)
            text_weight: Weight for text features (default: 0.2)
        """
        self.audio_weight = audio_weight
        self.image_weight = image_weight
        self.text_weight = text_weight
        
        # Feature dimensions from settings
        self.audio_dim = settings.AUDIO_FEATURE_DIMENSIONS
        self.image_dim = settings.IMAGE_FEATURE_DIMENSIONS
        self.text_dim = settings.TEXT_FEATURE_DIMENSIONS
    
    def combine_features(self, 
                         audio_features: np.ndarray, 
                         image_features: np.ndarray, 
                         text_features: np.ndarray,
                         method: str = 'concatenate') -> np.ndarray:
        """
        Combine features from multiple modalities
        
        Args:
            audio_features: Audio features
            image_features: Image features
            text_features: Text features
            method: Method to combine features ('concatenate', 'weighted_sum', 'average')
            
        Returns:
            Combined feature vector
        """
        # Normalize each feature vector
        audio_norm = self._normalize(audio_features)
        image_norm = self._normalize(image_features)
        text_norm = self._normalize(text_features)
        
        if method == 'concatenate':
            # Apply weights
            weighted_audio = audio_norm * self.audio_weight
            weighted_image = image_norm * self.image_weight
            weighted_text = text_norm * self.text_weight
            
            # Concatenate features
            combined = np.concatenate([weighted_audio, weighted_image, weighted_text])
            
        elif method == 'weighted_sum':
            # Resize all features to the same dimension
            target_dim = max(len(audio_norm), len(image_norm), len(text_norm))
            audio_resized = self._resize_features(audio_norm, target_dim)
            image_resized = self._resize_features(image_norm, target_dim)
            text_resized = self._resize_features(text_norm, target_dim)
            
            # Weighted sum
            combined = (audio_resized * self.audio_weight + 
                        image_resized * self.image_weight + 
                        text_resized * self.text_weight)
            
        elif method == 'average':
            # Resize all features to the same dimension
            target_dim = max(len(audio_norm), len(image_norm), len(text_norm))
            audio_resized = self._resize_features(audio_norm, target_dim)
            image_resized = self._resize_features(image_norm, target_dim)
            text_resized = self._resize_features(text_norm, target_dim)
            
            # Simple average
            combined = (audio_resized + image_resized + text_resized) / 3
            
        else:
            # Default to concatenation
            combined = np.concatenate([audio_norm, image_norm, text_norm])
        
        # Final normalization
        combined = self._normalize(combined)
        
        return combined
    
    def _normalize(self, features: np.ndarray) -> np.ndarray:
        """Normalize feature vector to unit length"""
        norm = np.linalg.norm(features)
        if norm > 0:
            return features / norm
        return features
    
    def _resize_features(self, features: np.ndarray, target_dim: int) -> np.ndarray:
        """Resize feature vector to target dimension"""
        if len(features) == target_dim:
            return features
        
        if len(features) > target_dim:
            # Truncate
            return features[:target_dim]
        else:
            # Pad with zeros
            padding = np.zeros(target_dim - len(features))
            return np.concatenate([features, padding])
    
    def adjust_weights(self, 
                       audio_weight: Optional[float] = None, 
                       image_weight: Optional[float] = None, 
                       text_weight: Optional[float] = None):
        """
        Adjust the weights for each modality
        
        Args:
            audio_weight: New weight for audio features
            image_weight: New weight for image features
            text_weight: New weight for text features
        """
        if audio_weight is not None:
            self.audio_weight = audio_weight
        
        if image_weight is not None:
            self.image_weight = image_weight
        
        if text_weight is not None:
            self.text_weight = text_weight
        
        # Normalize weights to sum to 1
        total = self.audio_weight + self.image_weight + self.text_weight
        if total > 0:
            self.audio_weight /= total
            self.image_weight /= total
            self.text_weight /= total

    def get_weights(self) -> Dict[str, float]:
        """
        Get the current weights for each modality
        
        Returns:
            Dictionary of weights
        """
        return {
            "audio_weight": self.audio_weight,
            "image_weight": self.image_weight,
            "text_weight": self.text_weight
        }