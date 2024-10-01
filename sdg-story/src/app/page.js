"use client";

import { useState } from 'react';
import WelcomeSection from './WelcomePage';
import StorySection1 from './StoryPage1';

export default function Home() {
  const [isClicked, setIsClicked] = useState(false);

  const handleEnterStoryClick = () => {
    setIsClicked(true);
  };

  const handleHomeButtonClick = () => {
    setIsClicked(false);
  };

  return (
    <main className="relative min-h-screen overflow-hidden">

      {/* Back Button for story sections */}
      {isClicked && (
        <div 
          onClick={handleHomeButtonClick} 
          className="absolute top-4 left-4 flex items-center space-x-2 cursor-pointer transition duration-300 hover:bg-blue-200 hover:scale-110 p-2 rounded-lg z-10"
        >
          
          <svg
            className="w-6 h-6 text-black"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M15 19l-7-7 7-7"
            />
          </svg>

          <img
            src="/images/osaa-logo-transparent.png"
            alt="OSAA Logo"
            className="w-8 h-10"
          />
        </div>
      )}

      {/* Container for welcome and story sections */}
      <div
        className={`flex transition-transform duration-500 ease-in-out ${isClicked ? 'translate-x-[-100vw]' : 'translate-x-0'}`}
        style={{ width: '200vw' }}
      >
        <WelcomeSection onEnterStory={handleEnterStoryClick} />
        <StorySection1 />
      </div>
    </main>
  );
}
