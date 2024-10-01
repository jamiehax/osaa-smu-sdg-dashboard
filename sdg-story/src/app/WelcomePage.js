import React from 'react';

const WelcomeSection = ({ onEnterStory }) => {
  return (
    <section className="flex w-screen min-h-screen">
      {/* Left half - Text */}
      <div className="flex flex-col justify-start items-center w-1/2 p-8 bg-white pt-24 min-h-screen">
        <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-black via-un-blue to-blue-200 text-center tracking-wider mb-8 pb-4">
          Welcome to UN-OSAA's Interactive SDG Story
        </h1>
        <div className="flex items-center justify-center flex-col h-full">
          <img
            src="/images/sdg-circle-logo.png"
            alt="SDG Logo"
            className="transition-transform duration-300 spin-animation max-h-[50vh] "
          />
        </div>
      </div>

      {/* Right half - Clickable logo to enter story */}
      <div className="w-1/2 flex items-center justify-end relative h-screen overflow-hidden group">
        <img
          onClick={onEnterStory}
          src="/images/osaa-logo-transparent.png"
          alt="OSAA logo"
          className="h-full object-cover cursor-pointer transform transition-transform duration-500 hover:transform-logo"
        />
        {/* Right Arrow sliding in on hover */}
        <div className="absolute bottom-4 left-24 opacity-0 transform -translate-x-20 transition-all duration-500 group-hover:translate-x-0 group-hover:opacity-100">
          <div className="flex items-center space-x-2">
            <span className="text-4xl font-bold" style={{ color: '#E6883C' }}>Enter</span>
            <svg
              className="w-12 h-12 text-un-blue"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              style={{ color: '#E6883C' }}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9 5l7 7-7 7"
              />
            </svg>
          </div>
        </div>
      </div>
    </section>
  );
};

export default WelcomeSection;
