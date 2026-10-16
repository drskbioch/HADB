"""Secret scan of (a) the files git would track (untracked, not ignored) and (b) the text entries of dist/backend_bundle.zip: passwords, tokens, private keys, cloud keys, e-mail addresses.
Also checks that the bundle holds no .env, certificate or record-level GBIF data. Prints findings (file:line, masked); exit 1 if any."""
import re, subprocess, sys, zipfile
from pathlib import Path
R = Path(__file__).resolve().parents[1]
PAT = {'private key': r'-----BEGIN [A-Z ]*PRIVATE KEY-----', 'aws key': r'AKIA[0-9A-Z]{16}', 'github token': r'gh[pousr]_[A-Za-z0-9]{30,}', 'slack token': r'xox[abprs]-[A-Za-z0-9-]{10,}', 'generic secret assignment': r'(?i)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token)\b\s*[:=]\s*["\']?[^\s"\'<>${}()]{6,}',
       'e-mail address': r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', 'bearer token': r'(?i)bearer\s+[A-Za-z0-9._-]{20,}'}
OK_EMAIL = re.compile(r'@(example\.(org|com)|[a-z.-]*\.invalid)$', re.I)
TEXT = {'.py', '.ts', '.tsx', '.js', '.mjs', '.json', '.md', '.txt', '.csv', '.tsv', '.yml', '.yaml', '.css', '.conf', '.example', '.cfg', '.toml', '.html', ''}
hits = []


def scan(name, text):
    for i, line in enumerate(text.splitlines(), 1):
        for k, p in PAT.items():
            for m in re.finditer(p, line):
                v = m.group(0)
                if k == 'e-mail address' and (OK_EMAIL.search(v) or v.startswith('@')): continue
                if k == 'generic secret assignment' and re.search(r'(?i)(YOUR_|PASSWORD:|<|\.\.\.|process\.env|os\.environ)', v): continue
                hits.append('%s:%d [%s] %s...' % (name, i, k, v[:6] + '***'))


files = subprocess.run(['git', 'ls-files', '-co', '--exclude-standard'], cwd=R, capture_output=True, text=True).stdout.splitlines(); n = 0
for f in files:
    p = R / f
    if p.suffix.lower() in TEXT and p.is_file() and p.stat().st_size < 3_000_000 and 'package-lock.json' not in f:
        n += 1; scan(f, p.read_text(encoding='utf-8', errors='ignore'))
bundle = R / 'dist' / 'backend_bundle.zip'; nb = 0
if bundle.exists():
    with zipfile.ZipFile(bundle) as z:
        for e in z.namelist():
            low = e.lower()
            if low.endswith(('.env', '.pem', '.key', '.zip')) or '/.env' in low or low == '.env' or 'records_' in low or 'occurrence' in low and low.endswith('.csv.gz'): hits.append('bundle entry not allowed: ' + e)
            if Path(e).suffix.lower() in TEXT and not e.endswith('.sqlite'):
                nb += 1; scan('bundle:' + e, z.read(e).decode('utf-8', errors='ignore'))
        sql = z.read('data/hadb.sqlite');
        for pat in (b'decimalLatitude', b'decimalLongitude', b'hasGeospatialIssue'):
            if pat in sql: hits.append('sqlite contains the column name %s' % pat.decode())
for h in hits: print('FINDING', h)
print('secret scan: %d git-tracked text files, %d bundle text entries, %d finding(s)' % (n, nb, len(hits))); sys.exit(1 if hits else 0)
