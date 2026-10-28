import type { Metadata } from 'next';
import { Roboto } from 'next/font/google';
import './globals.css';
import Shell from '@/components/Shell';

// Self-hosted at build time: the browser makes no request to Google.
const roboto = Roboto({ subsets: ['latin'], weight: ['400', '700'], display: 'swap', variable: '--font-roboto' });

const isPublic = process.env.NEXT_PUBLIC_PUBLIC_RELEASE === '1';

export const metadata: Metadata = {
  title: { default: 'HADB: Hyperaccumulator Database', template: '%s | HADB' },
  description: 'HADB v1: plants reported to accumulate or hyperaccumulate Ni, Mn, Zn, Co and other elements, with evidence, tiers, citations and environment summaries.',
  robots: isPublic ? { index: true, follow: true } : { index: false, follow: false },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={roboto.variable}>
      <body>
        <Shell>{children}</Shell>
      </body>
    </html>
  );
}
