import csv, hashlib, shutil
from pathlib import Path
P = Path(__file__).resolve().parents[1]; A = Path(r'D:\Tayyab\DrS\data_db\HADB\HADB_data_organized\HADB_data'); D = A/'14_derived'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
add = [('derived', D/f) for f in ('unresolved_names_review_v3.csv','gbif_download_excluded_step14.csv','gbif_species_set_step14.csv','gbif_counts_final.csv')] + [('docs', A/'SUMMARY_STEP14.txt'), ('docs', A/'SUMMARY_STEP13.txt')]
rows = list(csv.reader(open(P/'data_release/MANIFEST.tsv', encoding='utf-8'), delimiter='\t')); have = {r[0] for r in rows[1:]}
for sub, f in add:
    d = P/'data_release'/sub/f.name
    if f.exists() and f'{sub}/{f.name}' not in have:
        shutil.copy2(f, d); rows.append([f'{sub}/{f.name}', d.stat().st_size, sha(d), sha(f), str(f)])
csv.writer(open(P/'data_release/MANIFEST.tsv', 'w', newline='', encoding='utf-8'), delimiter='\t', lineterminator='\n').writerows(rows); print(len(rows)-1, 'files in manifest')
