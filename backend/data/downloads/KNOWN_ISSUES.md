# KNOWN ISSUES (rc3)

Read this before using the release. Units: block_b_row (raw Block B row), master_row (stored row of `master_species_v2.csv`), species (WCVP species-level name).

## 1. Scope is unknown for 76% of rows

2,655 of 3,479 species_element rows have `scope = unknown` (3,159 of 4,543 evidence rows). The cause is the title rule: a Block B record is tagged only if its article title contains "hyperaccumulat", "remediation" or "phytoextraction". The ten largest Block B articles hold 75% of block_b_rows and most of them match neither word. Nothing in `scope` should be read as "this is not a phytoremediation or hyperaccumulation species". A hand-labelling sheet for the ten largest PMIDs is `14_derived/scope_pmid_lookup_v3.csv` (no labels filled; the build reads them if they are).

## 2. Evidence is concentrated in a few secondary sources

- Block B supplies 3,479 of 4,543 evidence rows (77%) and is the only evidence for 2,939 of 3,479 species_element rows (84%). It records which elements, not how much, and 13 of its 26 PMIDs are tagged Review by Europe PMC.
- One review, PMID 27726084 ("A tabulated review on distribution of heavy metals in various plants"; Europe PMC tags it only Journal Article), supplies 1,604 evidence rows (35%) and is the only evidence for 1,297 species_element rows. Its 329 block_b_rows share one source text (the article abstract), so a row-level check against the article is not possible from the archive.
- **Suspect source.** One link, a CORE PDF (`core.ac.uk/download/pdf/41685633.pdf`), supplies 191 evidence rows (191 in rc1, 198 in rc2) (tagged `suspect_source = Y`; no tier change) from 19 block_b_rows and 18 species; 114 of its 191 species x element pairs have no other evidence. The PDF could not be downloaded (HTTP 403); by title in CORE and Crossref it is Bhat et al. 2009, *Food Analytical Methods*, DOI 10.1007/s12161-009-9107-y. Profile: `core_pdf_profile.csv`, `core_pdf_species.csv`.
- Without Block B the release holds 417 species (`counts.csv`); Cd and Se have no evidence at all outside Block B.

## 3. No measured negative set

The release lists species reported to accumulate an element. It has no species measured and found below a threshold, so absence of a species is not evidence of absence, and the table cannot be used to train or test a classifier of non-hyperaccumulators. The only sub-threshold values in the archive (the *Noccaea* tables, Ni and Zn) are not in the release.

## 4. Sabah species-list gap

The Sabah paper's species lists (28 Ni, 51 Mn, 12 to 14 Co species) are in Supplementary Tables 2 to 4, which are not in the archive. The 46 Sabah master_rows (35 species) come from the results text: 24 of 28 Ni species, 15 of 51 Mn, 6 of 12 to 14 Co. Queensland Mn is also partial (9 of 20 to 27 species; Table S3 not in the archive).

## 5. Citation gaps

- 335 evidence rows (7.4%) rest on a web link, because their block_b_row has no valid PMID; they are marked in `citation_note` ("link only; article not identified" or the suspect-source note).
- Five source rows (excel rows 106 to 110) cited DOIs `10.1016/j.foodchem.2003.06.005` to `.009`, which Crossref resolves to unrelated papers; they give 25 evidence rows (rc1 showed only 9 of them, because it dropped link citations of master_rows that also had a PMID). After a Crossref title check against the row context (Nigerian herbal plants; Fe, Mn, Cu, Pb, Zn) they now cite `10.1016/j.foodchem.2003.06.004` ("Heavy trace metals and macronutrients status in herbal plants of Nigeria", Ajasa et al. 2004), and `citation_note` says so. The check was at title level; the article text was not read; these rows carry `citation_inferred = Y` and are left out of the headline view. Decision file: `14_derived/doi_corrections_step11.csv`.
- Evidence rows with no DOI, PMID or URL: 0.
- The Gei 2020 DOI (10.1093/botlinnean/boaa029) was supplied and checked against Crossref (title, journal, year); the PDF in the archive prints no DOI. Gei rows cite a supplement table and row, not a page.
- Sabah rows are "van der Ent et al. 2019b" (J. Geochem. Explor.). The Sci. Rep. paper "2019a" (10.1038/s41598-019-40050-6) supplies no evidence row.

## 6. Excluded rows

2 master_rows are in `excluded_rows.csv`: element label "Mi" in the source (a typo). Proposals taken from the source lists (never applied): *Clematis gouriana* Mn (fairly confident), *Elsholtzia communis* Mn or Ni (undecided).

## 7. Names

- 135 block_b_rows are kept out (`unresolved_names.csv`): 72 genus-only, 15 non-taxa, 48 unresolved (4.5% of block_b_rows).
- 11 block_b_rows (7 names) are in the table by decision: 4 abbreviated genera (*V. zizanioides*, *C. zizanioides*, *C. angustifolia*, *D. sanguinalis*) whose full genus is given in the same row or the same article, and 3 spellings kept by decision (*Cyclosorus afer*, *Linum utitassimum*, *Solanum incum*; `match_class = spelling_manual`, spelling similarity 0.89 to 0.93). The other 7 abbreviated names that rc2 had accepted (8 block_b_rows) were cleared in rc3 because neither their row nor their article gives the full genus; they are in `unresolved_names.csv`. Two similar candidates were reverted earlier and stay unresolved (*Alisma plantago aquatica*, a cell naming two species). The decisions and their evidence are in `14_derived/unresolved_names_review_v3.csv` (columns `match_class`, `decision_note`).

## 8. Other

- 43% of species_element rows are T3 (element outside Ni, Zn, Mn, Co, Cd, Se, or no concentration basis).
- No licence is chosen; 5 inputs have unknown redistribution status (`14_derived/licence_table.csv`).
- The manual audit of Block B (samples v1 to v5) is not coded, so the error rate of Block B rows is unknown.
