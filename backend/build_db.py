"""Build backend/data/hadb.sqlite from the release CSVs (data_release/, read-only copies of rc3 and the environment run).
Public scope only: species, element, class, tier, scope, citations, names, environment summaries. No concentration values, no GBIF points or coordinates.
Entity = species-level name (as in counts.csv); its id is the WCVP id of the species-rank record (or of its first infraspecific taxon when no species-rank record exists).
Run:  python backend/build_db.py"""
import datetime, hashlib, json, sqlite3, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DR = ROOT / 'data_release'
OUT = ROOT / 'backend' / 'data' / 'hadb.sqlite'
SCOPE_ORDER = ['hyperaccumulation', 'phytoremediation', 'biosorbent', 'other', 'mixed', 'unknown']
TIER_RANK = {'T1': 0, 'T2': 1, 'T3': 2}; THR = {'high-range': 0, 'standard': 1, 'label-only': 2}
CLS = {'hyperaccumulator (high-range)': 0, 'hyperaccumulator (standard or low-range)': 1, 'hyperaccumulator': 1, 'listed, no concentration': 2, 'label': 3}
GBIF_CITATION = 'GBIF.org (13 October 2026) GBIF Occurrence Download https://doi.org/10.15468/dl.kb25da'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()


def best(rows, tier_col, thr_col, cls_col):
    return sorted(rows, key=lambda r: (TIER_RANK[r[tier_col]], THR.get(r[thr_col], 2), CLS.get(r[cls_col], 3)))[0]


