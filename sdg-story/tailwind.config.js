/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        'un-blue': '#009AD9',
        black: '#000000',
        white: '#FFFFFF',
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
      fontFamily: {
        roboto: ['Roboto', 'sans-serif'],
      },
      textShadow: {
        'default': '2px 2px 4px rgba(0, 0, 0, 0.3)',
        'lg': '4px 4px 6px rgba(0, 0, 0, 0.4)',
      },
      keyframes: {
        scroll: {
          '0%': { backgroundPosition: 'center top' },
          '100%': { backgroundPosition: 'center bottom' },
        },
      },
      animation: {
        'scroll-up-down': 'scroll 10s linear infinite',
      },
    },
  },
  plugins: [
    function ({ addUtilities }) {
      const newUtilities = {
        '.text-shadow': {
          textShadow: '2px 2px 4px rgba(0, 0, 0, 0.3)',
        },
        '.text-shadow-lg': {
          textShadow: '4px 4px 6px rgba(0, 0, 0, 0.4)',
        },
      };
      addUtilities(newUtilities, ['responsive', 'hover']);
    },
  ],
};
