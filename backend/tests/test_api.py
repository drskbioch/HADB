"""API tests (pytest). Run from backend/:  python -m pytest -q"""
import hashlib, json, sqlite3, sys
from pathlib import Path
import pandas as pd
import pytest
from fastapi.testclient import TestClient

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B))
from app.main import create_app, settings  # noqa: E402

CFG = dict(settings()); CFG['cors'] = ['https://hadb.example.org']
client = TestClient(create_app(CFG))
R = B.parent / 'data_release'


def test_health():
    r = client.get('/api/v1/health'); assert r.status_code == 200 and r.json()['status'] == 'ok' and r.json()['species'] > 900


def test_filter_counts_equal_release_counts():
    C = pd.read_csv(R / 'release/counts.csv', keep_default_na=False); C = C[(C.view_label == 'headline') & (C.scope == 'all')]
    for el in ('Ni', 'Mn', 'Zn', 'Co'):
        for t in ('T1', 'T2'):
            want = int(C[(C.element == el) & (C.best_tier == t)].unique_species.sum()); got = client.get('/api/v1/species', params=dict(element=el, tier=t, page_size=1)).json()['total']
            assert got == want, (el, t, got, want)


def test_pagination_limits():
    assert client.get('/api/v1/species', params=dict(page_size=101)).status_code == 422
    assert client.get('/api/v1/species', params=dict(page=0)).status_code == 422
    j = client.get('/api/v1/species', params=dict(page_size=100, page=2)).json(); assert len(j['items']) == 100 and j['page'] == 2


@pytest.mark.parametrize('params', [dict(q="' OR 1=1 --"), dict(q='a%'), dict(q='x_y'), dict(element="Ni';DROP TABLE species;--"), dict(element='nickel'), dict(tier='T9'), dict(scope='x'), dict(family="x'; DROP TABLE species;--"),
                                    dict(genus='a/../b'), dict(rank='root')])
def test_injection_and_bad_input_are_rejected_or_harmless(params):
    r = client.get('/api/v1/species', params=params)
    assert r.status_code in (200, 422)
    if r.status_code == 200: assert r.json()['total'] == 0
    assert client.get('/api/v1/health').json()['species'] > 900          # tables still there


def test_species_detail_and_public_scope():
    s = client.get('/api/v1/species', params=dict(q='Noccaea caerulescens')).json()['items']; assert s
    d = client.get('/api/v1/species/%d' % s[0]['species_id']).json()
    assert d['environment_status'] == 'ok' and d['environment']['n_cells'] >= 20 and d['ultramafic'] == 'not assessed (no coverage outside the Americas)'
    assert d['evidence'] and d['elements'] and 'GBIF.org' in d['occurrence_citation']
    txt = json.dumps(d).lower()
    for bad in ('decimallatitude', 'decimallongitude', '"lat"', '"lon"', 'concentration', 'mg/kg', 'ug/g'): assert bad not in txt
    assert not any(k.startswith('ultramafic_') for k in d['environment'])


def test_not_found_and_validation():
    assert client.get('/api/v1/species/999999999').status_code == 404
    assert client.get('/api/v1/species/0').status_code == 422
    assert client.get('/api/v1/species/abc').status_code == 422


def test_insufficient_records_status():
    con = sqlite3.connect('file:%s?mode=ro' % Path(CFG['db']).as_posix(), uri=True); sid = con.execute("SELECT species_id FROM species WHERE env_status = 'insufficient records' LIMIT 1").fetchone()[0]; con.close()
    d = client.get('/api/v1/species/%d' % sid).json(); assert d['environment'] is None and d['environment_status'].startswith('insufficient records')


def test_security_headers():
    r = client.get('/api/v1/health'); h = r.headers
    assert h['x-content-type-options'] == 'nosniff' and h['x-frame-options'] == 'DENY' and 'frame-ancestors' in h['content-security-policy'] and h['referrer-policy'] == 'no-referrer'
    assert 'strict-transport-security' in client.get('/api/v1/health', headers={'x-forwarded-proto': 'https'}).headers


def test_cors_allowlist():
    ok = client.get('/api/v1/health', headers={'Origin': 'https://hadb.example.org'}); assert ok.headers.get('access-control-allow-origin') == 'https://hadb.example.org'
    no = client.get('/api/v1/health', headers={'Origin': 'https://evil.example.com'}); assert 'access-control-allow-origin' not in no.headers
    nocfg = TestClient(create_app(dict(CFG, cors=[]))).get('/api/v1/health', headers={'Origin': 'https://hadb.example.org'}); assert 'access-control-allow-origin' not in nocfg.headers


def test_downloads_hash_and_whitelist():
    lst = client.get('/api/v1/downloads').json()['items']; assert lst and all(len(i['sha256']) == 64 for i in lst)
    it = lst[0]; r = client.get('/api/v1/downloads/' + it['name']); assert r.status_code == 200 and hashlib.sha256(r.content).hexdigest().upper() == it['sha256']
    assert client.get('/api/v1/downloads/..%2F..%2Fhadb.sqlite').status_code in (404, 422); assert client.get('/api/v1/downloads/hadb.sqlite').status_code == 404
    assert not any(i['name'].endswith(('.zip', '.sqlite')) for i in lst)


def test_elements_stats_versions():
    el = {e['element']: e for e in client.get('/api/v1/elements').json()['items']}; assert el['Ni']['t1_headline'] == 211
    st = client.get('/api/v1/stats').json(); assert st['species_with_environment'] == 198 and st['headline_counts']
    v = client.get('/api/v1/versions').json(); assert v['gbif_doi'] == '10.15468/dl.kb25da' and v['release_licence'] == 'TBC' and len(v['rc3_manifest_sha256']) == 64


def test_database_is_read_only_and_openapi_valid():
    con = sqlite3.connect('file:%s?mode=ro' % Path(CFG['db']).as_posix(), uri=True)
    with pytest.raises(sqlite3.OperationalError): con.execute('INSERT INTO versions VALUES (?, ?)', ('x', 'y'))
    con.close(); o = client.get('/api/v1/openapi.json').json(); assert o['openapi'].startswith('3') and '/api/v1/species/{wcvp_id}' in o['paths'] and client.get('/docs').status_code == 404
