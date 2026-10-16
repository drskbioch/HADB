# HADB hyperaccumulator list: release candidate 3 (rc3)

**Status: release candidate, built 2026-10-13. Not published, not licensed.** No licence has been chosen for this release, and 5 of the inputs have an unknown redistribution status (see `14_derived/licence_table.csv`); nothing here should be redistributed until that is decided. `source_license` and `nc_derived` in `evidence.csv` carry what is known per row. Read `KNOWN_ISSUES.md` first.

## What this is

A table of which plant species are reported to accumulate (or hyperaccumulate) which chemical elements, with the evidence behind each statement and a tier for how strong that evidence is. It records **which** elements, **not how much**: no concentration values are in this release.

Units used in all files and reports:
- **block_b_row**: one raw row of HADB Block B (1,065 rows, sheet "HADB fInal" of `HADB final.xlsx`; `excel_row` = `block_b_row` + 1).
- **master_row**: one stored row of `14_derived/master_species_v2.csv` (4,098 rows; one per name as published, element, evidence type and source row; the number of distinct species x element x source keys is smaller).
- **species**: a WCVP species-level name (`species_level_name`; 947). Infraspecific taxa and hybrids sit under their species in counts. `rank` in `species_element.csv` says whether the accepted name is a species or an infraspecific taxon.

The master and this folder are regenerated from the raw inputs by `scripts/build_release.py` (see `scripts/` and `MANIFEST.tsv`); running it twice gives byte-identical files.

## Files

| File | Rows | What |
| --- | --- | --- |
| `species_element.csv` | 3,479 | one row per (wcvp_accepted_name, element) with rank, best tier, class, scope, citations, weakened, suspect counts |
| `evidence.csv` | 4,543 | one row per evidence record (master_row x citation); no concentrations; `doi`, `suspect_source`, `citation_note` |
| `unresolved_names.csv` | 135 | block_b_rows kept out of the table: 72 rank_genus_by_design, 15 non_taxon, 48 unresolved, each with a reason |
| `counts.csv` | 2,096 | unique species per element by best tier and scope; 16 views, one of them the headline view |
| `counts_species.csv` | 1,812 | the same by rank (species / infraspecific / genus): unique species and unique taxa |
| `excluded_rows.csv` | 2 | master_rows left out because the element label is not a chemical symbol, with a proposed correction (not applied) |
| `new_name_decisions_table.csv`, `new_names_merged_records.csv`, `block_b_row_accounting.csv`, `headline_pairs_by_tier_scope.csv`, `gbif_clean20_by_element_tier.csv`, `gbif_clean20_top_families.csv` | | the 14 accepted names, their merged records, the bucket of every block_b_row, headline pairs, GBIF >= 20 clean records |
| `block_b_record_drops.csv`, `name_class_table.csv`, `top10_pmids_by_block_b_rows.csv`, `pmid_value_breakdown.csv`, `core_pdf_profile.csv`, `core_pdf_species.csv` | | audit tables (see `KNOWN_ISSUES.md`) |
| `rc2_vs_rc3_species_element_diff.csv`, `rc2_vs_rc3_evidence_diff.csv` | | what changed since rc2, by key |
| `data_dictionary.csv`, `KNOWN_ISSUES.md`, `CHANGELOG.md` | | documentation |
| `MANIFEST.tsv` | | SHA256 and size of every rc3 file (except itself), of the regenerated master, of every build input and of the upstream sources |
| `scripts/` | | `build_release.py` and its modules, `validate_release.py`, `fetch_crossref_checks.py` |

## Scope

`scope` says what kind of source a record comes from. It is a tag, not a finding.
- **hyperaccumulation**: the source is a hyperaccumulator screen or species table (Gei 2020 XRF and compiled lists; the Sabah and Queensland papers), or a Block B article whose title contains "hyperaccumulat".
- **phytoremediation**: a Block B article whose title contains "remediation" or "phytoextraction".
- **biosorbent**: reserved for the biosorbent sheet (`Final-2`), which is **not** in this release; no row has it.
- **other / mixed**: accepted only as hand labels in `14_derived/scope_pmid_lookup_v3.csv`; none have been filled in.
- **unknown**: a Block B article whose title names neither, or a row without a usable PMID. `species_element.csv`: 2,655 of 3,479 rows (76%) are unknown.

## Tiers

- **T1**: taxon-level measurement tested against a threshold, where the paper's class is hyperaccumulator (Gei XRF rows; paper rows with their own value).
- **T2**: literature label or compiled list: Block B labels for Ni, Zn, Mn, Co, Cd, Se; Gei compiled lists S2.6 and S2.7; paper values cited from earlier work. The 15 species found only in the compiled lists (12 Ni, 3 Mn) are T2 by decision.
- **T3**: an element outside Ni, Zn, Mn, Co, Cd, Se, or no concentration basis.

