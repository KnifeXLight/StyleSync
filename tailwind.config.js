/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'selector',
  content: ["./**/*.{html,js}"], 
  theme: {
    extend: {}
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: {
    colors : {
      "logo" :"#8a2be2",
  },
},
},
};