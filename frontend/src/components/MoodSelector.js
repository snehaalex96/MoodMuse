import React from 'react';

const MoodSelector = ({ onMoodSelect, selectedMood }) => {
  // Define moods with icons, colors, and descriptions
  const moods = [
    {
      id: 'happy',
      name: 'Happy',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM15.5 11C16.33 11 17 10.33 17 9.5C17 8.67 16.33 8 15.5 8C14.67 8 14 8.67 14 9.5C14 10.33 14.67 11 15.5 11ZM8.5 11C9.33 11 10 10.33 10 9.5C10 8.67 9.33 8 8.5 8C7.67 8 7 8.67 7 9.5C7 10.33 7.67 11 8.5 11ZM12 17.5C14.33 17.5 16.31 16.04 17.11 14H6.89C7.69 16.04 9.67 17.5 12 17.5Z" fill="currentColor"/>
        </svg>
      ),
      color: '#FFD166',
      description: 'Upbeat and joyful music'
    },
    {
      id: 'sad',
      name: 'Sad',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM15.5 11C16.33 11 17 10.33 17 9.5C17 8.67 16.33 8 15.5 8C14.67 8 14 8.67 14 9.5C14 10.33 14.67 11 15.5 11ZM8.5 11C9.33 11 10 10.33 10 9.5C10 8.67 9.33 8 8.5 8C7.67 8 7 8.67 7 9.5C7 10.33 7.67 11 8.5 11ZM12 14C9.67 14 7.69 15.46 6.89 17.5H17.11C16.31 15.46 14.33 14 12 14Z" fill="currentColor"/>
        </svg>
      ),
      color: '#118AB2',
      description: 'Melancholic and emotional music'
    },
    {
      id: 'energetic',
      name: 'Energetic',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M7 2V13H10V22L17 10H13L17 2H7Z" fill="currentColor"/>
        </svg>
      ),
      color: '#EF476F',
      description: 'High-energy and upbeat music'
    },
    {
      id: 'calm',
      name: 'Calm',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM10 9.5C10 10.33 9.33 11 8.5 11C7.67 11 7 10.33 7 9.5C7 8.67 7.67 8 8.5 8C9.33 8 10 8.67 10 9.5ZM17 9.5C17 10.33 16.33 11 15.5 11C14.67 11 14 10.33 14 9.5C14 8.67 14.67 8 15.5 8C16.33 8 17 8.67 17 9.5ZM12 15C13.1 15 14 14.1 14 13H10C10 14.1 10.9 15 12 15Z" fill="currentColor"/>
        </svg>
      ),
      color: '#06D6A0',
      description: 'Peaceful and relaxing music'
    },
    {
      id: 'romantic',
      name: 'Romantic',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.03L12 21.35Z" fill="currentColor"/>
        </svg>
      ),
      color: '#E63946',
      description: 'Romantic and heartfelt music'
    },
    {
      id: 'melancholic',
      name: 'Melancholic',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 3V13.55C11.41 13.21 10.73 13 10 13C7.79 13 6 14.79 6 17C6 19.21 7.79 21 10 21C12.21 21 14 19.21 14 17V7H18V3H12ZM10 19C8.9 19 8 18.1 8 17C8 15.9 8.9 15 10 15C11.1 15 12 15.9 12 17C12 18.1 11.1 19 10 19Z" fill="currentColor"/>
        </svg>
      ),
      color: '#5C4E7A',
      description: 'Reflective and nostalgic music'
    }
  ];
  
  return (
    <div className="mood-selector">
      <h3>Choose a Mood</h3>
      <p>Select a mood to get matching music recommendations</p>
      
      <div className="mood-grid">
        {moods.map((mood) => (
          <div 
            key={mood.id}
            className={`mood-card ${selectedMood === mood.id ? 'selected' : ''}`}
            onClick={() => onMoodSelect(mood.id)}
            style={{
              '--mood-color': mood.color,
              '--mood-bg-color': `${mood.color}20` // 20% opacity
            }}
          >
            <div className="mood-icon">
              {mood.icon}
            </div>
            <div className="mood-name">{mood.name}</div>
            <div className="mood-description">{mood.description}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MoodSelector;