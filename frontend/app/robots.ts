import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  const isPublic = process.env.NEXT_PUBLIC_PUBLIC_RELEASE === '1';
  return isPublic ? { rules: { userAgent: '*', allow: '/' } } : { rules: { userAgent: '*', disallow: '/' } };
}
