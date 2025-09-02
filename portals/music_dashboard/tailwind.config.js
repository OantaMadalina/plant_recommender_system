/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      keyframes: {
        "zoom-in": {
          "0%": {
            opacity: 0,
            transform: "scale3d(0.3, 0.3, 0.3)",
          },
          "80%": {
            opacity: 0.8,
            transform: "scale3d(1.1, 1.1, 1.1)",
          },
          "100%": {
            opacity: 1,
          },
        },
        "zoom-out": {
          "0%": {
            opacity: 1,
          },
          "15%": {
            opacity: 0.8,
            transform: "scale3d(1.1, 1.1, 1.1)",
          },
          "100%": {
            opacity: 0,
            transform: "scale3d(0.3, 0.3, 0.3)",
          },
        },
        "fade-in": {
            "0%": {
                opacity: 0
            },
            "100%": {
                opacity: 1
            },
        },
        "fade-out": {
            "0%": {
                opacity: 1
            },
            "100%": {
                opacity: 0
            },
        },
        "fade-in-up": {
            "0%": {
                opacity: 0,
                transform: "translate3d(0, 100%, 0)",
            },
            "100%": {
                opacity: 1,
                transform: "translate3d(0, 0, 0)",
            },
        },
        "fade-out-down": {
            "0%": {
                opacity: 1,
            },
            "100%": {
                opacity: 0,
                transform: "translate3d(0, 100%, 0)",
            },
        },

      },
      animation:{
        fadeinup: 'fade-in-up 1s ease-in-out 0.25s 1',
        fadeoutdown: 'fade-out-down 1s ease-in-out 0.25s 1',
        fadein: 'fade-in 1s ease-in-out 0.25s 1',
        fadeout: 'fade-out 1s ease-out 0.25s 1',
        zoomIn: 'zoom-in 1s ease-out 0.25s 1',
        zoomOut: 'zoom-out 1s ease-out 0.25s 1',
      }
    },
  },
  plugins: [],
}

