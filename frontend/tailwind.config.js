/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#4f46e5',
          50: '#f5f5ff',
          100: '#ecebfe',
          200: '#d9d7fd',
          300: '#b9b5fc',
          400: '#948af9',
          500: '#7c6ff5',
          600: '#6152eb',
          700: '#4f46e5',
          800: '#3730a3',
          900: '#312e81',
          950: '#1e1b4b',
        },
        background: '#f9fafb',
        card: '#ffffff',
        foreground: '#111827',
        muted: '#f3f4f6',
        accent: '#4338ca',
        success: '#22c55e',
        warning: '#eab308',
        danger: '#ef4444',
        'card-foreground': '#111827',
        'muted-foreground': '#6b7280',
        'accent-foreground': '#ffffff',
        'success-foreground': '#ffffff',
        'warning-foreground': '#ffffff',
        'danger-foreground': '#ffffff',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      keyframes: {
        'accordion-down': {
          from: { height: 0 },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: 0 },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};
