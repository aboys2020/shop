/** @type {import('tailwindcss').Config} */

export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    container: {
      center: true,
      padding: "1rem",
    },
    extend: {
      colors: {
        bg: "#0B0C10",
        surface: "#1F2833",
        "surface-2": "#2A3441",
        border: "#3A4555",
        text: "#C5C6C7",
        heading: "#FFFFFF",
        muted: "#8D99AE",
        accent: "#FF9F1C",
        "accent-2": "#2EC4B6",
        danger: "#E71D36",
      },
      fontFamily: {
        display: ["'Clash Display'", "sans-serif"],
        mono: ["'JetBrains Mono'", "ui-monospace", "monospace"],
      },
      animation: {
        "fade-in-down": "fadeInDown 0.6s ease-out forwards",
        "fade-in-up": "fadeInUp 0.6s ease-out forwards",
        pulse: "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
      keyframes: {
        fadeInDown: {
          "0%": { opacity: "0", transform: "translateY(-16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        fadeInUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