Counts in `species_element.csv`: T1 504, T2 1,494, T3 1,481. `suspect_source = Y` rows keep their tier; filtering them is left to the user (`counts.csv` has the view).

## Thresholds

Used only for T1 and for `threshold_class` (micrograms per gram, as in the sources):

| | Ni | Mn | Co | Zn |
| --- | --- | --- | --- | --- |
| standard (low-range) | 1,000 | 10,000 | 300 | 3,000 |
| high-range (Gei 2020) | 5,000 | 20,000 | 1,000 | 10,000 |

`threshold_class` is high-range if the taxon's listed maximum is at or above the high-range threshold, standard if at or above the standard one, and label-only if there is no concentration or the element has no threshold. Paper rows use the paper's own threshold for `paper_class`. Rows with only a group maximum or a lower bound are capped at standard. Rows below the threshold were kept and flagged in the master, not removed. `weakened = Y` marks Gei compiled-list rows printed in red ("not confirmed in this study"); at species_element level it is Y only if all evidence is weakened (4 rows).

## Limits

1. **HADB records which elements, not amounts.** Block B has no concentration column; its rows are "accumulation reported". Only Gei and paper rows carry thresholds.
2. **Block B is mostly from reviews.** 13 of its 26 PMIDs are tagged Review by Europe PMC (499 of 983 block_b_rows with a valid PMID, 51%); one more article, PMID 27726084 (329 block_b_rows, 31% of Block B), is tagged only "Journal Article" but its title says "tabulated review". The ten largest PMIDs hold 75% of Block B. Most Block B rows are therefore second-hand extractions. Only 3 of 26 PMIDs have open full text; the manual audit of Block B is not coded.
3. **The Sabah species list is missing.** Its species lists (28 Ni, 51 Mn, 12 to 14 Co species) are in Supplementary Tables 2 to 4, which are not in the archive. The 46 Sabah master_rows (35 species) come from the results text: 24 of 28 Ni species, 15 of 51 Mn, 6 of 12 to 14 Co.
4. **No measured negative set.** The only sub-threshold values in the archive are the *Noccaea* tables (Ni, Zn), which are not part of this release; the Gei tables list only taxa with at least one specimen in the low range. Absence from this table is not evidence of absence.
5. **The biosorbent sheet is excluded.** `Final-2` (182 rows of microbial and agricultural-waste biosorbents, PMID 26315592) is not in the master, so no row has scope biosorbent. Block A (foliar nutrients, 1,044 rows) is not in the table either.
6. **PMIDs.** The PMID column of the 2,109-row table holds 487 distinct values = 61 in Block B only + 426 in Block A only (none in both); **only 28 are valid PMIDs** (26 in Block B, 2 in Block A). Block A's values are mostly web addresses.
7. **Names.** Of 1,065 block_b_rows, 930 are resolved to a species (87.3%), 72 are genus-only by design, 15 are non-taxa and 48 are unresolved (4.5%); the last three groups are in `unresolved_names.csv`. 11 of the resolved rows come from 7 names accepted by decision: 4 abbreviated genera whose full genus is given in the same row or the same article (`match_class` abbreviation_full_genus_in_row / _in_article) and 3 spelling corrections kept by decision (`spelling_manual`). Abbreviated names without such evidence were cleared and stay unresolved (revert or add by editing `decision` in `14_derived/unresolved_names_review_v3.csv`).
8. **Licences.** `nc_derived = Y` on 85 evidence rows (the Sabah manuscript is CC BY-NC; one Block B article is CC BY-NC-ND); `unknown` on 4,252.

## Counts

**Headline view** (`view_label = headline` in `counts.csv` and `counts_species.csv`): Block B included; evidence tagged `suspect_source = Y`, `weakened = Y` or `citation_inferred = Y` dropped. **All-inclusive view**: nothing dropped. `counts.csv` has 16 views (Block B, suspect, weakened, inferred each in or out).

Unique species, all scopes and tiers: 947 all-inclusive; 938 headline; 413 headline without Block B.

| Element | species, all-inclusive | species, headline | headline T1 | headline T2 | headline without Block B |
| --- | --- | --- | --- | --- | --- |
| Ni | 504 | 495 | 211 | 277 | 227 |
| Mn | 560 | 554 | 201 | 347 | 210 |
| Zn | 397 | 392 | 18 | 374 | 18 |
| Co | 240 | 233 | 37 | 196 | 40 |
| Cd | 243 | 243 | 0 | 243 | 0 |
| Se | 18 | 18 | 0 | 18 | 0 |

`headline_pairs_by_tier_scope.csv` gives the unique species x element pairs by best tier and scope for the two views.

## Checking

`python -X utf8 -I scripts/validate_release.py` prints failures only (nothing printed means all checks passed; exit code 0; `--verbose` lists the counts). It checks unique keys, WCVP ids, tier, element, rank and scope values, citations (a DOI, PMID or URL on every row), duplicates, agreement between the files, and the MANIFEST hashes.
