"""Tables 1-3 of the paper (manuscript/tables/Table1-3.csv, UTF-8 with BOM) and their notes. No hand-typed numbers: everything is computed from data_release/."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hadb_data as H
OUT = H.P / 'manuscript' / 'tables'; OUT.mkdir(parents=True, exist_ok=True)


def write(df, name, notes):
    df.to_csv(OUT / name, index=False, encoding='utf-8-sig', lineterminator='\n')
    (OUT / name.replace('.csv', '_notes.txt')).write_text('\n'.join(notes) + '\n', encoding='utf-8', newline='\n')


def table1():
    C = H.counts('headline'); rows = []
    for el in H.ELEMENTS + H.LABEL_ONLY:
        t1, t2 = H.count_of(C, el, 'T1'), H.count_of(C, el, 'T2')
        rows.append([el + ('' if el in H.ELEMENTS else ' (label-only)'), t1, t2, t1 + t2, H.count_of(C, el, 'T1', 'hyperaccumulation'), H.count_of(C, el, 'T2', 'hyperaccumulation'),
                     'Gei XRF, papers, literature labels' if el in H.ELEMENTS else 'Block B labels only'])
    t1, t2 = H.count_of(C, 'ALL_ELEMENTS', 'T1'), H.count_of(C, 'ALL_ELEMENTS', 'T2')
    rows.append(['All elements (unique species)', t1, t2, t1 + t2, H.count_of(C, 'ALL_ELEMENTS', 'T1', 'hyperaccumulation'), H.count_of(C, 'ALL_ELEMENTS', 'T2', 'hyperaccumulation'), 'a species counts once'])
    cols = ['Element', 'Species with best tier T1 (n)', 'Species with best tier T2 (n)', 'Species T1 + T2 (n)', 'T1 from hyperaccumulation-scope sources (n)', 'T2 from hyperaccumulation-scope sources (n)', 'Evidence basis']
    df = pd.DataFrame(rows, columns=cols)
    for c in cols[1:6]: df[c] = df[c].astype(int)
    notes = ['Table 1. Unique species (WCVP species-level names) per element by best evidence tier in the headline view of release rc3 (counts.csv, view_label = headline).',
             'Headline view: Block B included; evidence rows from the suspect source, rows printed as not confirmed (weakened) and rows with an inferred citation are left out.',
             'Best tier: T1 = taxon-level measurement tested against a threshold; T2 = literature label or compiled list; a species is counted once per element at its best tier (T2 column = species whose best tier is T2).',
             'Counts are not additive across elements: a species can appear for several elements; the last row counts each species once. Cd and Se have Block B labels only (tier T2). Elements outside Ni, Mn, Zn, Co, Cd and Se are tier T3 (label only) and are not shown.',
             'Hyperaccumulation scope: the source is a hyperaccumulator screen or species table, or an article whose title contains "hyperaccumulat". The scope is unknown for most Block B rows (see Supplementary Methods).']
    write(df, 'Table1.csv', notes); return df


def table2():
    E = H.evidence(headline=True); E['lic'] = E.source_license.map(H.licence_class); rows = []
    for et, lab in H.SRC_LABEL.items():
        g = E[E.evidence_type == et]; lc = g.lic.value_counts()
        rows.append([lab, 'evidence rows', len(g), g.species_level_name.nunique(), g.citation.nunique(), '; '.join('%s %d' % (k, v) for k, v in lc.items()), int((g.nc_derived == 'Y').sum())])
    L = pd.read_csv(H.WRK / 'licence_split_by_licence.csv'); nm = {'CC0_1_0': 'CC0 1.0', 'CC_BY_4_0': 'CC BY 4.0', 'CC_BY_NC_4_0': 'CC BY-NC 4.0'}
    for r in L.itertuples():
        rows.append(['GBIF occurrence download, records under ' + nm[r.licence], 'occurrence records', int(r.records), int(r.species), 'not applicable', nm[r.licence], int(r.records) if r.licence == 'CC_BY_NC_4_0' else 0])
    cols = ['Source', 'Kind', 'Rows or records (n)', 'Species (n)', 'Distinct citations (n)', 'Licence of the source (rows)', 'Non-commercial rows or records (n)']
    df = pd.DataFrame(rows, columns=cols)
    for c in (cols[2], cols[3], cols[6]): df[c] = df[c].astype(int)
    Eall = H.evidence(headline=False); F = H.env_facts()
    notes = ['Table 2. Sources of the evidence (headline view of rc3) and licences; GBIF occurrence records are listed by record licence.',
             'Evidence rows: headline view, %d of %d evidence rows in rc3; species = WCVP species-level names. Licence of the source is the licence recorded per row (Europe PMC licence field, PDF notice, or not stated); "not stated or unknown" means no licence was found, not that the source is unlicensed.' % (len(E), len(Eall)),
             'Non-commercial rows: evidence rows tagged nc_derived = Y; for GBIF, the CC BY-NC 4.0 records. GBIF labels the whole download CC BY-NC 4.0 because it contains non-commercial records.',
             'GBIF download: key 0023369-260928105237408; %d records, %d species requested (20 to 100,000 final-predicate records per species; GBIF backbone taxonomy, no checklistKey). Citation: %s.' % (int(L.records.sum()), F['n_species_requested'], H.CITATION_GBIF),
             'No licence has been chosen for the HADB release; see Supplementary S4 for the licences of all inputs.']
    write(df, 'Table2.csv', notes); return df


def table3():
    S = H.env_ok(); rows = []
    for el in H.ELEMENTS:
        g = S[S.elements_in_hadb.map(lambda s: el in H.split_elements(s))]
        def iqr(c, d):
            q = np.nanpercentile(g[c], [25, 75]); return '%s to %s' % (format(q[0], '.%df' % d), format(q[1], '.%df' % d))
        rows.append([el, len(g), format(g.bio1_median_C.median(), '.1f'), iqr('bio1_median_C', 1), format(g.bio12_median_mm.median(), '.0f'), iqr('bio12_median_mm', 0), format(g.ph_median.median(), '.2f'), iqr('ph_median', 2)])
    cols = ['Element', 'Species with 20 or more native cells (n)', 'Median of species medians, mean annual temperature bio1 (degrees C)', 'IQR across species, bio1 (degrees C)',
            'Median of species medians, annual precipitation bio12 (mm)', 'IQR across species, bio12 (mm)', 'Median of species medians, soil pH (water, 0-5 cm)', 'IQR across species, pH']
    df = pd.DataFrame(rows, columns=cols); df[cols[1]] = df[cols[1]].astype(int)
    n_all = len(H.env()); n_ok = len(S); F = H.env_facts()
    notes = ['Table 3. Climate and soil at the native occurrence cells of species with 20 or more native cells, by element (environment run, species_environment_summary.csv).',
             'Basis: non-NC GBIF records (CC0 and CC BY), cleaned, one record per species per CHELSA 30 arc-second cell, native in the WCVP distribution; %d of %d species have 20 or more native cells, the other %d are "insufficient records" and carry no statistics.' % (n_ok, n_all, n_all - n_ok),
             'Each species contributes its own median; the table gives the median and the interquartile range (25th to 75th percentile) of those species medians. A species with several elements counts under each element, so rows are not additive.',
             'bio1 and bio12: CHELSA V2.1 1981-2010 (bio12 is saturated at 6,553.5 mm at %d coordinates). pH: SoilGrids 2.0 phh2o 0-5 cm mean (stored x10, divided by 10). Ultramafic status was not assessed (the layers cover the Americas only) and is not tabulated.' % F['ceiling_coords'],
             'Cleaning did not test country capitals or institution coordinates; %.1f%% of the %d final native cells have no recorded coordinate uncertainty (kept, flagged). Occurrence sampling is uneven (New Caledonia, Sweden, Australia).' % (F['unc_null_pct'], F['n_cells'])]
    write(df, 'Table3.csv', notes); return df


if __name__ == '__main__':
    for f in (table1, table2, table3):
        d = f(); print(f.__name__, d.shape)
    print(pd.read_csv(OUT / 'Table1.csv', encoding='utf-8-sig').head(5).to_string())
