import type { Config } from 'tailwindcss';
import theme from './theme.json';

// UI colours follow the parent S Khan Lab sites (AVPCD and siblings). The element and tier colours still come from theme.json,
// which is shared with the figure scripts, so charts and the web keep one colour per element.
const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}', './lib/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: '#0e22af', // royal blue: links, buttons, key numbers (contrast on white > 9:1)
        navy: '#040486', // deep blue: headings, active nav pill, table rules
        accent: '#328af1', // lab blue: borders and decoration only (contrast on white ~3.6:1, not for text)
        sky: '#e4f6fa', // pale card background
        skydeep: '#d3e9fd', // panel background
        ink: theme.text,
        t2: theme.tiers.T2,
        el: { Ni: theme.elements.Ni, Mn: theme.elements.Mn, Zn: theme.elements.Zn, Co: theme.elements.Co, other: theme.elements.other },
      },
      fontFamily: { sans: ['var(--font-roboto)', 'Arial', 'Helvetica', 'system-ui', 'sans-serif'] },
    },
  },
  plugins: [],
};
export default config;
