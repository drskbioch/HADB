"""HADB public API (read-only). FastAPI, SQLite opened read-only, parameterised queries, validated input, security headers, CORS allowlist.
Public scope: species, element, class, tier, scope, citations, names, environment summaries. No concentration values, no GBIF points or coordinates."""
import json, os, sqlite3
from pathlib import Path
from typing import Annotated, Literal, Optional
from fastapi import FastAPI, HTTPException, Path as PathParam, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

HERE = Path(__file__).resolve().parents[1]
Tier = Literal['T1', 'T2', 'T3']
Scope = Literal['hyperaccumulation', 'phytoremediation', 'biosorbent', 'other', 'mixed', 'unknown']
Rank = Literal['species', 'infraspecific']
View = Literal['headline', 'all']
Element = Annotated[str, Query(pattern=r'^[A-Z][a-z]?$', description='chemical symbol, e.g. Ni')]
TextQ = Annotated[str, Query(min_length=2, max_length=80, pattern=r'^[^\x00-\x1f%_\\]+$', description='name search (no wildcards)')]
NameQ = Annotated[str, Query(min_length=2, max_length=60, pattern=r'^[A-Za-z×][A-Za-z× \-]*$')]
UNLICENSED = 'Release licence: CC BY 4.0; see /api/v1/versions.'
ULTRAMAFIC = 'not assessed (no coverage outside the Americas)'
INSUFFICIENT = 'insufficient records (fewer than 20 native cells; no environment statistics)'
CORE = ['Ni', 'Mn', 'Zn', 'Co', 'Cd', 'Se']


def settings():
    return dict(db=os.environ.get('HADB_DB_PATH') or str(HERE / 'data' / 'hadb.sqlite'), downloads=os.environ.get('HADB_DOWNLOADS_DIR') or str(HERE / 'data' / 'downloads'),
                cors=[o.strip() for o in (os.environ.get('HADB_CORS_ORIGINS') or 'https://hadb.habdsk.org').split(',') if o.strip()])


