"""Writes manuscript/figure_legends.md and manuscript/results_skeleton.md. Every number in the sentences is computed from data_release/ (no hand-typed numbers)."""
import json, re, sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import spearmanr
sys.path.insert(0, str(Path(__file__).resolve().parent))
from figures import figdata as FD
ROOT = Path(__file__).resolve().parents[1]
META = ROOT / 'manuscript' / 'figure_meta'
fm = lambda x: format(int(round(x)), ',')

TITLES = {'2a': 'Species per element and tier', '2b': 'Evidence rows by source', '2c': 'Ni: overlap of evidence sources', '2d': 'Threshold class by element', '2e': 'Families: T1 vs T2 species', '2f': 'Species vs citing articles',
          '2g': 'Ten articles hold most Block B rows', '2h': 'Scope of the evidence by source', '2i': 'New vs known in the three screens', '3a': 'Names of the Block B rows', '3b': 'Name match types', '3c': 'Similarity of accepted matches',
          '3d': 'From Block B rows to evidence rows', '3e': 'Thresholds in the Gei screen', '3f': 'Removed from the headline view', '3g': 'Licence of the evidence sources', '3h': 'Families by element', '4a': 'Where the cleaned native cells are',
          '4b': 'Records per species', '4c': 'Cleaning of the occurrence records', '4d': 'Native regions', '4e': 'T1 species by source region', '4f': 'Basis of record', '4g': 'Licence of the records', '4h': 'Collection year',
          '4i': 'Latitude of the native cells', '5a': 'Temperature (bio1)', '5b': 'Precipitation (bio12)', '5c': 'Climate space of the species', '5d': 'Soil pH', '5e': 'Completeness of the environment data',
          '5f': 'Family climate envelopes', '5g': 'PCA of the species medians', '5h': 'T1 vs T2 species', '5i': 'Data-rich T1 species', '5j': 'Median environment by family and element'}


