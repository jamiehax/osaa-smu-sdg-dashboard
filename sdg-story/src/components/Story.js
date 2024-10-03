import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import WelcomePage from './WelcomePage';
import StoryPage1 from './StoryPage1';
import StoryPage2 from './StoryPage2';
import DashboardPage from './DashboardPage';

const Story = () => {
  const [currentSection, setCurrentSection] = useState('welcome');

  // Define motion variants for the welcome screen transition
  const welcomeVariants = {
    hidden: { opacity: 0, scale: 1.2 },
    enter: { opacity: 1, scale: 1, transition: { duration: 0.25, ease: 'easeInOut' } },
    exit: { opacity: 0, scale: 1.2, transition: { duration: 1, ease: 'easeInOut' } },
  };

  // Define motion variants for the story sections (onNext - moving forward)
  const storyVariants = {
    hidden: { opacity: 0, scale: 1, x: 200, filter: 'blur(4px)' },
    enter: { opacity: 1, scale: 1, x: 0, filter: 'blur(0px)', transition: { duration: 0.25, ease: 'easeInOut' } },
    exit: { opacity: 0, scale: 1, filter: 'blur(4px)', transition: { duration: 0.25, ease: 'easeInOut' } },
  };

  const renderSection = () => {
    switch (currentSection) {
      case 'welcome':
        return (
          <motion.div
            key="welcome"
            initial="hidden"
            animate="enter"
            exit="exit"
            variants={welcomeVariants}
            className="absolute bg-white flex items-center justify-center"
          >
            <WelcomePage 
              onStart={() => setCurrentSection('storyPage1')}
              onDashboard={() => setCurrentSection('dashboardPage')}
           />
          </motion.div>
        );
      case 'storyPage1':
        return (
          <motion.div
            key="storyPage1"
            initial="hidden"
            animate="enter"
            exit="exit"
            variants={storyVariants}
            className="absolute inset-0 bg-white flex items-center justify-center"
          >
            <StoryPage1 
              onNext={() => setCurrentSection('storyPage2')} 
              onHome={() => setCurrentSection('welcome')} 
              onBack={() => setCurrentSection('welcome')}
            />
          </motion.div>
        );
      case 'storyPage2':
        return (
          <motion.div
            key="storyPage2"
            initial="hidden"
            animate="enter"
            exit="exit"
            variants={storyVariants}
            className="absolute inset-0 bg-white flex items-center justify-center"
          >
            <StoryPage2 
              onNext={() => setCurrentSection('dashboardPage')} 
              onBack={() => setCurrentSection('storyPage1')} 
              onHome={() => setCurrentSection('welcome')} 
            />
          </motion.div>
        );
        case 'dashboardPage':
        return (
          <motion.div
            key="storyPage3"
            initial="hidden"
            animate="enter"
            exit="exit"
            variants={storyVariants}
            className="absolute inset-0 bg-white flex items-center justify-center"
          >
            <DashboardPage 
              onNext={() => setCurrentSection('welcome')} 
              onBack={() => setCurrentSection('storyPage2')} 
              onHome={() => setCurrentSection('welcome')} 
            />
          </motion.div>
        );
      default:
        return (
          <motion.div
            key="default"
            initial="hidden"
            animate="enter"
            exit="exit"
            variants={welcomeVariants}
            className="absolute inset-0 bg-white flex items-center justify-center"
          >
            <WelcomePage onStart={() => setCurrentSection('storyPage1')} />
          </motion.div>
        );
    }
  };

  return (
    <div className="relative w-full h-screen overflow-hidden bg-white">
      <AnimatePresence mode="wait">
        {renderSection()}
      </AnimatePresence>
    </div>
  );
};

export default Story;
