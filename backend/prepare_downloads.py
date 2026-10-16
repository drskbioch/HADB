"""Copy the public release files into backend/data/downloads/ and write downloads_manifest.json with SHA256. No GBIF zip, no record-level data.
Run:  python backend/prepare_downloads.py"""
import hashlib, json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; DR = ROOT / 'data_release'; OUT = ROOT / 'backend' / 'data' / 'downloads'; OUT.mkdir(parents=True, exist_ok=True)
FILES = [('release/species_element.csv', 'one row per species (WCVP taxon) and element: best tier, class, scope, citations'), ('release/evidence.csv', 'one row per evidence record with citation, DOI, tier, scope, flags (no concentration values)'),
         ('release/counts.csv', 'unique species per element by best tier and scope, 16 views (headline view marked)'), ('release/counts_species.csv', 'the same by rank'), ('release/unresolved_names.csv', 'Block B rows kept out of the table, with reasons'),
         ('release/excluded_rows.csv', 'rows left out for a non-symbol element label'), ('release/data_dictionary.csv', 'column dictionary'), ('release/README.md', 'release README'), ('release/KNOWN_ISSUES.md', 'known issues of the release'),
         ('release/CHANGELOG.md', 'changes since earlier release candidates'), ('release/MANIFEST.tsv', 'SHA256 of every release file and input'), ('derived/species_environment_summary.csv', 'climate and soil summary per species (>= 20 native cells; others: insufficient records); aggregated, no coordinates')]
items = []
for rel, desc in FILES:
    src = DR / rel; dst = OUT / src.name; shutil.copy2(src, dst); h = hashlib.sha256(dst.read_bytes()).hexdigest().upper()
    items.append(dict(name=src.name, bytes=dst.stat().st_size, sha256=h, description=desc, version='HADB v1 (rc3)'))
(OUT / 'downloads_manifest.json').write_text(json.dumps(items, indent=1), encoding='utf-8'); print(len(items), 'files in downloads')
