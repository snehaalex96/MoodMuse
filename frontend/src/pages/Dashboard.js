import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { PlayerContext } from '../context/PlayerContext';
import AudioPlayer from '../components/AudioPlayer';
import SongList from '../components/SongList';
import RecommendationCard from '../components/RecommendationCard';
import MoodSelector from '../components/MoodSelector';
import ImageUploader from '../components/ImageUploader';

import api from '../services/api';

const Dashboard = () => {
  const { user, isAuthenticated } = useContext(AuthContext);
  const { currentSong } = useContext(PlayerContext);
  
  const [popularSongs, setPopularSongs] = useState([]);
  const [personalRecommendations, setPersonalRecommendations] = useState([]);
  const [recentlyPlayed, setRecentlyPlayed] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedTab, setSelectedTab] = useState('discover'); // 'discover', 'mood', 'image'
  const [selectedMood, setSelectedMood] = useState(null);
  const [moodRecommendations, setMoodRecommendations] = useState([]);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imageRecommendations, setImageRecommendations] = useState([]);
  const [imageAnalysis, setImageAnalysis] = useState(null);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  
  // Fetch data on component mount
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Get popular songs (for all users)
        const popularRes = await api.get('/recommendations/popular', { params: { limit: 10 } });
        setPopularSongs(popularRes.data.popular_songs);
        
        // Get personalized recommendations and history for authenticated users
        if (isAuthenticated) {
          const [personalRes, historyRes] = await Promise.all([
            api.get('/recommendations/user', { params: { limit: 5 } }),
            api.get('/users/history')
          ]);
          
          setPersonalRecommendations(personalRes.data.recommendations);
          setRecentlyPlayed(historyRes.data);
        }
        
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load recommendations. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, [isAuthenticated]);
  
  // Handle mood selection
  const handleMoodSelect = async (mood) => {
    setSelectedMood(mood);
    
    try {
      setLoadingRecommendations(true);
      const response = await api.get(`/recommendations/mood/${mood}`, { params: { limit: 10 } });
      setMoodRecommendations(response.data.recommendations);
    } catch (err) {
      console.error('Error fetching mood recommendations:', err);
      setError('Failed to load mood recommendations. Please try again.');
    } finally {
      setLoadingRecommendations(false);
    }
  };
  
  // Handle image upload
  const handleImageUpload = async (imageFile) => {
    setUploadedImage(imageFile);
    
    if (!imageFile) {
      setImageRecommendations([]);
      setImageAnalysis(null);
      return;
    }
    
    try {
      setLoadingRecommendations(true);
      const response = await api.getRecommendationsByImage(imageFile, 10);
      setImageRecommendations(response.data.recommendations);
      setImageAnalysis(response.data.image_analysis);
    } catch (err) {
      console.error('Error fetching image recommendations:', err);
      setError('Failed to analyze image. Please try again.');
    } finally {
      setLoadingRecommendations(false);
    }
  };
  
  if (loading) {
    return (
      <div className="dashboard loading">
        <div className="loading-spinner"></div>
        <p>Loading recommendations...</p>
      </div>
    );
  }
  
  return (
    <div className="dashboard">
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      {currentSong && <AudioPlayer />}
      
      <div className="dashboard-header">
        <h1>
          {isAuthenticated 
            ? `Welcome back, ${user.username}!` 
            : 'Discover new music with AI'}
        </h1>
        <p className="dashboard-subtitle">
          Our multimodal AI analyzes audio, visuals, and lyrics to find your perfect music match
        </p>
      </div>
      
      <div className="recommendation-tabs">
        <button 
          className={`tab-button ${selectedTab === 'discover' ? 'active' : ''}`}
          onClick={() => setSelectedTab('discover')}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 4V11H5.17L4 12.17V4H15ZM16 2H3C2.45 2 2 2.45 2 3V17L6 13H16C16.55 13 17 12.55 17 12V3C17 2.45 16.55 2 16 2ZM21 6H19V15H6V17C6 17.55 6.45 18 7 18H18L22 22V7C22 6.45 21.55 6 21 6Z" fill="currentColor"/>
          </svg>
          Discover
        </button>
        
        <button 
          className={`tab-button ${selectedTab === 'mood' ? 'active' : ''}`}
          onClick={() => setSelectedTab('mood')}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11.99 2C6.47 2 2 6.48 2 12C2 17.52 6.47 22 11.99 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12C4 7.58 7.58 4 12 4C16.42 4 20 7.58 20 12C20 16.42 16.42 20 12 20ZM15.5 11C16.33 11 17 10.33 17 9.5C17 8.67 16.33 8 15.5 8C14.67 8 14 8.67 14 9.5C14 10.33 14.67 11 15.5 11ZM8.5 11C9.33 11 10 10.33 10 9.5C10 8.67 9.33 8 8.5 8C7.67 8 7 8.67 7 9.5C7 10.33 7.67 11 8.5 11ZM12 17.5C14.33 17.5 16.31 16.04 17.11 14H6.89C7.69 16.04 9.67 17.5 12 17.5Z" fill="currentColor"/>
          </svg>
          By Mood
        </button>
        
        <button 
          className={`tab-button ${selectedTab === 'image' ? 'active' : ''}`}
          onClick={() => setSelectedTab('image')}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 19V5C21 3.9 20.1 3 19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19ZM8.5 13.5L11 16.51L14.5 12L19 18H5L8.5 13.5Z" fill="currentColor"/>
          </svg>
          By Image
        </button>
      </div>
      
      <div className="tab-content">
        {selectedTab === 'discover' && (
          <div className="discover-tab">
            {isAuthenticated && personalRecommendations.length > 0 && (
              <section className="recommendation-section">
                <h2>Recommended for You</h2>
                <div className="recommendation-cards">
                  {personalRecommendations.map(rec => (
                    <RecommendationCard 
                      key={rec.id} 
                      song={rec} 
                      similarity={rec.similarity}
                      reason="Based on your listening history"
                    />
                  ))}
                </div>
              </section>
            )}
            
            {isAuthenticated && recentlyPlayed.length > 0 && (
              <section className="recent-section">
                <h2>Recently Played</h2>
                <SongList songs={recentlyPlayed} />
              </section>
            )}
            
            <section className="popular-section">
              <h2>Popular Right Now</h2>
              <SongList songs={popularSongs} />
            </section>
          </div>
        )}
        
        {selectedTab === 'mood' && (
          <div className="mood-tab">
            <MoodSelector onMoodSelect={handleMoodSelect} selectedMood={selectedMood} />
            
            {loadingRecommendations && (
              <div className="loading-indicator">
                <div className="loading-spinner"></div>
                <p>Finding matching music...</p>
              </div>
            )}
            
            {!loadingRecommendations && selectedMood && moodRecommendations.length > 0 && (
              <section className="mood-recommendations">
                <h2>Music for {selectedMood} Mood</h2>
                <div className="recommendation-cards">
                  {moodRecommendations.map(rec => (
                    <RecommendationCard 
                      key={rec.id} 
                      song={rec} 
                      similarity={rec.mood_match}
                      reason={`Matches ${selectedMood} mood`}
                    />
                  ))}
                </div>
              </section>
            )}
            
            {!loadingRecommendations && selectedMood && moodRecommendations.length === 0 && (
              <div className="no-recommendations">
                <p>No songs found for this mood. Try a different mood.</p>
              </div>
            )}
          </div>
        )}
        
        {selectedTab === 'image' && (
          <div className="image-tab">
            <ImageUploader 
              onImageUpload={handleImageUpload}
              title="Find Music That Matches Your Image"
              description="Upload any image and our AI will analyze its mood and find matching music"
            />
            
            {loadingRecommendations && (
              <div className="loading-indicator">
                <div className="loading-spinner"></div>
                <p>Analyzing image and finding matching music...</p>
              </div>
            )}
            
            {!loadingRecommendations && imageAnalysis && (
              <div className="image-analysis">
                <h3>Image Analysis</h3>
                <p>Our AI detected: {imageAnalysis.description}</p>
                
                <div className="mood-tags">
                  {Object.entries(imageAnalysis.moods || {}).map(([mood, score]) => (
                    <span key={mood} className="mood-tag">
                      {mood} ({Math.round(score * 100)}%)
                    </span>
                  ))}
                </div>
              </div>
            )}
            
            {!loadingRecommendations && imageRecommendations.length > 0 && (
              <section className="image-recommendations">
                <h2>Music That Matches Your Image</h2>
                <div className="recommendation-cards">
                  {imageRecommendations.map(rec => (
                    <RecommendationCard 
                      key={rec.id} 
                      song={rec} 
                      similarity={rec.similarity}
                      reason="Visual style matches your image"
                    />
                  ))}
                </div>
              </section>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;