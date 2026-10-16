"""Data access for the figure panels: reads only data_release/ (release rc3, environment run, work files). Aggregated data only reach the figures."""
import json
from functools import lru_cache
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
REL, DER, WRK = ROOT / 'data_release' / 'release', ROOT / 'data_release' / 'derived', ROOT / 'data_release' / 'work'
CORE = ['Ni', 'Mn', 'Zn', 'Co']
SIX = ['Ni', 'Mn', 'Zn', 'Co', 'Cd', 'Se']


def rel(p): return str(Path(p))


@lru_cache(None)
def evidence_all():
    E = pd.read_csv(REL / 'evidence.csv', dtype=str, keep_default_na=False)
    SE = pd.read_csv(REL / 'species_element.csv', dtype=str, keep_default_na=False).drop_duplicates('wcvp_accepted_name').set_index('wcvp_accepted_name')
    E['sp'] = E.species.map(SE.species_level_name); E['family'] = E.species.map(SE.family)
    E['headline'] = (E.suspect_source != 'Y') & (E.weakened != 'Y') & (E.citation_inferred != 'Y')
    return E


@lru_cache(None)
def evidence():
    E = evidence_all(); return E[E.headline].copy()


@lru_cache(None)
def species_tier():
    """best tier per species over all elements in the headline view"""
    E = evidence(); return E.groupby('sp').tier.min()


@lru_cache(None)
def pairs():
    """species x element pairs of the headline view: best tier and whether a hyperaccumulation-scope row exists"""
    E = evidence(); E = E.assign(hyp=(E.scope == 'hyperaccumulation'))
    return E.groupby(['sp', 'element']).agg(tier=('tier', 'min'), hyp=('hyp', 'max'), family=('family', 'first')).reset_index()


@lru_cache(None)
def env():
    return pd.read_csv(DER / 'species_environment_summary.csv', keep_default_na=False, na_values=[''])


@lru_cache(None)
def env_ok():
    S = env(); return S[S.meets_20_cells == 'Y'].copy()


def elements_of(s): return [x.strip() for x in str(s).split(';') if x.strip()]


@lru_cache(None)
def cells_all():
    """native cells of the primary basis (non-NC, cleaned, one per species per cell); aggregated by the panels"""
    R = pd.read_csv(WRK / 'records_environment_primary.csv.gz', low_memory=False)
    return R[R.native_status == 'native'].copy()


@lru_cache(None)
def cells_ok():
    S = env_ok(); R = cells_all(); return R[R.species_level_name.isin(set(S.accepted_name))].copy()


def species_by_element(S):
    """long table species x element (Ni, Mn, Zn, Co) from the environment summary"""
    rows = [(r.accepted_name, e) for r in S.itertuples() for e in elements_of(r.elements_in_hadb) if e in CORE]
    return pd.DataFrame(rows, columns=['sp', 'element'])


@lru_cache(None)
def flags():
    return pd.read_csv(WRK / 'records_flags_all.csv.gz', usecols=['species_level_name', 'licence', 'year', 'basisOfRecord', 'non_nc'], low_memory=False)


@lru_cache(None)
def region_names():
    g = json.loads((WRK / 'wgsrpd_level3.geojson').read_text(encoding='utf-8'))
    return {f['properties']['LEVEL3_COD']: f['properties']['LEVEL3_NAM'] for f in g['features']}


def counts_headline():
    C = pd.read_csv(REL / 'counts.csv', keep_default_na=False); return C[C.view_label == 'headline']


def n_of(C, element, tier, scope='all'):
    q = C[(C.element == element) & (C.best_tier == tier) & (C.scope == scope)].unique_species; return int(q.sum()) if len(q) else 0


def land():
    import geopandas as gpd, pyogrio
    p = Path(pyogrio.__file__).parent / 'tests' / 'fixtures' / 'naturalearth_lowres' / 'naturalearth_lowres.shp'
    return gpd.read_file(p)


def primary_element(elems):
    """one element per species for colouring: the first of Ni, Co, Mn, Zn present (stated rule)"""
    for e in ('Ni', 'Co', 'Mn', 'Zn'):
        if e in elems: return e
    return 'other'
