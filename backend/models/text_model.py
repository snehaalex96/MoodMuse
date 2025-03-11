import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from typing import Dict, List, Optional, Union
import logging
import re

from config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextFeatureExtractor:
    """
    Extract features from text using pre-trained language models
    """
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load pre-trained model and tokenizer
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Small, efficient model
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name).to(self.device)
            self.model.eval()
        except Exception as e:
            logger.error(f"Error loading text model: {e}")
            self.tokenizer = None
            self.model = None
            
        self.feature_dim = settings.TEXT_FEATURE_DIMENSIONS
    
    def _mean_pooling(self, model_output, attention_mask):
        """Mean pooling to get sentence embedding"""
        token_embeddings = model_output[0]  # First element of model_output contains token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    def extract_features(self, text: str) -> np.ndarray:
        """
        Extract features from text
        
        Args:
            text: Input text
            
        Returns:
            numpy array of text features
        """
        try:
            if self.tokenizer is None or self.model is None:
                return np.zeros(self.feature_dim, dtype=np.float32)
                
            # Clean and preprocess text
            text = self._preprocess_text(text)
            
            # Tokenize
            encoded_input = self.tokenizer(
                text, 
                padding=True, 
                truncation=True, 
                max_length=512, 
                return_tensors='pt'
            ).to(self.device)
            
            # Extract features
            with torch.no_grad():
                model_output = self.model(**encoded_input)
                
            # Mean pooling
            sentence_embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])
            
            # Normalize embeddings
            sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
            
            # Convert to numpy
            features = sentence_embeddings.squeeze().cpu().numpy()
            
            # Ensure fixed dimensions
            if len(features) > self.feature_dim:
                features = features[:self.feature_dim]
            elif len(features) < self.feature_dim:
                padding = np.zeros(self.feature_dim - len(features))
                features = np.concatenate([features, padding])
                
            return features.astype(np.float32)
            
        except Exception as e:
            logger.error(f"Error extracting text features: {e}")
            # Return zeros if extraction fails
            return np.zeros(self.feature_dim, dtype=np.float32)
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not text:
            return ""
            
        # Convert to string
        if not isinstance(text, str):
            text = str(text)
            
        # Replace newlines with spaces
        text = text.replace('\n', ' ')
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        
        return text.strip()

class TextModel:
    """
    Main text model class that handles text feature extraction and analysis
    """
    def __init__(self):
        self.feature_extractor = TextFeatureExtractor()
        
    def extract_features(self, text: str) -> np.ndarray:
        """Extract features from text"""
        return self.feature_extractor.extract_features(text)
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with sentiment scores
        """
        # In a real application, you would use a sentiment analysis model
        # For demonstration, we'll use a simple rule-based approach
        
        # Define positive and negative keywords
        positive_words = ["love", "happy", "joy", "amazing", "great", "wonderful", "beautiful"]
        negative_words = ["sad", "pain", "hate", "hurt", "angry", "broken", "cry"]
        
        # Count word occurrences
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total_count = positive_count + negative_count
        if total_count == 0:
            # Default to neutral
            return {
                "positive": 0.5,
                "negative": 0.5,
                "compound": 0.0
            }
        
        # Calculate normalized scores
        positive_score = positive_count / total_count
        negative_score = negative_count / total_count
        
        # Compound score ranges from -1 (negative) to 1 (positive)
        compound_score = positive_score - negative_score
        
        return {
            "positive": float(positive_score),
            "negative": float(negative_score),
            "compound": float(compound_score)
        }
    
    def extract_themes(self, text: str) -> List[str]:
        """
        Extract main themes from text
        
        Args:
            text: Input text
            
        Returns:
            List of themes
        """
        # In a real application, you would use a topic modeling approach
        # For demonstration, we'll use a simple keyword matching approach
        
        # Define theme keywords
        theme_keywords = {
            "love": ["love", "heart", "romance", "passion"],
            "party": ["party", "dance", "club", "night"],
            "heartbreak": ["heartbreak", "cry", "tears", "broken"],
            "nostalgia": ["remember", "past", "memory", "nostalgia"],
            "empowerment": ["power", "strong", "rise", "stand"],
            "spirituality": ["god", "heaven", "soul", "spirit"],
            "social issues": ["world", "change", "fight", "justice"]
        }
        
        # Find matching themes
        text_lower = text.lower()
        matching_themes = []
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                matching_themes.append(theme)
                
        # If no themes found, return unknown
        if not matching_themes:
            return ["unknown"]
            
        return matching_themes