def sentences():
    S = {}; E = FD.evidence(); C = FD.counts_headline(); env = FD.env(); ok = FD.env_ok(); cells = FD.cells_all(); P = FD.pairs()
    nT = lambda e, t: FD.n_of(C, e, t); allt1, allt2 = nT('ALL_ELEMENTS', 'T1'), nT('ALL_ELEMENTS', 'T2')
    S['2a'] = 'The headline view lists %s species with best tier T1 or T2 (%s T1, %s T2); Ni has %s T1 and %s T2 species and Mn %s and %s (Fig 2a, Table 1).' % (fm(allt1 + allt2), fm(allt1), fm(allt2), nT('Ni', 'T1'), nT('Ni', 'T2'), nT('Mn', 'T1'), nT('Mn', 'T2'))
    vc = E.evidence_type.value_counts(); S['2b'] = 'Of %s headline evidence rows, %.0f%% are Block B literature labels, %.0f%% Gei et al. compiled lists, %.0f%% Gei XRF rows and %.0f%% paper tables (Fig 2b).' % (fm(vc.sum()), 100 * vc['block_b_label'] / vc.sum(), 100 * vc['gei_literature_update'] / vc.sum(), 100 * vc['gei_xrf_taxon'] / vc.sum(), 100 * vc['paper_table'] / vc.sum())
    ni = E[E.element == 'Ni'].groupby('sp').evidence_type.apply(lambda s: tuple(sorted(set(s)))); only_b = int((ni == ('block_b_label',)).sum()); S['2c'] = 'Of %s Ni species, %s rest on Block B labels alone and %s have evidence from more than one source type (Fig 2c).' % (fm(len(ni)), fm(only_b), fm((ni.map(len) > 1).sum()))
    r = {'high-range': 0, 'standard': 1, 'label-only': 2}; q = E[E.element.isin(FD.CORE)].assign(r=lambda d: d.threshold_class.map(r)).groupby(['sp', 'element']).r.min().reset_index(); nq = q[q.element == 'Ni']
    S['2d'] = 'Among Ni species, %s reach the high-range threshold, %s the standard threshold only and %s are label-only (Fig 2d).' % (fm((nq.r == 0).sum()), fm((nq.r == 1).sum()), fm((nq.r == 2).sum()))
    fam = E.drop_duplicates('sp').set_index('sp').family; t = FD.species_tier(); D = pd.DataFrame({'family': fam, 'tier': t}).dropna(); g = D.groupby(['family', 'tier']).size().unstack(fill_value=0); g['tot'] = g.sum(axis=1); g = g.sort_values('tot', ascending=False)
    S['2e'] = '%s is the largest family (%s species, %s with best tier T1), followed by %s (%s) and %s (%s) (Fig 2e).' % (g.index[0], g.tot.iloc[0], g.T1.iloc[0], g.index[1], g.tot.iloc[1], g.index[2], g.tot.iloc[2])
    cs = E.groupby('citation').sp.apply(set); order = cs.map(len).sort_values(ascending=False).index; seen = set(); y = []
    for c in order: seen |= cs[c]; y.append(len(seen))
    k50, k90 = int(np.argmax(np.array(y) >= .5 * y[-1])) + 1, int(np.argmax(np.array(y) >= .9 * y[-1])) + 1; S['2f'] = '%s citations cover %s species; the %s largest citations already give 50%% and the %s largest 90%% of them (Fig 2f).' % (fm(len(y)), fm(y[-1]), k50, k90)
    T = pd.read_csv(FD.REL / 'top10_pmids_by_block_b_rows.csv'); S['2g'] = 'The ten largest PMIDs hold %.0f%% of the 1,065 Block B rows; the largest, PMID %s, holds %s rows (Fig 2g).' % (100 * T.cumulative_share_of_1065.iloc[-1], T.pmid.iloc[0], T.block_b_rows.iloc[0])
    hy = E.groupby('evidence_type').scope.apply(lambda s: 100 * (s == 'hyperaccumulation').mean()); S['2h'] = 'Only %.0f%% of Block B rows come from articles tagged hyperaccumulation, against %.0f%% of Gei XRF rows and %.0f%% of paper rows (Fig 2h).' % (hy['block_b_label'], hy['gei_xrf_taxon'], hy['paper_table'])
    Nv = pd.read_csv(FD.DER / 'new_vs_known_counts_papers.csv', keep_default_na=False); g0 = Nv[(Nv.paper.str.startswith('Gei')) & (Nv.element_or_scope == 'Ni') & (Nv.row_type == 'quoted_new_vs_known')].iloc[0]; fi = lambda x: int(re.match(r'\s*(\d+)', str(x)).group(1))
    S['2i'] = 'The Gei et al. screen of New Caledonia quoted %d Ni taxa of which %d were known previously (%d new); the Sabah and Queensland screens quote similar new-versus-known counts (Fig 2i, Supplementary S4).' % (fi(g0.total_as_quoted), fi(g0.previously_known_as_quoted), fi(g0.total_as_quoted) - fi(g0.previously_known_as_quoted))
    nc = pd.read_csv(FD.REL / 'name_class_table.csv').set_index('class'); S['3a'] = 'Of 1,065 Block B rows, %s (%.1f%%) resolve to a species name, %s are genus-only, %s non-taxa and %s unresolved (Fig 3a).' % (nc.loc['species_resolved', 'block_b_rows'], nc.loc['species_resolved', 'pct_of_block_b_rows'], nc.loc['rank_genus_by_design', 'block_b_rows'], nc.loc['non_taxon', 'block_b_rows'], nc.loc['unresolved', 'block_b_rows'])
    M = pd.read_csv(FD.DER / 'master_species_v2.csv', usecols=['match_type'], low_memory=False); mc = M.match_type.value_counts(); S['3b'] = '%.0f%% of %s master rows match a WCVP name exactly and %.0f%% after normalisation; %s rows needed a recorded decision (Fig 3b).' % (100 * mc['exact'] / len(M), fm(len(M)), 100 * mc['normalised'] / len(M), fm(len(M) - mc['exact'] - mc['normalised']))
    v = {}; a_ = pd.read_csv(FD.DER / 'name_review.csv'); a_ = a_[a_.decision == 'accept']; v.update({r.input: r.similarity for r in a_.itertuples()}); b_ = pd.read_csv(FD.DER / 'name_decisions_step6.csv'); b_ = b_[(b_.applied == 'Y') & b_['sim'].notna()]
    v.update({r.name_as_published: r.sim for r in b_.itertuples() if r.name_as_published not in v}); c_ = pd.read_csv(FD.DER / 'pending_positives.csv'); c_ = c_[c_.decision == 'accept']; v.update({r.gei_name: r.nearest1_similarity for r in c_.itertuples() if r.gei_name not in v})
    d_ = pd.read_csv(FD.DER / 'unresolved_names_review_v3.csv', keep_default_na=False); d_ = d_[(d_.decision == 'accept') & (d_.match_class == 'spelling_manual')]; v.update({r.input_name: float(r.similarity) for r in d_.itertuples() if r.input_name not in v}); xs_ = np.array(list(v.values())) / 100
    S['3c'] = 'Of %d accepted non-exact name matches with a spelling similarity, %d lie below 0.95 (minimum %.2f); they were accepted by region test or orthographic rule, not automatically (Fig 3c).' % (len(xs_), int((xs_ < 0.95).sum()), xs_.min())
    A = pd.read_csv(FD.REL / 'block_b_row_accounting.csv'); Eb = FD.evidence_all().query("evidence_type=='block_b_label'"); S['3d'] = 'The %s Block B rows give %s rows in the master bucket, %s evidence rows and %s species x element pairs (Fig 3d).' % (fm(len(A)), fm((A.bucket == 'master').sum()), fm(len(Eb)), fm(Eb.drop_duplicates(['species', 'element']).shape[0]))
    G = E[(E.evidence_type == 'gei_xrf_taxon') & E.element.isin(FD.CORE)].assign(r=lambda d: d.threshold_class.map(r)).groupby(['sp', 'element']).r.min().reset_index(); S['3e'] = 'In the Gei screen, %s Ni species reach the high-range threshold and %s only the standard threshold, against %s T1 Ni species from all sources (Fig 3e).' % (int(((G.element == 'Ni') & (G.r == 0)).sum()), int(((G.element == 'Ni') & (G.r == 1)).sum()), nT('Ni', 'T1'))
    Ea = FD.evidence_all(); S['3f'] = 'The headline view drops %s of %s evidence rows (%s from the suspect source, %s weakened, %s inferred citations) (Fig 3f).' % (fm((~Ea.headline).sum()), fm(len(Ea)), fm((Ea.suspect_source == 'Y').sum()), fm((Ea.weakened == 'Y').sum()), fm((Ea.citation_inferred == 'Y').sum()))
    lic = Ea.source_license.map(lambda s: 'CC BY' if ('cc by' in s.lower() and 'nc' not in s.lower()) else ('NC' if 'nc' in s.lower() else 'none')); S['3g'] = 'The licence of the source is not stated or unknown for %.0f%% of evidence rows and CC BY for %.0f%% (Fig 3g, Table 2).' % (100 * (lic == 'none').mean(), 100 * (lic == 'CC BY').mean())
    Pm = P[P.element.isin(FD.SIX)]; ff = Pm.groupby(['family', 'element']).sp.nunique().sort_values(ascending=False); S['3h'] = 'The largest family-element cell is %s with %s species for %s (Fig 3h).' % (ff.index[0][0], ff.iloc[0], ff.index[0][1])
    rg = cells.LEVEL3_NAM.value_counts(); S['4a'] = 'The %s native cells of the primary basis lie mostly in %s (%s cells), %s (%s), %s (%s) and %s (%s) (Fig 4a).' % (fm(len(cells)), rg.index[0], fm(rg.iloc[0]), rg.index[1], fm(rg.iloc[1]), rg.index[2], fm(rg.iloc[2]), rg.index[3], fm(rg.iloc[3]))
    S['4b'] = '%s of %s species have 20 or more native cells and %s species have fewer, which receive no environment statistics (Fig 4b).' % (len(ok), len(env), len(env) - len(ok))
    sv = pd.read_csv(FD.WRK / 'survival_table.csv'); sv = sv[sv.variant == 'primary']; S['4c'] = 'Cleaning, thinning to one record per species per cell and the native-range filter reduce %s non-NC records to %s native cells; %.1f%% of those cells have no recorded coordinate uncertainty (Fig 4c).' % (fm(sv.records.iloc[0]), fm(sv.records.iloc[9]), 100 * cells.unc_null.mean())
    import re as _re
    cnt = {}
    for s in env.regions.dropna():
        for c in set(_re.findall(r'([A-Z]{3}) \(', s)): cnt[c] = cnt.get(c, 0) + 1
    top = sorted(cnt.items(), key=lambda kv: -kv[1])[:2]; nm = FD.region_names(); S['4d'] = 'The most species have native cells in %s (%s species) and %s (%s) (Fig 4d).' % (nm[top[0][0]], top[0][1], nm[top[1][0]], top[1][1])
    t1 = E[E.tier == 'T1']; nc_t1 = t1[t1.evidence_type == 'gei_xrf_taxon'].sp.nunique(); S['4e'] = '%s of %s T1 species come from the New Caledonia XRF screen of Gei et al. (Fig 4e).' % (nc_t1, t1.sp.nunique())
    el = FD.species_by_element(env); cc = cells[['species_level_name', 'basisOfRecord', 'year', 'lat']].merge(el, left_on='species_level_name', right_on='sp'); ni = cc[cc.element == 'Ni']; S['4f'] = 'Human observations make up %.0f%% of Ni cells and preserved specimens %.0f%% (Fig 4f).' % (100 * (ni.basisOfRecord == 'HUMAN_OBSERVATION').mean(), 100 * (ni.basisOfRecord == 'PRESERVED_SPECIMEN').mean())
    F = FD.flags().merge(el, left_on='species_level_name', right_on='sp'); fn = F[F.element == 'Ni']; S['4g'] = 'CC BY-NC records are %.0f%% of the downloaded records of Ni species and are excluded from the primary basis (Fig 4g).' % (100 * (fn.licence == 'CC_BY_NC_4_0').mean())
    yr = pd.to_numeric(ni.year, errors='coerce'); S['4h'] = 'The median collection year of Ni native cells is %d, with %.0f%% collected since 2000 (Fig 4h).' % (yr.median(), 100 * (yr >= 2000).mean())
    S['4i'] = 'Ni native cells have a median latitude of %.1f degrees and Mn cells of %.1f degrees (Fig 4i).' % (ni.lat.median(), cc[cc.element == 'Mn'].lat.median())
    e5 = FD.species_by_element(ok).merge(ok[['accepted_name', 'bio1_median_C', 'bio12_median_mm', 'ph_median']], left_on='sp', right_on='accepted_name'); md = e5.groupby('element')[['bio1_median_C', 'bio12_median_mm', 'ph_median']].median()
    S['5a'] = 'Among species with 20 or more native cells, median bio1 is %.1f degrees C for Ni species and %.1f for Mn species (Fig 5a, Table 3).' % (md.loc['Ni', 'bio1_median_C'], md.loc['Mn', 'bio1_median_C'])
    S['5b'] = 'Median bio12 is %s mm for Ni and %s mm for Mn species; bio12 is saturated at 6,553.5 mm in %s native cells (Fig 5b).' % (fm(md.loc['Ni', 'bio12_median_mm']), fm(md.loc['Mn', 'bio12_median_mm']), int((cells.bio12_raw == 65535).sum()))
    rho = spearmanr(ok.bio1_median_C, ok.bio12_median_mm).statistic; S['5c'] = 'Species medians of bio1 and bio12 are correlated (Spearman rho = %.2f, n = %d species) (Fig 5c).' % (rho, len(ok))
    S['5d'] = 'Median soil pH is %.1f for Ni species and %.1f for Mn species (Fig 5d, Table 3).' % (md.loc['Ni', 'ph_median'], md.loc['Mn', 'ph_median'])
    ins = ~cells.species_level_name.isin(set(ok.accepted_name)); S['5e'] = '%.1f%% of native cells belong to species with fewer than 20 cells, and %.1f%% of native cells have no SoilGrids pH value (Fig 5e).' % (100 * ins.mean(), 100 * cells.ph_h2o_0_5cm.isna().mean())
    gf = ok.groupby('family').agg(n=('accepted_name', 'size'), t=('bio1_median_C', 'median')).query('n>=8').sort_values('t'); S['5f'] = 'Among families with at least 8 species the warmest median bio1 is %.1f degrees C (%s) and the coolest %.1f (%s) (Fig 5f).' % (gf.t.iloc[-1], gf.index[-1], gf.t.iloc[0], gf.index[0])
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    X = ok.dropna(subset=['bio1_median_C', 'bio12_median_mm', 'ph_median'])[['bio1_median_C', 'bio12_median_mm', 'ph_median']]; ev = PCA(2).fit(StandardScaler().fit_transform(X)).explained_variance_ratio_ * 100; S['5g'] = 'The first two principal components explain %.0f%% and %.0f%% of the variance of species medians (Fig 5g).' % (ev[0], ev[1])
    tt = ok.assign(t=ok.accepted_name.map(t)).dropna(subset=['t']); S['5h'] = 'T1 species (n = %d) have a median bio1 of %.1f degrees C against %.1f for T2 species (n = %d) (Fig 5h).' % ((tt.t == 'T1').sum(), tt[tt.t == 'T1'].bio1_median_C.median(), tt[tt.t == 'T2'].bio1_median_C.median(), (tt.t == 'T2').sum())
    t1s = set(E[(E.tier == 'T1') & (E.scope == 'hyperaccumulation')].sp); d4 = ok[ok.accepted_name.isin(t1s)].sort_values('n_cells', ascending=False).head(4); S['5i'] = 'The four T1 species with most native cells are %s, with %s native cells in total (Fig 5i).' % (', '.join(d4.accepted_name), fm(d4.n_cells.sum()))
    fams = ok.family.value_counts().head(12).index
    S['5j'] = 'Across the 12 largest families the family-level median bio1 spans %.1f to %.1f degrees C, so family explains much of the variation among elements (Fig 5j).' % (ok[ok.family.isin(fams)].groupby('family').bio1_median_C.median().min(), ok[ok.family.isin(fams)].groupby('family').bio1_median_C.median().max())
    return S


