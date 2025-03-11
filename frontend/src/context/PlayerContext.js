import React, { createContext, useState, useRef, useEffect } from 'react';
import api from '../services/api';

export const PlayerContext = createContext();

export const PlayerProvider = ({ children }) => {
  const [currentSong, setCurrentSong] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [volume, setVolume] = useState(0.5);
  
  const audioRef = useRef(null);
  
  useEffect(() => {
    // Initialize audio element
    audioRef.current = new Audio();
    
    // Set up event listeners
    audioRef.current.addEventListener('timeupdate', handleTimeUpdate);
    audioRef.current.addEventListener('loadedmetadata', handleLoadedMetadata);
    audioRef.current.addEventListener('ended', handleEnded);
    
    // Clean up
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.removeEventListener('timeupdate', handleTimeUpdate);
        audioRef.current.removeEventListener('loadedmetadata', handleLoadedMetadata);
        audioRef.current.removeEventListener('ended', handleEnded);
      }
    };
  }, []);
  
  // Set volume whenever it changes
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume;
    }
  }, [volume]);
  
  // Handle play/pause state
  useEffect(() => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.play().catch(error => {
          console.error('Error playing audio:', error);
          setIsPlaying(false);
        });
      } else {
        audioRef.current.pause();
      }
    }
  }, [isPlaying]);
  
  // Load song when currentSong changes
  useEffect(() => {
    if (currentSong && audioRef.current) {
      // Update audio source
      audioRef.current.src = currentSong.path;
      
      // Start playing
      audioRef.current.load();
      setIsPlaying(true);
      
      // Record song to user history if user is logged in
      const token = localStorage.getItem('token');
      if (token) {
        recordSongHistory(currentSong.id);
      }
    }
  }, [currentSong]);
  
  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };
  
  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };
  
  const handleEnded = () => {
    setIsPlaying(false);
    setCurrentTime(0);
  };
  
  const playSong = (song) => {
    setCurrentSong(song);
  };
  
  const togglePlay = () => {
    setIsPlaying(!isPlaying);
  };
  
  const stop = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsPlaying(false);
    setCurrentTime(0);
  };
  
  const seek = (time) => {
    if (audioRef.current) {
      audioRef.current.currentTime = time;
      setCurrentTime(time);
    }
  };
  
  const adjustVolume = (newVolume) => {
    setVolume(newVolume);
  };
  
  const recordSongHistory = async (songId) => {
    try {
      const token = localStorage.getItem('token');
      await api.post(`/users/history/${songId}`, {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
    } catch (error) {
      console.error('Error recording song history:', error);
    }
  };
  
  return (
    <PlayerContext.Provider
      value={{
        currentSong,
        isPlaying,
        duration,
        currentTime,
        volume,
        playSong,
        togglePlay,
        stop,
        seek,
        adjustVolume
      }}
    >
      {children}
    </PlayerContext.Provider>
  );
};