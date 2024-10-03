import Story from '../components/Story';

const Home = () => {
  return <Story />;
};

export default Home;

// "use client";

// import Layout from '../components/Layout';

// import { useState } from 'react';
// import WelcomeSection from '../components/WelcomePage';
// import StorySection1 from '../components/StorySection1';
// import StorySection2 from '../components/StorySection2';

// export default function Home() {
//   const [isClicked, setIsClicked] = useState(false);
//   const [showStorySection2, setShowStorySection2] = useState(false);

//   const handleEnterStoryClick = () => {
//     setIsClicked(true);
//   };

//   const handleHomeButtonClick = () => {
//     setIsClicked(false);
//   };

//   const handleNextSection = () => {
//     setShowStorySection2(true);
//   };

//   return (
//     <main className="relative min-h-screen overflow-hidden">

//       {/* Back Button for story sections */}
//       {isClicked && (
//         <div 
//           onClick={handleHomeButtonClick} 
//           className="absolute top-4 left-4 flex items-center space-x-2 cursor-pointer transition duration-300 hover:bg-blue-200 hover:scale-110 p-2 rounded-lg z-10"
//         >
          
//           <svg
//             className="w-6 h-6 text-black"
//             fill="none"
//             stroke="currentColor"
//             strokeWidth="2"
//             viewBox="0 0 24 24"
//             xmlns="http://www.w3.org/2000/svg"
//           >
//             <path
//               strokeLinecap="round"
//               strokeLinejoin="round"
//               d="M15 19l-7-7 7-7"
//             />
//           </svg>

//           <img
//             src="/images/osaa-logo-transparent.png"
//             alt="OSAA Logo"
//             className="w-8 h-10"
//           />
//         </div>
//       )}

//       {/* Container for welcome and story sections */}
//       <div
//         className={`flex transition-transform duration-500 ease-in-out ${isClicked ? 'translate-x-[-100vw]' : 'translate-x-0'}`}
//         style={{ width: '200vw' }}
//       >
//         <WelcomeSection onEnterStory={handleEnterStoryClick} />
//         <StorySection1 onNextSection={handleNextSection} />
//       </div>

//       {/* StorySection2 */}
//       {showStorySection2 && <StorySection2 />}
      
//     </main>
//   );
// }
