const NavBar = ({ onBack, onHome, onNext }) => {
    return (
        <div className="absolute top-0 left-0 w-full flex justify-between items-center p-4">
            {/* Back Button */}
            <div
                onClick={onBack}
                className="flex items-center space-x-2 cursor-pointer transition duration-300 hover:bg-blue-200 hover:scale-110 p-2 rounded-lg z-10"
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
            </div>

            {/* Home Button with Upward Arrow */}
            <div
                onClick={onHome}
                className="flex items-center space-x-2 cursor-pointer transition duration-300 hover:bg-blue-200 hover:scale-110 p-2 rounded-lg z-10"
            >
                {/* Upward Arrow Icon */}
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
                        d="M5 15l7-7 7 7"
                    />
                </svg>

                {/* OSAA Logo */}
                <img
                    src="${basePath}/images/osaa-logo-transparent.svg"
                    alt="OSAA Logo"
                    className="w-8 h-10"
                />
            </div>

            {/* Next Button */}
            <div
                onClick={onNext}
                className="flex items-center space-x-2 cursor-pointer transition duration-300 hover:bg-blue-200 hover:scale-110 p-2 rounded-lg z-10"
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
                        d="M9 5l7 7-7 7"
                    />
                </svg>
            </div>
        </div>
    );
};

export default NavBar;
