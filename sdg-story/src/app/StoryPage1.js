import React, { useState } from 'react';

function StorySection1() {
  const [showDefinitions, setShowDefinitions] = useState(false);
  const [activeText, setActiveText] = useState(null);

  const handleClick = (text) => {
    setActiveText(text);
    setShowDefinitions(true);
  };

  const handleHideDefinitionClick = () => {
    setShowDefinitions(false);
    setActiveText(null);
  };

  return (
    <section className="w-screen min-h-screen flex bg-white relative overflow-hidden">

      {/* Button to hide definitions */}
      {showDefinitions && (
        <button
          onClick={handleHideDefinitionClick}
          className="absolute top-4 right-4 flex items-center space-x-2 cursor-pointer transition duration-500 hover:bg-blue-200 hover:scale-110 p-2 rounded-lg z-10"
        >
          <svg
            className="w-6 h-6 text-black transform rotate-180"
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
        </button>
      )}

      {/* Left Half - Story Text */}
      <div
        className={`flex flex-col items-center justify-center text-center space-y-24 transition-all duration-500 ease-in-out ${showDefinitions ? 'w-4/6' : 'w-full'}`}
      >
        <h1
          onClick={() => handleClick('Sustainable Development')}
          className="text-5xl md:text-6xl lg:text-7xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-black via-un-blue to-blue-200 tracking-wider mb-8 pb-4 cursor-pointer transition-all duration-500 hover:font-black hover:italic"
        >
          Sustainable Development
        </h1>

        <h2 className="text-3xl font-medium text-un-blue">
          is hindered by a lack of
        </h2>

        <h1
          onClick={() => handleClick('Sustainable Financing')}
          className="text-5xl md:text-6xl lg:text-7xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-blue-200 via-un-blue to-black tracking-wider mb-8 pb-4 cursor-pointer transition-all duration-500 hover:font-black hover:italic"
        >
          Sustainable Financing
        </h1>
      </div>

      {/* Right Half - Definitions Section */}
      <div
        className={`flex items-center justify-center bg-gray-100 transition-all duration-500 ease-in-out ${showDefinitions ? 'w-2/6 opacity-100' : 'w-0 opacity-0'}`}
        style={{ transitionProperty: 'width, opacity' }}
      >
        <div className="text-center p-8">
          {activeText === 'Sustainable Development' && (
            <p className="text-xl text-black text-justify leading-relaxed">
              Sustainable Development refers to ...
            </p>
          )}
          {activeText === 'Sustainable Financing' && (
            <p className="text-xl text-black text-justify leading-loose">
              Sustainable finance refers to financial practices that ensure long-term stability and growth, enabling countries to retain and create wealth while efficiently managing their own resources. It focuses on fostering inclusiveness and ensuring that investments are not only profitable but also socially and environmentally responsible. Sustainable finance empowers countries to control their financial future, reducing dependency on external, unpredictable funding sources. 
            </p>
          )}
        </div>
      </div>
    </section>
  );
}

export default StorySection1;