def create_app(cfg: Optional[dict] = None) -> FastAPI:
    cfg = cfg or settings()
    app = FastAPI(title='HADB API', version='1.0.0', docs_url=None, redoc_url=None, openapi_url='/api/v1/openapi.json',
                  description='Read-only API of the Hyperaccumulator Database (HADB v1). ' + UNLICENSED)
    if cfg['cors']:
        app.add_middleware(CORSMiddleware, allow_origins=cfg['cors'], allow_methods=['GET'], allow_headers=[], allow_credentials=False, max_age=600)

    @app.middleware('http')
    async def _debug(request: Request, call_next):  # TEMPORARY DIAGNOSTIC, remove after the Vercel routing is fixed
        if '__debug' in request.url.query:
            return JSONResponse({'path': request.scope['path'], 'raw_path': (request.scope.get('raw_path') or b'').decode(), 'root_path': request.scope.get('root_path'), 'url': str(request.url), 'headers': dict(request.headers)})
        return await call_next(request)

    @app.middleware('http')
    async def headers(request: Request, call_next):
        r = await call_next(request)
        r.headers.update({'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY', 'Referrer-Policy': 'no-referrer', 'Content-Security-Policy': "default-src 'none'; frame-ancestors 'none'",
                          'Permissions-Policy': 'geolocation=(), camera=(), microphone=()', 'Cross-Origin-Resource-Policy': 'same-site'})
        if request.headers.get('x-forwarded-proto') == 'https': r.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        if request.method == 'GET' and r.status_code == 200 and 'Cache-Control' not in r.headers: r.headers['Cache-Control'] = 'public, max-age=300'
        return r

    @app.exception_handler(sqlite3.Error)
    async def db_error(request, exc):
        return JSONResponse({'detail': 'database error'}, status_code=500)

    def q(sql, params=()):
        con = sqlite3.connect('file:%s?mode=ro' % Path(cfg['db']).as_posix(), uri=True)
        con.row_factory = sqlite3.Row
        try: return [dict(r) for r in con.execute(sql, params).fetchall()]
        finally: con.close()

    def split(s): return [x for x in (s or '').split(',') if x]

    @app.get('/api/v1/health')
    def health():
        n = q('SELECT COUNT(*) AS n FROM species')[0]['n']; return {'status': 'ok', 'species': n}

    @app.get('/api/v1/species')
    def species(q_: Annotated[Optional[str], Query(alias='q', min_length=2, max_length=80, pattern=r'^[^\x00-\x1f%_\\]+$')] = None, element: Annotated[Optional[str], Query(pattern=r'^[A-Z][a-z]?$')] = None,
                tier: Optional[Tier] = None, scope: Optional[Scope] = None, family: Optional[NameQ] = None, genus: Optional[NameQ] = None, rank: Optional[Rank] = None, view: View = 'headline',
                page: Annotated[int, Query(ge=1, le=100000)] = 1, page_size: Annotated[int, Query(ge=1, le=100)] = 25):
        sfx = 'headline' if view == 'headline' else 'all'; where, par = [], []
        if view == 'headline': where.append('s.in_headline = 1')
        if q_: where.append("s.search_text LIKE ? ESCAPE '\\'"); par.append('%' + q_.lower() + '%')
        if family: where.append('s.family = ?'); par.append(family)
        if genus: where.append('s.genus = ?'); par.append(genus)
        if rank: where.append('s.rank = ?'); par.append(rank)
        if tier and not element and not scope: where.append('s.best_tier_%s = ?' % sfx); par.append(tier)
        if element or scope:
            sub = ['e.species_id = s.species_id']
            if element: sub.append('e.element = ?'); par.append(element)
            if tier: sub.append('e.best_tier_%s = ?' % sfx); par.append(tier)
            if scope: sub.append('e.scope_%s = ?' % sfx); par.append(scope)
            if view == 'headline': sub.append('e.in_headline = 1')
            where.append('EXISTS (SELECT 1 FROM species_element e WHERE ' + ' AND '.join(sub) + ')')
        w = (' WHERE ' + ' AND '.join(where)) if where else ''
        total = q('SELECT COUNT(*) AS n FROM species s' + w, par)[0]['n']
        rows = q('SELECT s.species_id, s.name, s.family, s.genus, s.rank, s.best_tier_%s AS best_tier, s.elements_%s AS elements, s.n_evidence_%s AS n_evidence, s.env_status FROM species s%s ORDER BY s.name LIMIT ? OFFSET ?' % (sfx, sfx, sfx, w),
                 par + [page_size, (page - 1) * page_size])
        for r in rows: r['elements'] = split(r['elements'])
        return {'total': total, 'page': page, 'page_size': page_size, 'view': view, 'items': rows, 'licence': UNLICENSED}

    @app.get('/api/v1/species/{wcvp_id}')
    def species_detail(wcvp_id: Annotated[int, PathParam(ge=1, le=10**9)]):
        s = q('SELECT * FROM species WHERE species_id = ?', [wcvp_id])
        if not s: raise HTTPException(404, 'species not found')
        s = s[0]; s['taxa'] = json.loads(s['taxa']); s['names_published'] = [n for n in s['names_published'].split(' ; ') if n]; del s['search_text']
        s['elements'] = q('SELECT element, best_tier_headline, best_tier_all, class_headline, class_all, threshold_class_headline, threshold_class_all, scope_headline, scope_all, n_evidence_headline, n_evidence_all, in_headline FROM species_element WHERE species_id = ? ORDER BY best_tier_all, element', [wcvp_id])
        s['evidence'] = q('SELECT evidence_id, taxon_name, element, evidence_type, tier, scope, citation, doi, class, threshold_class, weakened, suspect_source, citation_inferred, citation_note, name_as_published, source_license, headline FROM evidence WHERE species_id = ? ORDER BY element, tier, evidence_id LIMIT 1000', [wcvp_id])
        env = q('SELECT * FROM environment_summary WHERE species_id = ?', [wcvp_id])
        s['environment'] = env[0] if env else None
        s['environment_status'] = 'ok' if env else (INSUFFICIENT if s['env_status'] == 'insufficient records' else 'not in the occurrence set')
        s['ultramafic'] = ULTRAMAFIC; s['occurrence_citation'] = q("SELECT value FROM versions WHERE key = 'gbif_citation'")[0]['value']; s['licence'] = UNLICENSED
        return s

    @app.get('/api/v1/elements')
    def elements():
        rows = q("SELECT element, COUNT(*) AS species_all, SUM(in_headline) AS species_headline, SUM(best_tier_headline = 'T1') AS t1_headline, SUM(best_tier_headline = 'T2') AS t2_headline, SUM(best_tier_headline = 'T3') AS t3_headline FROM species_element GROUP BY element")
        rows.sort(key=lambda r: (CORE.index(r['element']) if r['element'] in CORE else 99, -(r['species_headline'] or 0))); return {'items': rows}

    @app.get('/api/v1/families')
    def families(page: Annotated[int, Query(ge=1)] = 1, page_size: Annotated[int, Query(ge=1, le=100)] = 50):
        n = q('SELECT COUNT(DISTINCT family) AS n FROM species')[0]['n']
        rows = q('SELECT family, COUNT(*) AS species, SUM(in_headline) AS species_headline FROM species GROUP BY family ORDER BY species DESC, family LIMIT ? OFFSET ?', [page_size, (page - 1) * page_size]); return {'total': n, 'items': rows}

    @app.get('/api/v1/stats')
    def stats():
        v = {r['key']: r['value'] for r in q('SELECT key, value FROM versions')}
        c = q("SELECT element, best_tier, scope, unique_species FROM counts WHERE view_label = 'headline' AND scope IN ('all', 'hyperaccumulation') AND best_tier IN ('T1', 'T2', 'T3')")
        tot = q('SELECT COUNT(*) AS n, SUM(in_headline) AS h, SUM(env_status = ?) AS e FROM species', ['ok'])[0]
        return {'species': tot['n'], 'species_headline': tot['h'], 'species_with_environment': tot['e'], 'headline_counts': c, 'versions': v}

    @app.get('/api/v1/versions')
    def versions():
        return {r['key']: r['value'] for r in q('SELECT key, value FROM versions')}

    def manifest():
        p = Path(cfg['downloads']) / 'downloads_manifest.json'
        return json.loads(p.read_text(encoding='utf-8')) if p.exists() else []

    @app.get('/api/v1/downloads')
    def downloads():
        return {'licence': UNLICENSED, 'zenodo_doi': 'to be added', 'items': manifest()}

    @app.get('/api/v1/downloads/{name}')
    def download(name: Annotated[str, PathParam(pattern=r'^[A-Za-z0-9_.\-]{1,100}$')]):
        item = next((m for m in manifest() if m['name'] == name), None)
        if not item: raise HTTPException(404, 'file not found')
        return FileResponse(Path(cfg['downloads']) / name, filename=name, headers={'X-SHA256': item['sha256']})

    return app


app = create_app()
