// Pre-build guard: a production build fails while the release licence is TBC, unless ALLOW_TBC_LICENSE=1.
const licence = (process.env.NEXT_PUBLIC_RELEASE_LICENSE || 'TBC').trim();
const allow = process.env.ALLOW_TBC_LICENSE === '1';
if (licence === 'TBC' && !allow) {
  console.error('\nBUILD STOPPED: NEXT_PUBLIC_RELEASE_LICENSE is TBC (no licence chosen for the HADB release).');
  console.error('Set NEXT_PUBLIC_RELEASE_LICENSE to the chosen licence, or set ALLOW_TBC_LICENSE=1 for a private preview build.\n');
  process.exit(1);
}
console.log('licence guard: release licence = %s%s', licence, licence === 'TBC' ? ' (allowed by ALLOW_TBC_LICENSE=1; site stays noindex)' : '');

// On Vercel the site must point at the real HTTPS API, never at the localhost default.
if (process.env.VERCEL === '1') {
  const base = (process.env.NEXT_PUBLIC_API_BASE || '').trim();
  if (!base.startsWith('https://')) {
    console.error('\nBUILD STOPPED: NEXT_PUBLIC_API_BASE must be the HTTPS URL of the API on Vercel (found: "%s").\n', base || 'not set');
    process.exit(1);
  }
}