def main():
    SE = pd.read_csv(DR / 'release/species_element.csv', dtype=str, keep_default_na=False)
    E = pd.read_csv(DR / 'release/evidence.csv', dtype=str, keep_default_na=False)
    ENV = pd.read_csv(DR / 'derived/species_environment_summary.csv', keep_default_na=False, na_values=[''])
    C = pd.read_csv(DR / 'release/counts.csv', keep_default_na=False)
    # ---- species entities
    tx = SE.drop_duplicates('wcvp_accepted_name')[['wcvp_accepted_name', 'species_level_name', 'rank', 'wcvp_id', 'family', 'name_as_published']].copy()
    tx['wcvp_id'] = tx.wcvp_id.astype(int); sid = {}
    for sp, g in tx.groupby('species_level_name'):
        sr = g[g['rank'] == 'species']; sid[sp] = int(sr.wcvp_id.iloc[0]) if len(sr) else int(g.wcvp_id.min())
    tax_species = tx.set_index('wcvp_accepted_name').species_level_name.to_dict()
    E['species_name'] = E.species.map(tax_species); E['species_id'] = E.species_name.map(sid); E['headline'] = ((E.suspect_source != 'Y') & (E.weakened != 'Y') & (E.citation_inferred != 'Y')).astype(int)
    SE['species_id'] = SE.species_level_name.map(sid)
    # ---- species_element (species level)
    rows = []
    for (spid, el), g in SE.groupby(['species_id', 'element']):
        r = best(g.to_dict('records'), 'best_tier', 'threshold_class', 'class'); ev = E[(E.species_id == spid) & (E.element == el)]; eh = ev[ev.headline == 1]
        bh = best(eh.to_dict('records'), 'tier', 'threshold_class', 'class') if len(eh) else None
        sc_all = min(g.scope, key=SCOPE_ORDER.index); sc_h = min(eh.scope, key=SCOPE_ORDER.index) if len(eh) else None
        rows.append(dict(species_id=int(spid), element=el, best_tier_all=r['best_tier'], class_all=r['class'], threshold_class_all=r['threshold_class'], scope_all=sc_all,
                         best_tier_headline=bh['tier'] if bh else None, class_headline=bh['class'] if bh else None, threshold_class_headline=bh['threshold_class'] if bh else None, scope_headline=sc_h,
                         n_evidence_all=len(ev), n_evidence_headline=len(eh), evidence_types=' ; '.join(sorted(set(ev.evidence_type))), citations=' | '.join(dict.fromkeys(ev.citation)), in_headline=int(len(eh) > 0)))
    SPE = pd.DataFrame(rows)
    # ---- species
    rows = []
    envi = ENV.set_index('accepted_name')
    for sp, g in tx.groupby('species_level_name'):
        i = sid[sp]; s = SPE[SPE.species_id == i]; sh = s[s.in_headline == 1]
        names = sorted({n for x in g.name_as_published for n in x.split('; ') if n} | {sp} | set(g.wcvp_accepted_name))
        envs = ('ok' if envi.meets_20_cells.get(sp) == 'Y' else 'insufficient records') if sp in envi.index else 'not in occurrence set'
        rows.append(dict(species_id=i, name=sp, family=g.family.iloc[0], genus=sp.split(' ')[0].replace('×', '').strip() or sp.split(' ')[1], rank='species' if (g['rank'] == 'species').any() else 'infraspecific', n_taxa=len(g), taxa=json.dumps([dict(wcvp_id=int(r.wcvp_id), name=r.wcvp_accepted_name, rank=r.rank) for r in g.itertuples()]),
                         names_published=' ; '.join(names), search_text=' '.join(names).lower(), best_tier_all=min(s.best_tier_all, key=TIER_RANK.get), best_tier_headline=min(sh.best_tier_headline, key=TIER_RANK.get) if len(sh) else None,
                         elements_all=','.join(sorted(s.element)), elements_headline=','.join(sorted(sh.element)), n_evidence_all=int(s.n_evidence_all.sum()), n_evidence_headline=int(s.n_evidence_headline.sum()), in_headline=int(len(sh) > 0), env_status=envs))
    SPC = pd.DataFrame(rows)
    # ---- environment summary: >= 20 native cells only
    ok = ENV[ENV.meets_20_cells == 'Y'].copy(); ok['species_id'] = ok.accepted_name.map(sid)
    cols = ['species_id', 'accepted_name', 'wcvp_id', 'n_records', 'n_cells', 'regions', 'n_regions', 'bio1_median_C', 'bio1_q25', 'bio1_q75', 'bio12_median_mm', 'bio12_q25', 'bio12_q75', 'bio12_n_at_ceiling', 'ph_n_valid', 'ph_median', 'ph_q25', 'ph_q75', 'licence_basis', 'citation']
    EV = ok[cols].rename(columns={'accepted_name': 'name', 'wcvp_id': 'wcvp_species_id'}); EV['ultramafic'] = 'not assessed (no coverage outside the Americas)'
    # ---- evidence (public columns; no n_specimens, master_row_id, source_rows)
    ec = ['evidence_id', 'species_id', 'species_name', 'species', 'element', 'evidence_type', 'tier', 'scope', 'citation', 'doi', 'class', 'threshold_class', 'weakened', 'suspect_source', 'citation_inferred', 'citation_note', 'source_license', 'nc_derived', 'name_as_published', 'headline']
    EVD = E[ec].rename(columns={'species': 'taxon_name'}); EVD['species_id'] = EVD.species_id.astype(int)
    CV = C.rename(columns={'unique_species': 'unique_species'})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists(): OUT.unlink()
    con = sqlite3.connect(OUT)
    for name, df in (('species', SPC), ('species_element', SPE), ('evidence', EVD), ('environment_summary', EV), ('counts', CV)): df.to_sql(name, con, index=False)
    ver = [('release', 'HADB v1, release candidate 3 (rc3)'), ('rc3_manifest_sha256', sha(DR / 'release/MANIFEST.tsv')), ('gbif_doi', '10.15468/dl.kb25da'), ('gbif_citation', GBIF_CITATION), ('build_date', datetime.date.today().isoformat()),
           ('headline_view', 'Block B included; suspect-source, weakened and inferred-citation evidence dropped'), ('environment_basis', 'non-NC GBIF records, cleaned, one record per species per CHELSA cell, native only; species with >= 20 native cells'),
           ('release_licence', 'TBC'), ('species', str(len(SPC))), ('species_element_rows', str(len(SPE))), ('evidence_rows', str(len(EVD))), ('species_with_environment', str(len(EV)))]
    pd.DataFrame(ver, columns=['key', 'value']).to_sql('versions', con, index=False)
    cur = con.cursor()
    for sql in ('CREATE UNIQUE INDEX ix_sp_id ON species(species_id)', 'CREATE INDEX ix_sp_family ON species(family)', 'CREATE INDEX ix_sp_genus ON species(genus)', 'CREATE INDEX ix_sp_rank ON species(rank)', 'CREATE INDEX ix_spe ON species_element(species_id, element)',
                'CREATE INDEX ix_spe_el ON species_element(element, best_tier_headline)', 'CREATE INDEX ix_ev_sp ON evidence(species_id, element)', 'CREATE UNIQUE INDEX ix_env ON environment_summary(species_id)'): cur.execute(sql)
    con.commit(); con.close()
    print('hadb.sqlite: %d species, %d species_element, %d evidence, %d environment rows; %d bytes' % (len(SPC), len(SPE), len(EVD), len(EV), OUT.stat().st_size))
    print('species without a species-rank id:', int((SPC.n_taxa > 0).sum() - sum(1 for sp in sid if True)), '| env_status', SPC.env_status.value_counts().to_dict())


if __name__ == '__main__':
    main()
