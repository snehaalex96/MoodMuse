import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle common errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle 401 Unauthorized errors (token expired or invalid)
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      // Reload the page to reset app state
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API functions for songs
export const getSongs = async (skip = 0, limit = 20) => {
  return api.get(`/songs?skip=${skip}&limit=${limit}`);
};

export const getSongById = async (songId) => {
  return api.get(`/songs/${songId}`);
};

export const getSongsByArtist = async (artist) => {
  return api.get(`/songs/artist/${encodeURIComponent(artist)}`);
};

export const addSong = async (songData) => {
  const formData = new FormData();
  for (const key in songData) {
    formData.append(key, songData[key]);
  }
  return api.post('/songs', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// API functions for recommendations
export const getRecommendationsBySong = async (songId, limit = 5) => {
  return api.get(`/recommendations/song/${songId}?limit=${limit}`);
};

export const getRecommendationsByMood = async (mood, limit = 5) => {
  return api.get(`/recommendations/mood/${mood}?limit=${limit}`);
};

export const getRecommendationsByImage = async (imageFile, limit = 5) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  formData.append('limit', limit);
  
  return api.post('/recommendations/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const getPersonalizedRecommendations = async (limit = 5) => {
  return api.get(`/recommendations/user?limit=${limit}`);
};

export const getPopularSongs = async (limit = 5) => {
  return api.get(`/recommendations/popular?limit=${limit}`);
};

// API functions for user management
export const register = async (userData) => {
  return api.post('/users/register', userData);
};

export const login = async (username, password) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  
  return api.post('/users/token', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const getCurrentUser = async () => {
  return api.get('/users/me');
};

export const getLikedSongs = async () => {
  return api.get('/users/likes');
};

export const toggleLikeSong = async (songId) => {
  return api.post(`/users/likes/${songId}`);
};

export const getListeningHistory = async () => {
  return api.get('/users/history');
};

export default api;