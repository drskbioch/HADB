"""Phase 1 checks: every number in Tables 1-3 equals counts.csv or the environment summary (recomputed here by a separate route); formats."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
P = Path(__file__).resolve().parents[1]
T = P / 'manuscript' / 'tables'; R = P / 'data_release'
fails = []


def check(name, ok):
    if not ok: fails.append(name)


def rd(n): return pd.read_csv(T / n, encoding='utf-8-sig', dtype=str, keep_default_na=False)


C = pd.read_csv(R / 'release' / 'counts.csv', keep_default_na=False); C = C[C.view_label == 'headline']
def cnt(el, t, sc='all'):
    q = C[(C.element == el) & (C.best_tier == t) & (C.scope == sc)].unique_species; return int(q.sum()) if len(q) else 0
t1 = rd('Table1.csv')
for r in t1.itertuples(index=False):
    el = r[0].split(' ')[0] if not r[0].startswith('All') else 'ALL_ELEMENTS'
    check('T1 %s T1' % el, int(r[1]) == cnt(el, 'T1')); check('T1 %s T2' % el, int(r[2]) == cnt(el, 'T2')); check('T1 %s sum' % el, int(r[3]) == cnt(el, 'T1') + cnt(el, 'T2'))
    check('T1 %s hyp T1' % el, int(r[4]) == cnt(el, 'T1', 'hyperaccumulation')); check('T1 %s hyp T2' % el, int(r[5]) == cnt(el, 'T2', 'hyperaccumulation'))
E = pd.read_csv(R / 'release' / 'evidence.csv', dtype=str, keep_default_na=False)
SE = pd.read_csv(R / 'release' / 'species_element.csv', dtype=str, keep_default_na=False).drop_duplicates('wcvp_accepted_name').set_index('wcvp_accepted_name').species_level_name
E['sp'] = E.species.map(SE); E = E[(E.suspect_source != 'Y') & (E.weakened != 'Y') & (E.citation_inferred != 'Y')]
t2 = rd('Table2.csv')
for et, lab in (('block_b_label', 'HADB Block B (literature labels)'), ('gei_xrf_taxon', 'Gei et al. 2020, XRF tables S2.1-S2.5'), ('gei_literature_update', 'Gei et al. 2020, compiled lists S2.6-S2.7'), ('paper_table', 'Sabah and Queensland papers (tables)')):
    g = E[E.evidence_type == et]; r = t2[t2.Source == lab].iloc[0]
    check('T2 ' + et, int(r.iloc[2]) == len(g) and int(r.iloc[3]) == g.sp.nunique() and int(r.iloc[4]) == g.citation.nunique() and int(r.iloc[6]) == int((g.nc_derived == 'Y').sum()))
L = pd.read_csv(R / 'work' / 'licence_split_by_licence.csv')
for r in L.itertuples():
    row = t2[t2.Source.str.endswith({'CC0_1_0': 'CC0 1.0', 'CC_BY_4_0': 'CC BY 4.0', 'CC_BY_NC_4_0': 'CC BY-NC 4.0'}[r.licence])]
    check('T2 gbif ' + r.licence, len(row) == 1 and int(row.iloc[0, 2]) == r.records and int(row.iloc[0, 3]) == r.species)
S = pd.read_csv(R / 'derived' / 'species_environment_summary.csv', keep_default_na=False, na_values=['']); S = S[S.meets_20_cells == 'Y']
t3 = rd('Table3.csv')
for r in t3.itertuples(index=False):
    g = S[S.elements_in_hadb.map(lambda s: r[0] in [x.strip() for x in str(s).split(';')])]
    q = lambda c, d: format(float(g[c].median()), '.%df' % d)
    iq = lambda c, d: ' to '.join(format(float(v), '.%df' % d) for v in np.nanpercentile(g[c], [25, 75]))
    check('T3 %s n' % r[0], int(r[1]) == len(g)); check('T3 %s bio1' % r[0], r[2] == q('bio1_median_C', 1) and r[3] == iq('bio1_median_C', 1))
    check('T3 %s bio12' % r[0], r[4] == q('bio12_median_mm', 0) and r[5] == iq('bio12_median_mm', 0)); check('T3 %s pH' % r[0], r[6] == q('ph_median', 2) and r[7] == iq('ph_median', 2))
for n in ('Table1', 'Table2', 'Table3'):
    raw = (T / (n + '.csv')).read_bytes(); check(n + ' BOM', raw[:3] == b'\xef\xbb\xbf'); txt = raw.decode('utf-8-sig')
    import re
    check(n + ' no scientific notation', not re.search(r'\d[eE][+-]?\d', txt.split('\n', 1)[1])); check(n + ' <= 8 columns', len(rd(n + '.csv').columns) <= 8); check(n + ' notes', (T / (n + '_notes.txt')).exists())
check('no ultramafic column in Table3', not any('ltramafic' in c for c in t3.columns))
sup = P / 'manuscript' / 'supplementary'
for f in ('S1_species_element.csv', 'S2_evidence.csv', 'S3_names_and_exclusions.xlsx', 'S4_sources_licences_new_vs_known.xlsx', 'S5_Supplementary_Methods_and_Limitations.docx'):
    check('exists ' + f, (sup / f).exists() and (sup / f).stat().st_size > 1000)
S2 = pd.read_csv(sup / 'S2_evidence.csv', encoding='utf-8-sig', nrows=1); check('S2 has no concentration column', not any(c in S2.columns for c in ('max_concentration', 'concentration', 'value_ug_g')))
for f in fails: print('FAIL', f)
print('table tests: %d failure(s)' % len(fails)); sys.exit(1 if fails else 0)
