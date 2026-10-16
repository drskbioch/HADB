"""Shared loaders for the HADB paper project. Reads only data_release/ (read-only copies of rc3 and the step 16 environment run)."""
from pathlib import Path
import numpy as np, pandas as pd
P = Path(__file__).resolve().parents[1]
REL, DER, WRK = P / 'data_release' / 'release', P / 'data_release' / 'derived', P / 'data_release' / 'work'
ELEMENTS = ['Ni', 'Mn', 'Zn', 'Co']
LABEL_ONLY = ['Cd', 'Se']
SRC_LABEL = {'block_b_label': 'HADB Block B (literature labels)', 'gei_xrf_taxon': 'Gei et al. 2020, XRF tables S2.1-S2.5', 'gei_literature_update': 'Gei et al. 2020, compiled lists S2.6-S2.7',
             'paper_table': 'Sabah and Queensland papers (tables)'}
CITATION_GBIF = 'GBIF.org (13 October 2026) GBIF Occurrence Download https://doi.org/10.15468/dl.kb25da'


def species_element():
    return pd.read_csv(REL / 'species_element.csv', dtype=str, keep_default_na=False)


def evidence(headline=False):
    E = pd.read_csv(REL / 'evidence.csv', dtype=str, keep_default_na=False)
    SE = species_element().drop_duplicates('wcvp_accepted_name').set_index('wcvp_accepted_name')
    E['species_level_name'] = E.species.map(SE.species_level_name); E['family'] = E.species.map(SE.family)
    E['headline'] = (E.suspect_source != 'Y') & (E.weakened != 'Y') & (E.citation_inferred != 'Y')
    return E[E.headline] if headline else E


def licence_class(s):
    s = s.lower()
    if 'by-nc-nd' in s: return 'CC BY-NC-ND'
    if 'by-nc' in s: return 'CC BY-NC'
    if 'cc by' in s: return 'CC BY'
    return 'not stated or unknown'


def counts(view='headline'):
    C = pd.read_csv(REL / 'counts.csv', keep_default_na=False)
    return C[C.view_label == view]


def count_of(C, element, tier, scope='all'):
    q = C[(C.element == element) & (C.best_tier == tier) & (C.scope == scope)]
    return int(q.unique_species.sum()) if len(q) else 0


def env():
    return pd.read_csv(DER / 'species_environment_summary.csv', keep_default_na=False, na_values=[''])


def env_ok():
    S = env(); return S[S.meets_20_cells == 'Y'].copy()


def split_elements(s):
    return [x.strip() for x in str(s).split(';') if x.strip()]


def env_facts():
    """numbers quoted in table notes and legends, computed from the record-level environment file (primary basis, native cells)"""
    R = pd.read_csv(WRK / 'records_environment_primary.csv.gz', low_memory=False); N = R[R.native_status == 'native']
    L = pd.read_csv(WRK / 'licence_split_by_licence.csv')
    return dict(n_cells=len(N), unc_null_pct=round(100 * N.unc_null.mean(), 1), ceiling_cells=int((N.bio12_raw == 65535).sum()), ceiling_coords=int(N[N.bio12_raw == 65535][['lat', 'lon']].drop_duplicates().shape[0]),
                n_species_requested=int(len(pd.read_csv(DER / 'species_environment_summary.csv', usecols=['accepted_name']))), records_all=int(L.records.sum()), records_non_nc=int(L[L.licence != 'CC_BY_NC_4_0'].records.sum()))
