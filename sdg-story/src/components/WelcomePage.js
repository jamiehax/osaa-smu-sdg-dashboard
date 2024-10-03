const WelcomePage = ({ onStart, onDashboard}) => {

    return (

      <section className="flex w-screen min-h-screen bg-white">

        {/* Left half - Text */}
        <div className="flex flex-col justify-start items-center w-1/2 p-12 bg-white min-h-screen">
          
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-black via-un-blue to-blue-300 text-center tracking-wider mb-8 pb-4">
            UN-OSAA Interactive SDG Story
          </h1>

          <button onClick={onDashboard} className="w-2/3 bg-gradient-to-r from-blue-300 via-un-blue to-black text-white px-4 py-3 rounded-lg transition-transform transform hover:scale-105 hover:shadow-lg duration-300">
            Go to Dashboards
          </button>
          
          <div className="flex items-center justify-center flex-col h-full">
            <img
              src="/images/sdg-circle-logo.png"
              alt="SDG Logo"
              className="transition-transform duration-300 spin-animation max-h-[50vh] "
            />
          </div>

          <div>
            <p>Interactive Story and Data Dashboards developed by UN-OSAA SMU Data Team.</p>
          </div>

        </div>
  
        {/* Right half - Clickable logo to enter story */}
        <div
          className="w-1/2 flex items-center p-12 justify-end relative h-screen overflow-hidden group cursor-pointer"
          onClick={onStart}
        >
          <img
            src="/images/osaa-logo-transparent.svg"
            alt="OSAA logo"
            className="h-full object-cover transition-transform duration-500 group-hover:transform-logo"
          />

          {/* "Enter Story" always visible, Arrow fades in */}
          <div className="absolute bottom-4 left-24 transform transition-all duration-500">
            <div className="flex items-center space-x-2">
              <span className="text-4xl font-bold" style={{ color: '#E6883C' }}>Enter Story</span>
              <svg
                className="w-12 h-12 text-un-blue opacity-0 transition-opacity duration-500 group-hover:opacity-100"
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

export default WelcomePage;