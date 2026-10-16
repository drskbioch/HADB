"""Phase 0: verify inputs, copy release inputs (read-only copies) into data_release/ with a SHA256 manifest, .gitignore, git init, image inventory."""
import csv, hashlib, os, shutil, subprocess, sys
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
P = Path(__file__).resolve().parents[1]
A = Path(r'D:\Tayyab\DrS\data_db\HADB\HADB_data_organized\HADB_data')
REL = A / '15_release_rc3'; DER = A / '14_derived'; W = DER / 'gbif_work'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest().upper()
need = [REL/'species_element.csv', REL/'evidence.csv', REL/'counts.csv', REL/'unresolved_names.csv', REL/'data_dictionary.csv', DER/'licence_table.csv',
        DER/'new_vs_known_counts_papers.csv', DER/'species_environment_summary.csv', W/'records_environment_primary.csv.gz', W/'cleaning_counts.csv', W/'survival_table.csv']
miss = [str(x) for x in need if not x.exists()]
if miss: print('MISSING', miss); sys.exit(2)
copies = {'release': [REL/f for f in ('species_element.csv','evidence.csv','counts.csv','counts_species.csv','unresolved_names.csv','data_dictionary.csv','excluded_rows.csv','block_b_row_accounting.csv',
           'name_class_table.csv','new_name_decisions_table.csv','headline_pairs_by_tier_scope.csv','top10_pmids_by_block_b_rows.csv','block_b_record_drops.csv','core_pdf_profile.csv','MANIFEST.tsv','README.md','KNOWN_ISSUES.md','CHANGELOG.md')],
          'derived': [DER/f for f in ('species_environment_summary.csv','species_environment_summary_sensitivity_all_records.csv','licence_table.csv','new_vs_known_counts_papers.csv','paper_totals_context.csv','gbif_download_taxonkeys.csv','gbif_counts_final_step14.csv','master_species_v2.csv')],
          'work': [W/f for f in ('records_environment_primary.csv.gz','records_flags_all.csv.gz','cleaning_counts.csv','survival_table.csv','licence_split_by_licence.csv','licence_split_by_species.csv','native_primary.csv.gz','species_wcvp_species_ids.csv','wgsrpd_level3.geojson','env_climate_file_metadata.csv','env_soil_file_metadata.csv')],
          'docs': [A/'rc3_FREEZE.md', A/'SUMMARY_STEP16.txt', A/'SUMMARY_STEP15.txt']}
rows = []
for sub, fs in copies.items():
    (P/'data_release'/sub).mkdir(parents=True, exist_ok=True)
    for f in fs:
        if not f.exists(): print('skip (absent):', f.name); continue
        d = P/'data_release'/sub/f.name
        if not d.exists(): shutil.copy2(f, d)
        rows.append((f'{sub}/{f.name}', d.stat().st_size, sha(d), sha(f), str(f)))
with open(P/'data_release'/'MANIFEST.tsv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh, delimiter='\t', lineterminator='\n'); w.writerow(['path','bytes','sha256','source_sha256','source']); w.writerows(rows)
bad = [r[0] for r in rows if r[2] != r[3]]
print('copied %d files; hash mismatches vs source: %s' % (len(rows), bad))
(P/'.gitignore').write_text('manuscript/\ndist/\ndata_release/\nbackend/data/*.sqlite\n*.zip\n.env*\nnode_modules/\n__pycache__/\n.next/\n_backups/\n', encoding='utf-8')
if not (P/'.git').exists(): subprocess.run(['git', 'init', '-q'], cwd=P)
# image inventory
SKIP = {'node_modules','_backups','.git','__pycache__','HADB_data_organized','HADB_project','.next','dist','literature'}
root = Path(r'D:\Tayyab\DrS'); out = []
for dp, dn, fn in os.walk(root):
    depth = len(Path(dp).relative_to(root).parts)
    dn[:] = [d for d in dn if d not in SKIP and depth < 4]
    for f in fn:
        if f.lower().endswith(('.png','.jpg','.jpeg','.webp','.svg')):
            p = Path(dp)/f
            try:
                if f.lower().endswith('.svg'): wh = ('','')
                else:
                    with Image.open(p) as im: wh = im.size
                out.append((str(p), wh[0], wh[1], p.stat().st_size, sha(p)))
            except Exception as e: out.append((str(p), '', '', p.stat().st_size, 'unreadable'))
with open(P/'docs'/'image_inventory.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['path','width','height','bytes','sha256']); w.writerows(out)
print('images found:', len(out), '| raster >= 400 px both sides:', sum(1 for r in out if r[1] != '' and r[1] >= 400 and r[2] >= 400))
