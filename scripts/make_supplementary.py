"""Supplementary files S1-S5 (manuscript/supplementary). Numbers are computed from data_release/."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hadb_data as H
OUT = H.P / 'manuscript' / 'supplementary'; OUT.mkdir(parents=True, exist_ok=True)
D = H.P / 'data_release'


def s1_s2():
    SE = H.species_element(); SE.to_csv(OUT / 'S1_species_element.csv', index=False, encoding='utf-8-sig', lineterminator='\n')
    E = pd.read_csv(H.REL / 'evidence.csv', dtype=str, keep_default_na=False); E.to_csv(OUT / 'S2_evidence.csv', index=False, encoding='utf-8-sig', lineterminator='\n')
    return len(SE), len(E)


def s3():
    U = pd.read_csv(H.REL / 'unresolved_names.csv', dtype=str, keep_default_na=False); X = pd.read_csv(H.REL / 'excluded_rows.csv', dtype=str, keep_default_na=False)
    A = pd.read_csv(H.REL / 'block_b_row_accounting.csv', dtype=str, keep_default_na=False); R = pd.read_csv(H.DER / 'unresolved_names_review_v3.csv', dtype=str, keep_default_na=False)
    R = R[(R.decision != '') | R.decision_note.str.startswith('cleared')][['input_name', 'rows', 'suggested_accepted_name', 'similarity', 'region_ok', 'origins', 'decision', 'match_class', 'decision_note']]
    G = pd.read_csv(H.DER / 'gbif_download_excluded_step14.csv', keep_default_na=False)
    Q = pd.read_csv(H.REL / 'name_class_table.csv')
    readme = pd.DataFrame({'sheet': ['name_classes', 'unresolved_names', 'excluded_rows', 'name_decisions', 'block_b_row_accounting', 'gbif_species_excluded'],
                           'content': ['Block B rows by name class (resolved, genus by design, non-taxon, unresolved)', 'Block B rows kept out of the table, with reason (rc3)', 'master rows left out because the element label is not a chemical symbol',
                                       'names accepted or cleared by decision, with evidence (abbreviated genus: accepted only if the same row or article gives the full genus)', 'each of the 1,065 Block B rows in exactly one bucket',
                                       'species of the GBIF candidate set that were not downloaded, with the reason (below 20 or above 100,000 records, GBIF match not usable, name rule)']})
    with pd.ExcelWriter(OUT / 'S3_names_and_exclusions.xlsx', engine='openpyxl') as w:
        readme.to_excel(w, 'README', index=False); Q.to_excel(w, 'name_classes', index=False); U.to_excel(w, 'unresolved_names', index=False); X.to_excel(w, 'excluded_rows', index=False)
        R.to_excel(w, 'name_decisions', index=False); A.to_excel(w, 'block_b_row_accounting', index=False); G.to_excel(w, 'gbif_species_excluded', index=False)
    return len(U), len(X), len(R), len(G)


def s4():
    L = pd.read_csv(H.DER / 'licence_table.csv', keep_default_na=False); N = pd.read_csv(H.DER / 'new_vs_known_counts_papers.csv', keep_default_na=False)
    T2 = pd.read_csv(H.P / 'manuscript' / 'tables' / 'Table2.csv', encoding='utf-8-sig'); G = pd.read_csv(H.WRK / 'licence_split_by_licence.csv')
    with pd.ExcelWriter(OUT / 'S4_sources_licences_new_vs_known.xlsx', engine='openpyxl') as w:
        pd.DataFrame({'sheet': ['licence_table', 'new_vs_known_papers', 'evidence_sources', 'gbif_licences'], 'content': ['licence and redistribution status of every input', 'counts of new versus previously known taxa as quoted in each paper, with PDF page and quote; total checks',
                      'Table 2 data', 'GBIF download records and species by licence; citation ' + H.CITATION_GBIF]}).to_excel(w, 'README', index=False)
        L.to_excel(w, 'licence_table', index=False); N.to_excel(w, 'new_vs_known_papers', index=False); T2.to_excel(w, 'evidence_sources', index=False); G.to_excel(w, 'gbif_licences', index=False)
    return len(L), len(N)


def s5():
    from docx import Document
    from docx.shared import Pt
    SE = H.species_element(); E = H.evidence(); Eh = H.evidence(headline=True); F = H.env_facts(); S = H.env(); Sok = H.env_ok()
    sv = pd.read_csv(H.WRK / 'survival_table.csv'); nc = pd.read_csv(H.REL / 'name_class_table.csv'); lic = pd.read_csv(H.WRK / 'licence_split_by_licence.csv')
    tiers = SE.best_tier.value_counts().to_dict(); sp = SE.species_level_name.nunique()
    doc = Document(); doc.styles['Normal'].font.name = 'Calibri'; doc.styles['Normal'].font.size = Pt(10.5)
    def h(t, l=1): doc.add_heading(t, level=l)
    def p(t): doc.add_paragraph(t)
    def b(t): doc.add_paragraph(t, style='List Bullet')
    def tbl(df):
        t = doc.add_table(rows=1, cols=len(df.columns)); t.style = 'Light Grid Accent 1'
        for i, c in enumerate(df.columns): t.rows[0].cells[i].text = str(c)
        for r in df.itertuples(index=False):
            cells = t.add_row().cells
            for i, v in enumerate(r): cells[i].text = str(v)
    doc.add_heading('Supplementary Methods and Limitations: HADB v1 (release candidate 3)', 0)
    p('Data units used throughout: block_b_row (one raw row of the literature-mined Block B, 1,065 rows), master_row (one stored row of the master table), species (a WCVP species-level name), evidence row (one citation for one species and element), cell (one 30 arc-second CHELSA grid cell).')
    h('1. Evidence tiers, scope and the headline view')
    p('HADB records which elements a species is reported to accumulate, not how much. Release rc3 holds %d species_element rows for %d species and %d evidence rows (%d without concentration values). Tiers: T1 = taxon-level measurement tested against a threshold, where the source class is hyperaccumulator (Gei et al. 2020 XRF rows; paper rows with their own value); T2 = literature label or compiled list (Block B labels for Ni, Zn, Mn, Co, Cd, Se; Gei compiled lists S2.6 and S2.7; paper values cited from earlier work); T3 = element outside Ni, Zn, Mn, Co, Cd, Se, or no concentration basis. species_element rows by best tier: T1 %d, T2 %d, T3 %d.' % (len(SE), sp, len(E), len(E), tiers.get('T1', 0), tiers.get('T2', 0), tiers.get('T3', 0)))
    p('Scope tags the kind of source (hyperaccumulation, phytoremediation, other, mixed, unknown). It is a tag, not a finding; a Block B record is tagged only when the article title contains "hyperaccumulat", "remediation" or "phytoextraction", so scope is unknown for %d of %d species_element rows.' % ((SE.scope == 'unknown').sum(), len(SE)))
    p('Headline view (used for all counts in the paper): Block B included; evidence rows with suspect_source = Y (one CORE PDF that could not be read), weakened = Y (rows printed in red, "not confirmed in this study") or citation_inferred = Y (DOI replaced after a Crossref title check) are left out. %d of %d evidence rows are in the headline view. The all-inclusive view drops nothing.' % (len(Eh), len(E)))
    h('2. Thresholds')
    p('Thresholds apply only to T1 and to threshold_class (micrograms per gram dry mass, as in the sources). Standard (low-range) and high-range (Gei et al. 2020) thresholds:')
    tbl(pd.DataFrame({'Element': ['Ni', 'Mn', 'Co', 'Zn'], 'Standard (ug/g)': ['1,000', '10,000', '300', '3,000'], 'High-range (ug/g)': ['5,000', '20,000', '1,000', '10,000']}))
    p('threshold_class is high-range if the taxon maximum is at or above the high-range threshold, standard if at or above the standard one, and label-only if there is no concentration or no threshold for the element. Rows with only a group maximum or a lower bound are capped at standard. Rows below the threshold were kept and flagged.')
    h('3. Name matching')
    p('Names as published were matched to the WCVP (Kew) names table: exact match, then normalised match (Unicode, case, whitespace, hybrid sign, first two words), then recorded decisions (gender endings, orthographic variants, single-candidate fuzzy matches at similarity 95 or more). A matched synonym resolves to its accepted name; a name without an accepted name stays unresolved. Of 1,065 Block B rows: %s.' % '; '.join('%s %d (%.1f%%)' % (r['class'].replace('_', ' '), r.block_b_rows, r.pct_of_block_b_rows) for _, r in nc.iterrows() if r['class'] != 'total block_b_rows'))
    p('Names with a region-passing candidate (an abbreviated genus or a misspelling) were accepted only by decision: an abbreviated genus is accepted only if the same row or the same article gives the full genus; spelling corrections were kept by explicit decision and tagged spelling_manual. The evidence for each decision is in Supplementary S3.')
    h('4. GBIF occurrence data')
    p('Species set: species with T1 or T2 evidence for Ni, Mn, Zn or Co from a hyperaccumulation-scope source in the headline view (403 candidates); species reached only through an abbreviated genus or a match below 0.95 similarity were dropped unless the match is a region-checked gender ending; species with a GBIF match that was not EXACT/SPECIES/ACCEPTED (or a synonym resolved to an accepted species) were listed and not used. Records were counted with limit = 0 under the final predicate (hasCoordinate = true, hasGeospatialIssue = false, occurrenceStatus = PRESENT, basisOfRecord in PRESERVED_SPECIMEN, HUMAN_OBSERVATION, OBSERVATION, MATERIAL_SAMPLE); species with 20 to 100,000 records were downloaded (279 species).')
    p('Download: key 0023369-260928105237408, SIMPLE_CSV, no checklistKey (default GBIF backbone). %d records; licences: %s. GBIF labels the whole download CC BY-NC 4.0. Citation: %s' % (lic.records.sum(), '; '.join('%s %d' % (r.licence.replace('_', ' '), r.records) for r in lic.itertuples()), H.CITATION_GBIF))
    h('5. Cleaning, thinning and native range')
    p('Primary basis: non-NC records (CC0 and CC BY; %d records). Tests that ran (CoordinateCleaner is an R package; R was not available, so equivalents were used): missing or zero coordinates, latitude = longitude, coordinate uncertainty above 10 km (records without uncertainty kept and flagged), distance to the GBIF headquarters (1 km), distance to country centroids (1 km; Natural Earth 110 m), and a locality-text proxy for institutions (garden, herbarium, museum, university, arboretum, nursery, campus, cultivated). Tests that did NOT run: country capitals and the institution coordinate list. One record per species per CHELSA cell was kept. The native-range filter used WGSRPD level 3 regions and the WCVP distribution (native: listed, not introduced, not doubtful).' % F['records_non_nc'])
    pr = sv[sv.variant == 'primary'][['step', 'records', 'species']].copy(); pr['step'] = pr.step.str.replace(r'^\d[a-z]? ', '', regex=True); tbl(pr)
    p('%.1f%% of the %d final native cells have no recorded coordinate uncertainty (kept, flagged). Native-range assignment depends on the WCVP distribution: for example Noccaea caerulescens is listed as introduced in Sweden, Norway, Finland and Great Britain, and Nicotiana tabacum (a crop) as native only in Bolivia, so those species keep few native cells.' % (F['unc_null_pct'], F['n_cells']))
    h('6. Environmental extraction')
    p('CHELSA V2.1 bio1 (mean annual temperature) and bio12 (annual precipitation), 1981-2010, 30 arc-second: scale and offset were read from each file (bio1 scale 0.1, offset -273.15; bio12 scale 0.1, offset 0; neither file declares a nodata value; bio1 has no fill values). bio12 is saturated at the top of the uint16 range (6,553.5 mm) at %d coordinates (%d primary native cells; Meghalaya, the Western Ghats, Sarawak): kept and flagged, the true value is higher. SoilGrids 2.0 phh2o 0-5 cm mean: the file metadata give scale 1 and offset 0, but the stored integers are pH x 10 (ISRIC documentation; tile statistics), so values were divided by 10; points were reprojected to Interrupted Goode Homolosine with the file CRS; nodata -32768 (7.5%% of primary native cells). Each species is summarised by the median and quartiles over its native cells. Species with fewer than 20 native cells (%d of %d) are reported as "insufficient records" and carry no environment statistics.' % (F['ceiling_coords'], F['ceiling_cells'], (S.meets_20_cells == 'N').sum(), len(S)))
    p('Ultramafic status was not assessed: the available layers cover the Americas only, no record fell in a covered country for a Ni or Co species, so no ultramafic result is reported (not assessed is not the same as zero).')
    h('7. Validation')
    p('rc3 is rebuilt from the raw inputs by build_release.py; two runs give identical SHA256 for the master and every file. validate_release.py runs 52 checks (unique keys, WCVP identifiers, tier, element and scope values, a DOI, PMID or URL on every evidence row, duplicates, agreement between files, row accountability: each of the 1,065 Block B rows in exactly one of five buckets, evidence-to-master foreign keys, MANIFEST hashes) and exits 0 on rc3; a copy with planted faults (deleted evidence row, deleted accounting row) fails the checks as expected. The GBIF request was dry-run validated against the key list and the release hash before submission, and the downloaded file was checked: 101,048 records equal the expected count and all 279 species are present.')
    h('8. Limitations')
    for t in ['HADB records which elements, not amounts. Only Gei et al. and paper rows carry thresholds.',
              'Block B is mostly second-hand: 13 of its 26 PMIDs are reviews, one review (PMID 27726084) supplies about a third of the evidence rows, and the manual audit of Block B is not coded, so its error rate is unknown. Screening bias: species appear because a screen or review reported them.',
              'There is no measured negative set: absence from HADB is not evidence of absence, and the table cannot train a classifier of non-hyperaccumulators.',
              'Scope is unknown for most Block B rows; the Sabah species lists (Supplementary Tables 2 to 4) and Queensland Table S3 were not available, so those sources are partial.',
              'Names: unresolved Block B rows are listed with reasons (S3); abbreviated names without the full genus in the row or article were cleared.',
              'Licences: no release licence is chosen; several inputs have unknown redistribution status (S4). The GBIF download is CC BY-NC 4.0 as a whole; the environment summaries use the non-NC records.',
              'Occurrence cleaning is weaker than CoordinateCleaner (no capital or institution coordinate tests); coordinate uncertainty is missing for most cells; sampling is uneven; cell values describe where species were recorded, not their niche. The native filter inherits errors and gaps of the WCVP distribution.',
              'bio12 is saturated at 6,553.5 mm in the wettest places; SoilGrids has no value on 7.5% of cells; the ultramafic layers cover the Americas only.']: b(t)
    h('9. Known issues of release rc3')
    ki = (H.REL / 'KNOWN_ISSUES.md').read_text(encoding='utf-8')
    for line in ki.splitlines():
        if line.startswith('## '): h(line[3:], 2)
        elif line.startswith('- '): b(line[2:].replace('`', '').replace('*', ''))
        elif line.strip() and not line.startswith('#'): p(line.replace('`', '').replace('*', ''))
    h('10. Data availability and citation')
    p('rc3 files and checksums: see MANIFEST.tsv of the release. Occurrence data: ' + H.CITATION_GBIF + '. Zenodo DOI: to be added.')
    doc.save(OUT / 'S5_Supplementary_Methods_and_Limitations.docx')


if __name__ == '__main__':
    print('S1/S2 rows', s1_s2()); print('S3 rows', s3()); print('S4 rows', s4()); s5(); print('S5 written')
