import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { PlayerContext } from '../context/PlayerContext';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';

const RecommendationCard = ({ song, similarity, reason }) => {
  const { playSong, currentSong, isPlaying, togglePlay } = useContext(PlayerContext);
  const { isAuthenticated } = useContext(AuthContext);
  
  // Format similarity score as percentage
  const formatSimilarity = (score) => {
    if (score === undefined || score === null) return null;
    return `${Math.round(score * 100)}%`;
  };
  
  // Handle playing a song
  const handlePlaySong = () => {
    if (currentSong && currentSong.id === song.id) {
      // If the same song is already selected, toggle play/pause
      togglePlay();
    } else {
      // Otherwise, play the new song
      playSong(song);
    }
  };
  
  // Handle liking a song
  const handleLikeSong = async (e) => {
    e.stopPropagation(); // Prevent triggering card click
    
    try {
      await api.post(`/users/likes/${song.id}`);
      // In a real application, you would update the liked status in the UI
      // For simplicity, we'll just show an alert
      alert('Song like status updated!');
    } catch (error) {
      console.error('Error liking song:', error);
    }
  };
  
  // Determine if this is the currently playing song
  const isActive = currentSong && currentSong.id === song.id;
  const isCurrentlyPlaying = isActive && isPlaying;
  
  return (
    <div className={`recommendation-card ${isActive ? 'active' : ''}`} onClick={handlePlaySong}>
      <div className="recommendation-artwork">
        {song.image_path ? (
          <img src={song.image_path} alt={`${song.title} artwork`} />
        ) : (
          <div className="artwork-placeholder">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 3V13.55C11.41 13.21 10.73 13 10 13C7.79 13 6 14.79 6 17C6 19.21 7.79 21 10 21C12.21 21 14 19.21 14 17V7H18V3H12ZM10 19C8.9 19 8 18.1 8 17C8 15.9 8.9 15 10 15C11.1 15 12 15.9 12 17C12 18.1 11.1 19 10 19Z" fill="currentColor"/>
            </svg>
          </div>
        )}
        
        <div className="play-overlay">
          {isCurrentlyPlaying ? (
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 19H10V5H6V19ZM14 5V19H18V5H14Z" fill="currentColor"/>
            </svg>
          ) : (
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
            </svg>
          )}
        </div>
      </div>
      
      <div className="recommendation-info">
        <div className="recommendation-meta">
          <Link 
            to={`/song/${song.id}`}
            className="song-title"
            onClick={(e) => e.stopPropagation()}
          >
            {song.title}
          </Link>
          
          <Link 
            to={`/songs/artist/${song.artist}`}
            className="song-artist"
            onClick={(e) => e.stopPropagation()}
          >
            {song.artist}
          </Link>
          
          <div className="song-album">{song.album}</div>
        </div>
        
        {similarity !== undefined && (
          <div className="similarity-score">
            <div className="similarity-label">Match</div>
            <div className="similarity-value">{formatSimilarity(similarity)}</div>
          </div>
        )}
        
        {reason && (
          <div className="recommendation-reason">
            {reason}
          </div>
        )}
      </div>
      
      {isAuthenticated && (
        <div className="recommendation-actions">
          <button 
            className="like-button"
            onClick={handleLikeSong}
            title="Like song"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16.5 3C14.76 3 13.09 3.81 12 5.09C10.91 3.81 9.24 3 7.5 3C4.42 3 2 5.42 2 8.5C2 12.28 5.4 15.36 10.55 20.04L12 21.35L13.45 20.03C18.6 15.36 22 12.28 22 8.5C22 5.42 19.58 3 16.5 3ZM12.1 18.55L12 18.65L11.9 18.55C7.14 14.24 4 11.39 4 8.5C4 6.5 5.5 5 7.5 5C9.04 5 10.54 5.99 11.07 7.36H12.94C13.46 5.99 14.96 5 16.5 5C18.5 5 20 6.5 20 8.5C20 11.39 16.86 14.24 12.1 18.55Z" fill="currentColor"/>
            </svg>
          </button>
          
          <button
            className="add-playlist-button"
            onClick={(e) => {
              e.stopPropagation();
              alert('Add to playlist feature coming soon!');
            }}
            title="Add to playlist"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M14 10H2V12H14V10ZM14 6H2V8H14V6ZM18 14V10H16V14H12V16H16V20H18V16H22V14H18ZM2 16H10V14H2V16Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
      )}
    </div>
  );
};

export default RecommendationCard;