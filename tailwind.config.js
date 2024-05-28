/** @type {import('tailwindcss').Config} */
module.exports = {
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