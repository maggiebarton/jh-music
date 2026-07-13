/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./epk/index.html", "./main.js"],
  theme: {
    extend: {
      colors: {
        ink: "#070608",
        violet: "#8b5cf6",
        plum: "#2e173d",
        parchment: "#eee9e1",
      },
      fontFamily: {
        display: ["Instrument Serif", "serif"],
        artist: ["Oswald", "sans-serif"],
        sans: ["DM Sans", "sans-serif"],
      },
    },
  },
  plugins: [],
};
