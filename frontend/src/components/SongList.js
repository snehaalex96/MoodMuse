import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { PlayerContext } from '../context/PlayerContext';
import api from '../services/api';

const SongList = ({ songs, showHeader = true, emptyMessage = "No songs found" }) => {
  const { isAuthenticated } = useContext(AuthContext);
  const { playSong, currentSong, isPlaying, togglePlay } = useContext(PlayerContext);
  
  // Handle playing a song
  const handlePlaySong = (song) => {
    if (currentSong && currentSong.id === song.id) {
      // If the same song is already selected, toggle play/pause
      togglePlay();
    } else {
      // Otherwise, play the new song
      playSong(song);
    }
  };
  
  // Handle liking a song
  const handleLikeSong = async (songId, e) => {
    e.stopPropagation(); // Prevent triggering row click
    
    try {
      await api.post(`/users/likes/${songId}`);
      // In a real application, you would update the liked status in the UI
      // For simplicity, we'll just show an alert
      alert('Song like status updated!');
    } catch (error) {
      console.error('Error liking song:', error);
    }
  };
  
  if (!songs || songs.length === 0) {
    return (
      <div className="songs-empty">
        <p>{emptyMessage}</p>
      </div>
    );
  }
  
  return (
    <div className="song-list">
      {showHeader && (
        <div className="song-list-header">
          <div className="song-list-cell song-number">#</div>
          <div className="song-list-cell song-info">Song</div>
          <div className="song-list-cell song-album">Album</div>
          <div className="song-list-cell song-duration">Duration</div>
          {isAuthenticated && (
            <div className="song-list-cell song-actions">Actions</div>
          )}
        </div>
      )}
      
      <div className="song-list-body">
        {songs.map((song, index) => {
          const isActive = currentSong && currentSong.id === song.id;
          const isCurrentlyPlaying = isActive && isPlaying;
          
          // Format duration (seconds to MM:SS)
          const formatDuration = (seconds) => {
            if (!seconds) return '0:00';
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = Math.floor(seconds % 60);
            return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
          };
          
          return (
            <div 
              key={song.id} 
              className={`song-list-row ${isActive ? 'active' : ''}`}
              onClick={() => handlePlaySong(song)}
            >
              <div className="song-list-cell song-number">
                {isCurrentlyPlaying ? (
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 6H10V18H8V6ZM14 6H16V18H14V6Z" fill="currentColor"/>
                  </svg>
                ) : (
                  <span>{index + 1}</span>
                )}
              </div>
              
              <div className="song-list-cell song-info">
                <div className="song-artwork">
                  {song.image_path ? (
                    <img src={song.image_path} alt={`${song.title} artwork`} />
                  ) : (
                    <div className="song-artwork-placeholder">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 3V13.55C11.41 13.21 10.73 13 10 13C7.79 13 6 14.79 6 17C6 19.21 7.79 21 10 21C12.21 21 14 19.21 14 17V7H18V3H12Z" fill="currentColor"/>
                      </svg>
                    </div>
                  )}
                </div>
                
                <div className="song-meta">
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
                </div>
              </div>
              
              <div className="song-list-cell song-album">
                {song.album}
              </div>
              
              <div className="song-list-cell song-duration">
                {formatDuration(song.duration)}
              </div>
              
              {isAuthenticated && (
                <div className="song-list-cell song-actions">
                  <button 
                    className="like-button"
                    onClick={(e) => handleLikeSong(song.id, e)}
                    title="Like song"
                  >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
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
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M14 10H2V12H14V10ZM14 6H2V8H14V6ZM18 14V10H16V14H12V16H16V20H18V16H22V14H18ZM2 16H10V14H2V16Z" fill="currentColor"/>
                    </svg>
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default SongList;