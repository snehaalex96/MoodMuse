import os
import numpy as np
import librosa
from PIL import Image
import re
from typing import Dict, List, Optional, Tuple, Union
import logging
from pathlib import Path
import shutil

from config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioPreprocessor:
    """
    Preprocess audio files for feature extraction
    """
    def __init__(self):
        self.target_sr = 22050  # Target sample rate
        self.mono = True  # Convert to mono
        
    def preprocess(self, audio_path: str, output_path: Optional[str] = None) -> str:
        """
        Preprocess audio file
        
        Args:
            audio_path: Path to audio file
            output_path: Path to save preprocessed file (optional)
            
        Returns:
            Path to preprocessed audio file
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=self.target_sr, mono=self.mono)
            
            # If output path is provided, save preprocessed audio
            if output_path:
                # Make sure directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Save as WAV
                librosa.output.write_wav(output_path, y, sr)
                
                return output_path
            
            # If no output path, return original path
            return audio_path
            
        except Exception as e:
            logger.error(f"Error preprocessing audio: {e}")
            return audio_path
    
    def get_duration(self, audio_path: str) -> float:
        """
        Get duration of audio file in seconds
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Duration in seconds
        """
        try:
            y, sr = librosa.load(audio_path, sr=None)
            return librosa.get_duration(y=y, sr=sr)
        except Exception as e:
            logger.error(f"Error getting audio duration: {e}")
            return 0.0

class ImagePreprocessor:
    """
    Preprocess images for feature extraction
    """
    def __init__(self):
        self.target_size = (224, 224)  # Target image size
        self.rgb = True  # Convert to RGB
        
    def preprocess(self, image_path: str, output_path: Optional[str] = None) -> str:
        """
        Preprocess image file
        
        Args:
            image_path: Path to image file
            output_path: Path to save preprocessed file (optional)
            
        Returns:
            Path to preprocessed image file
        """
        try:
            # Load image
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if self.rgb and img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to target size
            img = img.resize(self.target_size, Image.LANCZOS)
            
            # If output path is provided, save preprocessed image
            if output_path:
                # Make sure directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Save as PNG
                img.save(output_path, format='PNG')
                
                return output_path
            
            # If no output path, return original path
            return image_path
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return image_path
    
    def extract_colors(self, image_path: str, num_colors: int = 5) -> List[Tuple[int, int, int]]:
        """
        Extract dominant colors from image
        
        Args:
            image_path: Path to image file
            num_colors: Number of colors to extract
            
        Returns:
            List of RGB color tuples
        """
        try:
            # Load image
            img = Image.open(image_path)
            img = img.convert('RGB')
            img = img.resize((100, 100))  # Resize for performance
            
            # Get pixel data
            pixels = list(img.getdata())
            
            # Count colors
            color_counts = {}
            for pixel in pixels:
                if pixel in color_counts:
                    color_counts[pixel] += 1
                else:
                    color_counts[pixel] = 1
            
            # Get most common colors
            dominant_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Return top N colors
            return [color for color, count in dominant_colors[:num_colors]]
            
        except Exception as e:
            logger.error(f"Error extracting colors: {e}")
            return [(0, 0, 0)]  # Default to black

class TextPreprocessor:
    """
    Preprocess text for feature extraction
    """
    def __init__(self):
        self.remove_special_chars = True
        self.lowercase = True
        
    def preprocess(self, text: str) -> str:
        """
        Preprocess text
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
            
        # Convert to string
        if not isinstance(text, str):
            text = str(text)
            
        # Convert to lowercase
        if self.lowercase:
            text = text.lower()
            
        # Replace newlines with spaces
        text = text.replace('\n', ' ')
        
        # Remove special characters
        if self.remove_special_chars:
            text = re.sub(r'[^\w\s]', '', text)
            
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            max_keywords: Maximum number of keywords to extract
            
        Returns:
            List of keywords
        """
        # Preprocess text
        processed_text = self.preprocess(text)
        
        # Split into words
        words = processed_text.split()
        
        # Remove stopwords (simple implementation)
        stopwords = {'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 
                     'be', 'been', 'being', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 
                     'about', 'as', 'of', 'that', 'this', 'these', 'those', 'it', 'its', 
                     'you', 'your', 'i', 'my', 'me', 'mine', 'we', 'us', 'our', 'they', 'them'}
        
        words = [word for word in words if word not in stopwords]
        
        # Count word frequencies
        word_counts = {}
        for word in words:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
        
        # Sort by frequency
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Return top N keywords
        return [word for word, count in sorted_words[:max_keywords]]

class FileManager:
    """
    Utility class for managing files
    """
    def __init__(self):
        # Create data directories if they don't exist
        self.audio_dir = Path(settings.AUDIO_SAMPLES_DIR)
        self.images_dir = Path(settings.IMAGES_DIR)
        self.metadata_dir = Path(settings.METADATA_DIR)
        
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
    
    def save_uploaded_file(self, file_bytes: bytes, filename: str, file_type: str) -> str:
        """
        Save uploaded file to appropriate directory
        
        Args:
            file_bytes: File content as bytes
            filename: Name of the file
            file_type: Type of file ('audio', 'image', or 'metadata')
            
        Returns:
            Path to saved file
        """
        try:
            # Determine target directory
            if file_type == 'audio':
                target_dir = self.audio_dir
            elif file_type == 'image':
                target_dir = self.images_dir
            elif file_type == 'metadata':
                target_dir = self.metadata_dir
            else:
                raise ValueError(f"Invalid file type: {file_type}")
            
            # Create full path
            file_path = target_dir / filename
            
            # Write file
            with open(file_path, 'wb') as f:
                f.write(file_bytes)
            
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return ""
    
    def copy_file(self, source_path: str, file_type: str) -> str:
        """
        Copy file to appropriate directory
        
        Args:
            source_path: Path to source file
            file_type: Type of file ('audio', 'image', or 'metadata')
            
        Returns:
            Path to copied file
        """
        try:
            source_path = Path(source_path)
            
            # Determine target directory
            if file_type == 'audio':
                target_dir = self.audio_dir
            elif file_type == 'image':
                target_dir = self.images_dir
            elif file_type == 'metadata':
                target_dir = self.metadata_dir
            else:
                raise ValueError(f"Invalid file type: {file_type}")
            
            # Create target path
            target_path = target_dir / source_path.name
            
            # Copy file
            shutil.copy2(source_path, target_path)
            
            return str(target_path)
            
        except Exception as e:
            logger.error(f"Error copying file: {e}")
            return ""