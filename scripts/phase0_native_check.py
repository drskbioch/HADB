"""Phase 0 step 6: native-range check (WCVP distribution vs the introduced cells of Noccaea caerulescens and Nicotiana tabacum)."""
import zipfile
from pathlib import Path
import pandas as pd
P = Path(__file__).resolve().parents[1]
ids = pd.read_csv(P/'data_release/work/species_wcvp_species_ids.csv', dtype=str).set_index('species_level_name').wcvp_species_id
R = pd.read_csv(P/'data_release/work/records_environment_primary.csv.gz', low_memory=False)
with zipfile.ZipFile(r'D:\Tayyab\DrS\data_db\HADB\HADB_data_organized\HADB_data\06_taxonomy_wcvp_kew\wcvp.zip') as z:
    D = pd.read_csv(z.open('wcvp_distribution.csv'), sep='|', dtype=str, usecols=['plant_name_id','area_code_l3','area','introduced','extinct','location_doubtful'])
bug = False
for sp in ('Noccaea caerulescens', 'Nicotiana tabacum'):
    d = D[D.plant_name_id == ids[sp]]; print('\n==', sp, 'WCVP id', ids[sp], '| distribution rows', len(d), '| native', int((d.introduced == '0').sum()), 'introduced', int((d.introduced == '1').sum()), 'doubtful', int((d.location_doubtful == '1').sum()))
    print('native :', '; '.join(d[(d.introduced == '0')].area.head(40)))
    print('introd.:', '; '.join(d[(d.introduced == '1')].area.head(40)))
    x = R[(R.species_level_name == sp) & (R.native_status == 'introduced')]
    g = x.groupby(['LEVEL3_COD', 'LEVEL3_NAM']).size().sort_values(ascending=False).head(10); print('WGSRPD regions of its "introduced" cells (top 10):', dict(((a, b), int(n)) for (a, b), n in g.items()))
    st = d.set_index('area_code_l3').introduced.to_dict()
    nat_listed = [c for c in x.LEVEL3_COD.dropna().unique() if st.get(c) == '0']; print('regions of introduced cells that WCVP lists as NATIVE:', nat_listed)
    bug |= bool(nat_listed)
s = R.groupby('species_level_name').native_status.value_counts().unstack(fill_value=0); s['n'] = s.sum(axis=1); s['introduced_share'] = (s.get('introduced', 0) / s.n).round(3)
print('\nspecies with introduced cells:', int((s.get('introduced', 0) > 0).sum()), 'of', len(s)); print(s[s.get('introduced', 0) > 0].sort_values('introduced_share', ascending=False).head(6).to_string())
print('\nBUG (WCVP lists an "introduced" region as native):', bug)
