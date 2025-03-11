import React, { useContext, useEffect, useRef, useState } from 'react';
import { PlayerContext } from '../context/PlayerContext';
import { Link } from 'react-router-dom';

const AudioPlayer = () => {
  const { 
    currentSong, 
    isPlaying, 
    duration, 
    currentTime, 
    volume,
    togglePlay, 
    stop, 
    seek, 
    adjustVolume 
  } = useContext(PlayerContext);
  
  const [showVolumeControl, setShowVolumeControl] = useState(false);
  const progressBarRef = useRef(null);
  
  // Format time in MM:SS
  const formatTime = (timeInSeconds) => {
    if (isNaN(timeInSeconds)) return '0:00';
    
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = Math.floor(timeInSeconds % 60);
    
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };
  
  // Handle click on progress bar to seek
  const handleProgressBarClick = (e) => {
    if (progressBarRef.current && duration > 0) {
      const progressBar = progressBarRef.current;
      const rect = progressBar.getBoundingClientRect();
      const clickPosition = (e.clientX - rect.left) / rect.width;
      const newTime = clickPosition * duration;
      
      seek(newTime);
    }
  };
  
  // Toggle volume control visibility
  const toggleVolumeControl = () => {
    setShowVolumeControl(!showVolumeControl);
  };
  
  // Handle volume change
  const handleVolumeChange = (e) => {
    const newVolume = parseFloat(e.target.value);
    adjustVolume(newVolume);
  };
  
  // Calculate progress percentage
  const progressPercentage = duration > 0 ? (currentTime / duration) * 100 : 0;
  
  // If no song is playing, don't render the player
  if (!currentSong) {
    return null;
  }
  
  return (
    <div className="audio-player">
      <div className="container">
        <div className="player-content">
          <div className="song-info">
            {currentSong.image_path ? (
              <img 
                src={currentSong.image_path} 
                alt={`${currentSong.title} album art`} 
                className="album-art"
              />
            ) : (
              <div className="album-art-placeholder">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 3V13.55C11.41 13.21 10.73 13 10 13C7.79 13 6 14.79 6 17C6 19.21 7.79 21 10 21C12.21 21 14 19.21 14 17V7H18V3H12ZM10 19C8.9 19 8 18.1 8 17C8 15.9 8.9 15 10 15C11.1 15 12 15.9 12 17C12 18.1 11.1 19 10 19Z" fill="currentColor"/>
                </svg>
              </div>
            )}
            
            <div className="song-details">
              <Link to={`/song/${currentSong.id}`} className="song-title">
                {currentSong.title}
              </Link>
              <Link to={`/songs/artist/${currentSong.artist}`} className="song-artist">
                {currentSong.artist}
              </Link>
            </div>
          </div>
          
          <div className="player-controls">
            <button className="control-button" onClick={stop}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M6 6H18V18H6V6Z" fill="currentColor"/>
              </svg>
            </button>
            
            <button className="control-button play-button" onClick={togglePlay}>
              {isPlaying ? (
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6 19H10V5H6V19ZM14 5V19H18V5H14Z" fill="currentColor"/>
                </svg>
              ) : (
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
                </svg>
              )}
            </button>
            
            <div className="volume-control-wrapper">
              <button className="control-button" onClick={toggleVolumeControl}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 9V15H7L12 20V4L7 9H3ZM16.5 12C16.5 10.23 15.48 8.71 14 7.97V16.02C15.48 15.29 16.5 13.77 16.5 12ZM14 3.23V5.29C16.89 6.15 19 8.83 19 12C19 15.17 16.89 17.85 14 18.71V20.77C18.01 19.86 21 16.28 21 12C21 7.72 18.01 4.14 14 3.23Z" fill="currentColor"/>
                </svg>
              </button>
              
              {showVolumeControl && (
                <div className="volume-slider-container">
                  <input 
                    type="range" 
                    min="0" 
                    max="1" 
                    step="0.01"
                    value={volume}
                    onChange={handleVolumeChange}
                    className="volume-slider"
                  />
                </div>
              )}
            </div>
          </div>
          
          <div className="progress-container">
            <span className="time current-time">{formatTime(currentTime)}</span>
            <div 
              className="progress-bar" 
              ref={progressBarRef}
              onClick={handleProgressBarClick}
            >
              <div 
                className="progress" 
                style={{ width: `${progressPercentage}%` }}
              ></div>
            </div>
            <span className="time total-time">{formatTime(duration)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AudioPlayer;