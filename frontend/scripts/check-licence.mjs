// Pre-build guard: a production build fails while the release licence is TBC, unless ALLOW_TBC_LICENSE=1.
const licence = (process.env.NEXT_PUBLIC_RELEASE_LICENSE || 'CC BY 4.0').trim();
const allow = process.env.ALLOW_TBC_LICENSE === '1';
if (licence === 'TBC' && !allow) {
  console.error('\nBUILD STOPPED: NEXT_PUBLIC_RELEASE_LICENSE is TBC (no licence chosen for the HADB release).');
  console.error('Set NEXT_PUBLIC_RELEASE_LICENSE to the chosen licence, or set ALLOW_TBC_LICENSE=1 for a private preview build.\n');
  process.exit(1);
}
console.log('licence guard: release licence = %s%s', licence, licence === 'TBC' ? ' (allowed by ALLOW_TBC_LICENSE=1; site stays noindex)' : '');

// On Vercel the site must point at an HTTPS API, never at the localhost default. If the variable is unset the build uses the production API (lib/api.ts).
if (process.env.VERCEL === '1') {
  const base = (process.env.NEXT_PUBLIC_API_BASE || '').trim();
  if (!base) {
    console.log('api guard: NEXT_PUBLIC_API_BASE is not set; using the default https://api.habdsk.org');
  } else if (!base.startsWith('https://')) {
    console.error('\nBUILD STOPPED: NEXT_PUBLIC_API_BASE must be the HTTPS URL of the API on Vercel (found: "%s").\n', base);
    process.exit(1);
  }
}