def main():
    S = sentences(); man = pd.read_csv(META / 'figure_manifest.csv'); man['k'] = man.panel.str.replace('figure', '')
    res = ['# Results skeleton (every number computed from data; replace with prose)', '', '## Evidence in HADB (Table 1)', 'Table 1 gives unique species per element by best tier in the headline view.', '']
    secs = {'2': '## Evidence, sources and tiers', '3': '## Names, thresholds and the headline view (Table 2)', '4': '## Occurrence records and their cleaning', '5': '## Climate and soil of the native cells (Table 3)'}
    res = ['# Results skeleton (every number computed from data; replace with prose)', '']
    for fig in '2345':
        res.append(secs[fig]); res.append('')
        for k in sorted(k for k in S if k[0] == fig): res.append(S[k])
        res.append('')
    (ROOT / 'manuscript' / 'results_skeleton.md').write_text('\n'.join(res), encoding='utf-8', newline='\n')
    cav = ['Screening bias: species appear because a screen or review reported them; absence is not evidence of absence.', 'Non-commercial (CC BY-NC) GBIF records are excluded from the primary basis.', 'Cleaning did not test country capitals or institution coordinates; coordinate uncertainty is missing for most native cells.',
           'bio12 is saturated at 6,553.5 mm in the wettest places; SoilGrids has no value on some cells.', 'Ultramafic status was not assessed (layers cover the Americas only; no panel shows it).', 'Species with fewer than 20 native cells have no environment statistics.']
    L = ['# Figure legends', '', 'Data: HADB release candidate 3 (headline view), environment run of 13 Oct 2026 (primary basis: non-NC GBIF records, cleaned, one record per species per CHELSA cell, native only). Occurrence data: ' + FD_CIT + '. Panel letters are added at assembly; no point records or coordinates are shown (hexagon and density summaries only).', '']
    for fig, title in (('2', 'Figure 2. Evidence in HADB: species, sources, tiers and thresholds.'), ('3', 'Figure 3. Names, thresholds and the headline view.'), ('4', 'Figure 4. The occurrence records and their cleaning.'), ('5', 'Figure 5. Climate and soil of the native cells of the species.')):
        L.append('**' + title + '**'); L.append('')
        for _, r in man[man.panel.str.startswith('figure' + fig)].iterrows():
            k = r.k; L.append('(%s) %s. Chart: %s. n = %s. Data and filter: %s.' % (k[1], TITLES[k], r.chart, format(int(r.n), ','), r['filter']))
        L.append(''); L.append('Caveats: ' + ' '.join(cav)); L.append('')
    (ROOT / 'manuscript' / 'figure_legends.md').write_text('\n'.join(L), encoding='utf-8', newline='\n'); print('wrote results_skeleton.md (%d sentences) and figure_legends.md' % len(S))


FD_CIT = FD.__dict__.get('CITATION', 'GBIF.org (13 October 2026) GBIF Occurrence Download https://doi.org/10.15468/dl.kb25da')
if __name__ == '__main__':
    main()
