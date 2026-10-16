import type { Config } from 'tailwindcss';
import theme from './theme.json';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}', './lib/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: theme.main,
        accent: theme.accent,
        navy: theme.navy,
        sky: theme.sky_tint,
        ink: theme.text,
        t2: theme.tiers.T2,
        el: { Ni: theme.elements.Ni, Mn: theme.elements.Mn, Zn: theme.elements.Zn, Co: theme.elements.Co, other: theme.elements.other },
      },
      fontFamily: { sans: ['Arial', 'Helvetica', 'system-ui', 'sans-serif'] },
    },
  },
  plugins: [],
};
export default config;
