import type { Metadata } from 'next';
import './globals.css';
import Shell from '@/components/Shell';

const isPublic = process.env.NEXT_PUBLIC_PUBLIC_RELEASE === '1';

export const metadata: Metadata = {
  title: { default: 'HADB: Hyperaccumulator Database', template: '%s | HADB' },
  description: 'HADB v1: plants reported to accumulate or hyperaccumulate Ni, Mn, Zn, Co and other elements, with evidence, tiers, citations and environment summaries.',
  robots: isPublic ? { index: true, follow: true } : { index: false, follow: false },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Shell>{children}</Shell>
      </body>
    </html>
  );
}
