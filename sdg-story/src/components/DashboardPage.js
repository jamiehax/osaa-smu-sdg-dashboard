import React, { useState } from 'react';
import NavBar from './NavBar';
import { motion } from 'framer-motion';
import Link from 'next/link';

const DashboardPage = ({ onNext, onBack, onHome }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [modalContent, setModalContent] = useState([]);

  const cards = [
    {
      title: "Theme 1",
      description: "Public Debt Management Quality",
      topics: ["Quality of Public Expenditures", "Conditions of Money Mobilizations and Spending", "Debt Flows Indicators", "Debt Stock Indicators"],
    },
    {
      title: "Theme 2",
      description: "Domestic Instutions Ability of Changing Countrie's positions in R/GVC's",
      topics: ["Domestic Value Added (DVA)", "Access to Resources and Technology", "Integration into Regional/Global Value Chains (R/GVCs)", "Trade Costs and Efficiency", "Intra-African Trade"],
    },
    {
      title: "Theme 3",
      description: "Excercise of Ownership over Economic and Financial Flows",
      topics: ["Primary Balance", "Domestic Savings Outflow", "Pension Funds and International Reserves"],
    },
    {
      title: "Theme 4",
      description: "DRM Institutions and Systems",
      topics: ["Public Expenditures", "Budget/Tax Revenues", "Capital Markets", "Illicit Financial Flows"],
    },
    {
      title: "Theme 5",
      description: "Derisking strategies for Private Sector Engagement",
      topics: ["Integrated National Financing Frameworks (INFF)", "Planning-Programming-Budgeting-Evaluation Systems (PPBES"],
    },
  ];

  const toggleModal = (content) => {
    setIsOpen(!isOpen);
    setModalContent(content);
  };

  return (
    <>
      <NavBar onBack={onBack} onHome={onHome} onNext={onNext} />

      <div className="flex flex-col items-center justify-center p-6 h-screen max-w-7xl mx-auto">
        <h1 className="text-5xl md:text-6xl lg:text-7xl font-regular text-center text-transparent bg-clip-text bg-gradient-to-r from-black via-un-blue to-blue-300 tracking-wider mb-8">
          Sustainable Development Dashboards
        </h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full">
          {cards.map((card, index) => (
            <motion.div
              key={index}
              className="bg-white p-6 rounded-lg shadow-lg cursor-pointer hover:scale-105 transition-transform duration-300 flex flex-col items-center text-center"
              onClick={() => toggleModal(card.topics)}
            >
              <h2 className="text-2xl font-semibold mb-2">{card.title}</h2>
              <p className="text-gray-600 mb-4">{card.description}</p>
              {/* <Link href="/index" passHref> */}
                <motion.button
                  className="bg-un-blue text-white px-4 py-2 rounded-lg transition-colors duration-100 hover:bg-blue-800"
                >
                  Go to Dashboard
                </motion.button>
              {/* </Link> */}
            </motion.div>
          ))}
        </div>

      </div>

      {/* Modal */}
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center bg-opacity-50 backdrop-blur-sm"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ type: 'spring', stiffness: 120, damping: 20 }}
          onClick={() => toggleModal([])}
        >
          <motion.div
            className="relative bg-white p-8 m-4 rounded-lg shadow-sm items-center justify-center border-4 border-black"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 150, damping: 12 }}
          >
            {/* SVG X button */}
            <button
              className="absolute top-2 right-2 text-gray-400 hover:text-gray-700"
              onClick={() => toggleModal([])}
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

            {/* Content */}
            <h3 className="text-xl font-semibold justify-center mb-4">Topics</h3>
            <ul className="list-disc list-inside">
              {modalContent.map((item, index) => (
                <li key={index} className="text-gray-700 mb-2">
                  {item}
                </li>
              ))}
            </ul>
          </motion.div>
        </motion.div>
      )}
    </>
  );
};

export default DashboardPage;
