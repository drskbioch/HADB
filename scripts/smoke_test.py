"""Local smoke test: starts the API (port 8010) and the built frontend (port 3010), checks every page and endpoint over HTTP, stops both. Prints failures only.
Needs a frontend build made with NEXT_PUBLIC_API_BASE=http://127.0.0.1:8010 (see DEPLOY.md / run_smoke.sh). Not tested here: client-side rendering in a browser (no browser available),
the responsive sidebar, keyboard navigation and screen-reader behaviour."""
import json, re, subprocess, sys, time, urllib.parse
from pathlib import Path
import requests

R = Path(__file__).resolve().parents[1]; API, WEB = 'http://127.0.0.1:8010', 'http://127.0.0.1:3010'
fails, notes = [], []


def check(name, ok, detail=''):
    if not ok: fails.append('FAIL %s %s' % (name, detail))


def wait(url, tries=60):
    for _ in range(tries):
        try:
            if requests.get(url, timeout=2).status_code < 500: return True
        except Exception: time.sleep(1)
    return False


def main():
    import os
    env = dict(os.environ, HADB_CORS_ORIGINS='http://127.0.0.1:3010,http://localhost:3010')
    api = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'app.main:app', '--port', '8010', '--log-level', 'warning'], cwd=R / 'backend', env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    web = subprocess.Popen(['node', str(R / 'frontend/node_modules/next/dist/bin/next'), 'start', '-p', '3010'], cwd=R / 'frontend', env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        check('API starts', wait(API + '/api/v1/health')); check('frontend starts', wait(WEB + '/'))
        s = requests.get(API + '/api/v1/species', params=dict(q='Noccaea caerulescens'), timeout=10).json()['items'][0]['species_id']
        # ---- API endpoints
        for p, key in (('/api/v1/health', 'status'), ('/api/v1/species?element=Ni&tier=T1&page_size=5', 'items'), ('/api/v1/species/%d' % s, 'evidence'), ('/api/v1/elements', 'items'), ('/api/v1/families', 'items'), ('/api/v1/stats', 'headline_counts'),
                       ('/api/v1/versions', 'gbif_doi'), ('/api/v1/downloads', 'items'), ('/api/v1/openapi.json', 'paths')):
            r = requests.get(API + p, timeout=15); check('API ' + p, r.status_code == 200 and key in r.text, r.status_code)
        r = requests.get(API + '/api/v1/health', headers={'Origin': 'http://127.0.0.1:3010'}); check('CORS from the frontend origin', r.headers.get('access-control-allow-origin') == 'http://127.0.0.1:3010')
        r = requests.get(API + '/api/v1/health', headers={'Origin': 'http://evil.example'}); check('CORS refuses other origins', 'access-control-allow-origin' not in r.headers)
        dl = requests.get(API + '/api/v1/downloads').json()['items'][0]; r = requests.get(API + '/api/v1/downloads/' + dl['name']); check('download served', r.status_code == 200 and len(r.content) == dl['bytes'])
        # ---- frontend pages
        pages = {'/': 'Hyperaccumulator', '/about': 'not assessed (no coverage outside the Americas)', '/browse': 'Browse the database', '/browse?element=Ni&tier=T1': 'Browse the database', '/species/%d' % s: 'Loading', '/statistics': 'Figure 5', '/evidence-tiers': 'Thresholds',
                 '/downloads': 'Downloads', '/api-docs': '/api/v1/species', '/citation': '10.15468/dl.kb25da'}
        for p, txt in pages.items():
            r = requests.get(WEB + p, timeout=20); h = r.text
            check('page %s 200' % p, r.status_code == 200, r.status_code); check('page %s text' % p, txt in h, txt)
            check('page %s landmarks' % p, all(t in h for t in ('<header', '<nav', '<aside', '<main', '<footer')))
            check('page %s skip link' % p, 'Skip to content' in h); check('page %s noindex header' % p, 'noindex' in r.headers.get('x-robots-tag', '')); check('page %s no cookies' % p, 'set-cookie' not in r.headers)
            check('page %s sidebar links' % p, all(('href="%s"' % x) in h for x in ('/about', '/browse', '/statistics', '/evidence-tiers', '/downloads', '/api-docs', '/citation', '/contact')))
            check('page %s element shortcuts' % p, all(('/browse?element=%s' % e) in h for e in ('Ni', 'Mn', 'Zn', 'Co')) and all(('/browse?tier=%s' % t) in h for t in ('T1', 'T2')))
            for img in re.findall(r'<img[^>]*>', h): check('img alt on %s' % p, ' alt="' in img and ' alt=""' not in img, img[:80])
        r = requests.get(WEB + '/contact', allow_redirects=False); check('contact redirect 307', r.status_code == 307 and r.headers.get('location', '').startswith('https://habdsk.org'), (r.status_code, r.headers.get('location')))
        check('404 page', requests.get(WEB + '/no-such-page').status_code == 404)
        t = requests.get(WEB + '/robots.txt').text; check('robots disallows while private', 'Disallow: /' in t)
        for n in (2, 3, 4, 5): check('figure copy %d' % n, requests.get(WEB + '/figures/figure%d.png' % n).status_code == 200)
        check('nav has Contact Us linking /contact', 'href="/contact"' in requests.get(WEB + '/').text)
    finally:
        for p in (api, web): p.terminate()
        for p in (api, web):
            try: p.wait(10)
            except Exception: p.kill()
    for f in fails: print(f)
    print('smoke test: %d failure(s)' % len(fails)); return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
