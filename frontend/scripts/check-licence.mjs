// Pre-build guard: a production build fails while the release licence is TBC, unless ALLOW_TBC_LICENSE=1.
const licence = (process.env.NEXT_PUBLIC_RELEASE_LICENSE || 'CC BY 4.0').trim();
const allow = process.env.ALLOW_TBC_LICENSE === '1';
if (licence === 'TBC' && !allow) {
  console.error('\nBUILD STOPPED: NEXT_PUBLIC_RELEASE_LICENSE is TBC (no licence chosen for the HADB release).');
  console.error('Set NEXT_PUBLIC_RELEASE_LICENSE to the chosen licence, or set ALLOW_TBC_LICENSE=1 for a private preview build.\n');
  process.exit(1);
}
console.log('licence guard: release licence = %s%s', licence, licence === 'TBC' ? ' (allowed by ALLOW_TBC_LICENSE=1; site stays noindex)' : '');

// The API address is fixed into the build (NEXT_PUBLIC_*). A missing value stops the build instead of baking in a wrong URL; on Vercel it must be HTTPS.
const base = (process.env.NEXT_PUBLIC_API_BASE || '').trim();
if (!base) {
  console.error('\nBUILD STOPPED: NEXT_PUBLIC_API_BASE is not set. Set it to the API address without a trailing slash, for example https://hadb-api.vercel.app\n');
  process.exit(1);
}
if (process.env.VERCEL === '1' && !base.startsWith('https://')) {
  console.error('\nBUILD STOPPED: NEXT_PUBLIC_API_BASE must be the HTTPS URL of the API on Vercel (found: "%s").\n', base);
  process.exit(1);
}
if (base.endsWith('/')) {
  console.error('\nBUILD STOPPED: NEXT_PUBLIC_API_BASE must not end with a slash (found: "%s").\n', base);
  process.exit(1);
}
console.log('api guard: API base = %s', base);
