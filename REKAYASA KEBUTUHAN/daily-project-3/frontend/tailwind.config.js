/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f2f8ff',
          100: '#dcecff',
          200: '#b7d8ff',
          300: '#82bcff',
          400: '#4798ff',
          500: '#1f76ff',
          600: '#145ee7',
          700: '#154bc8',
          800: '#1a419f',
          900: '#1b397d',
        },
      },
      fontFamily: {
        sans: ['Poppins', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        panel: '0 14px 30px -20px rgba(20, 44, 80, 0.45)',
      },
    },
  },
  plugins: [],
}
