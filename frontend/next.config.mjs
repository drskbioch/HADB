// Contact Us: /contact redirects (307, not permanent) to the HADB site (https); the nav link keeps the /contact URL.
const isPublicRelease = process.env.NEXT_PUBLIC_PUBLIC_RELEASE === '1';

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  images: { unoptimized: true },
  async redirects() {
    return [{ source: '/contact', destination: 'https://habdsk.org/', permanent: false }];
  },
  async headers() {
    const h = [
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'X-Frame-Options', value: 'DENY' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Content-Security-Policy', value: "frame-ancestors 'none'; base-uri 'self'; object-src 'none'" },
    ];
    if (!isPublicRelease) h.push({ key: 'X-Robots-Tag', value: 'noindex, nofollow' });
    return [{ source: '/(.*)', headers: h }];
  },
};

export default nextConfig;
