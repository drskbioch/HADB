'use client';
import { GBIF_CITATION, RELEASE_LICENSE } from '@/lib/api';
import { useApi } from '@/lib/useApi';
import ApiNote from '@/components/ApiNote';

const HISTORY = [
  ['rc3', 'Name decisions re-checked: abbreviated genera accepted only when the row or article gives the full genus; environment summaries from non-NC GBIF records added.'],
  ['rc2', 'Region-test name decisions, row accountability and key checks in the validator, headline view with suspect-source, weakened and inferred-citation evidence removed.'],
  ['rc1', 'First release candidate built from the Block B table, Gei et al. (2020) and the two regional papers.'],
];

export default function Citation() {
  const { data, error } = useApi<Record<string, string>>('/api/v1/versions');
  return (
    <div>
      <h1>Citation and versions</h1>
      <h2>How to cite</h2>
      <p>HADB: Hyperaccumulator Database, version 1. Plant &amp; Cell Physiology database paper (in preparation). Zenodo DOI: to be added. Release licence: {RELEASE_LICENSE === 'TBC' ? 'to be confirmed (TBC)' : RELEASE_LICENSE}.</p>
      <p>Occurrence data used for the environment summaries: <strong>{GBIF_CITATION}</strong></p>
      <p>Please also cite the sources of the evidence you use; every evidence row carries its citation (PMID or DOI). Names follow the World Checklist of Vascular Plants (WCVP, Royal Botanic Gardens, Kew); climate is CHELSA V2.1, soil pH is SoilGrids 2.0, regions are WGSRPD (TDWG).</p>
      <h2>This version</h2>
      {error && <ApiNote message={error} />}
      {data && (<dl className="grid max-w-3xl grid-cols-[12rem_1fr] gap-y-1 text-sm">{Object.entries(data).map(([k, v]) => (<div key={k} className="contents"><dt className="font-semibold">{k.replace(/_/g, ' ')}</dt><dd className="break-all">{v}</dd></div>))}</dl>)}
      <h2>Version history</h2>
      <ul className="list">{HISTORY.map((h) => (<li key={h[0]}><strong>{h[0]}</strong>: {h[1]}</li>))}</ul>
    </div>
  );
}
