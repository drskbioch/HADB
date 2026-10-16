# CHANGELOG

## rc3 (2026-10-13)

rc3 is rebuilt from the raw inputs by `scripts/build_release.py` (step 13); the master is `14_derived/master_species_v2.csv` (rc2 used `master_species_v1.csv`, which is left as it was).

Changes since rc2 (`rc2_vs_rc3_species_element_diff.csv`, `rc2_vs_rc3_evidence_diff.csv`):
- Name decisions: of the 14 names rc2 accepted by region test, 7 abbreviated genera were cleared (8 block_b_rows, back in `unresolved_names.csv`); 4 abbreviated genera stay because the same row or article gives the full genus (`match_class` abbreviation_full_genus_in_row / _in_article) and 3 spelling corrections stay (`match_class = spelling_manual`). Evidence for each is in `new_name_decisions_table.csv` and `14_derived/unresolved_names_review_v3.csv`.
- species_element: 3,497 rows in rc2, 3,479 in rc3; 0 added, 18 removed, 3,479 in both (changed cells: n_evidence 21, name_as_published 21, citations 17).
- evidence: 4,583 rows in rc2, 4,543 in rc3; 4,543 identical on (species, element, evidence type, name, citation); only in rc2 40, only in rc3 0 (rc2 only: name decision cleared (abbreviated genus, step 13) 40).
- `new_name_decisions_table.csv` gains `match_class` and `evidence_for_decision`; `rc1_vs_rc2_*` diff files are replaced by `rc2_vs_rc3_*`.
- `validate_release.py` reads `master_species_v2.csv` for rc3.
- Not changed: tiers, thresholds, scope rules, headline view definition, all other inputs.

### rc2 (2026-10-13)

rc2 is rebuilt from the raw inputs by `scripts/build_release.py` (step 11); the regenerated `master_species_v1.csv` was first checked against the stored v1 with the candidate decisions switched off: identical in all 36 columns.

Changes since rc1 (`rc1_vs_rc2_species_element_diff.csv`, `rc1_vs_rc2_evidence_diff.csv`):
- species_element: 3,450 rows in rc1, 3,497 in rc2; 47 added, 0 removed, 3,450 in both (changed cells: n_evidence 52, name_as_published 26, citations 136).
- evidence: 4,479 rows in rc1, 4,583 in rc2; 4,470 identical on (species, element, evidence type, name, citation); only in rc1 9, only in rc2 113 (rc1 only: citation replaced 9; rc2 only: citation added (a block_b_row without a PMID that rc1 did not carry over) 28; rc2 only: citation replaced 9; rc2 only: new row: name accepted by region-test decision 76).
- 19 block_b_rows from 14 names with a region-passing candidate are now in the table (decision `region_test_candidate_accepted_step11`). In rc1 they were neither in the table nor in `unresolved_names.csv`; `README.md` of rc1 counted them as resolved by mistake.
- 25 evidence rows (9 visible in rc1) from source rows with unusable DOIs now cite `10.1016/j.foodchem.2003.06.004` (Crossref title check; `citation_note`).
- `evidence.csv`: new columns `source_rows` and `suspect_source`; the 198 rows from the CORE PDF (191 in rc1) are tagged `suspect_source = Y` (no tier change).
- `species_element.csv`: new columns `rank`, `n_suspect`, `suspect_only`. `counts.csv` gains a suspect view; `counts_species.csv` is new.
- `excluded_rows.csv` replaces `excluded_records.csv` and gives the proposed correction for the two "Mi" rows.
- `scope`: `other` and `mixed` are accepted as hand labels; none filled in.
- The master drops the column `scope_previous` (36 columns again).
- Revision 2 (step 12): `evidence.csv` gains `citation_inferred` (Y on the 25 rows citing 10.1016/j.foodchem.2003.06.004 by inference); `counts.csv` and `counts_species.csv` gain `inferred_view` and `view_label` (headline = suspect, weakened and inferred evidence dropped); `species_element.csv` gains `n_inferred`; new tables for the 14 accepted names, merged records, row accounting, headline pairs and GBIF >= 20 clean records; GBIF counts for the 6 added species; `validate_release.py` checks row accountability and evidence-to-master keys.
- Documents: the 487 PMID values are described as 61 Block B only + 426 Block A only, of which only 28 are valid PMIDs; the Europe PMC extraction item is dropped from the inventory (it was based on 487 values that are not PMIDs).
