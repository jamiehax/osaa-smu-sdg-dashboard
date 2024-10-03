import { useState } from 'react';
import NavBar from './NavBar';
import { motion } from 'framer-motion';

const StoryPage1 = ({ onBack, onHome, onNext }) => {

  const [isOpen, setIsOpen] = useState(false);
  const [modalText, setModalText] = useState(null);

  const toggleDefinition = (text) => {
    setIsOpen(!isOpen);
    setModalText(text);
  };

  const handleClickOutside = (e) => {
    if (e.target.id === 'modal-background') {
      toggleDefinition();
    }
  };

  const sustainableDevelopmentDef = "Sustainable Development refers to ...";
  const sustainableFinancingDef = "Sustainable finance refers to financial practices that ensure long-term stability and growth, enabling countries to retain and create wealth while efficiently managing their own resources. It focuses on fostering inclusiveness and ensuring that investments are not only profitable but also socially and environmentally responsible. Sustainable finance empowers countries to control their financial future, reducing dependency on external, unpredictable funding sources.";

  return (
    <>
      <NavBar onBack={onHome} onHome={onHome} onNext={onNext} />

      <div className="flex flex-col items-center justify-center p-24 m-24 h-screen max-w-7xl mx-auto">

        <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-center text-transparent m-12 bg-clip-text bg-gradient-to-r from-black via-un-blue to-blue-300 tracking-wider cursor-pointer transition-all duration-500 relative hover:italic hover:after:w-full after:content-[''] after:absolute after:left-0 after:bottom-0 after:w-0 after:h-1 after:bg-un-blue after:transition-all after:duration-500" onClick={() => toggleDefinition(sustainableDevelopmentDef)}>
          Sustainable Development
        </h1>

        <h1 className="text-4xl font-regular text-center text-transparent m-12 bg-clip-text bg-gradient-to-r from-blue-300 via-black to-un-blue tracking-wider">
          is hindered by a lack of
        </h1>

        <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-center text-transparent m-12 pb-4 bg-clip-text bg-gradient-to-r from-blue-300 via-un-blue to-black tracking-wider cursor-pointer transition-all duration-500 relative hover:italic hover:after:w-full after:content-[''] after:absolute after:left-0 after:bottom-0 after:w-0 after:h-1 after:bg-un-blue after:transition-all after:duration-500" onClick={() => toggleDefinition(sustainableFinancingDef)}>
          Sustainable Financing
        </h1>

      </div>

      {/* Modal */}
      {isOpen && (
        <motion.div
          id="modal-background"
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ type: 'spring', stiffness: 120, damping: 20 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-opacity-50 backdrop-blur-sm"
          onClick={handleClickOutside}
        >
          <motion.div
            className="relative bg-white p-8 m-4 rounded-lg shadow-sm flex items-center justify-center border-4 border-black" // Limits width to middle third of the page
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 150, damping: 12 }}
          >
            {/* SVG X button */}
            <button
              className="absolute top-2 right-2 text-gray-400 hover:text-gray-700"
              onClick={toggleDefinition}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 hover:scale-150 transition-all duration-300 scale:125"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>

            {/* Modal content */}
            <div className="text-center">
              <p className="tracking-wider text-2xl font-medium">
                {modalText}
              </p>
            </div>
          </motion.div>
        </motion.div>
      )}

    </>
  );
};

export default StoryPage1;
