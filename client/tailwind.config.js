/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        risk: {
          low: '#22c55e',
          medium: '#f59e0b',
          high: '#ef4444',
          critical: '#991b1b',
        },
        status: {
          stable: '#22c55e',
          watch: '#f59e0b',
          critical: '#ef4444',
          discharged: '#6b7280',
        },
        medical: {
          primary: '#0891b2',
          secondary: '#06b6d4',
          accent: '#14b8a6',
        },
      },
    },
  },
  plugins: [],
}
