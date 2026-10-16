'use client';
import { useState } from 'react';
import Link from 'next/link';
import { ULTRAMAFIC_TEXT, SpeciesDetail } from '@/lib/api';
import { elementColor } from '@/lib/elements';
import { useApi } from '@/lib/useApi';
import ApiNote from './ApiNote';
import Citation from './Citation';

const num = (v: unknown, d = 1) => (typeof v === 'number' ? v.toFixed(d) : '');

export default function SpeciesClient({ id }: { id: string }) {
  const { data: s, error, loading } = useApi<SpeciesDetail>(`/api/v1/species/${encodeURIComponent(id)}`);
  const [onlyHeadline, setOnlyHeadline] = useState(true);
  if (loading) return <p aria-live="polite">Loading...</p>;
  if (error || !s) return error === 'not found' ? <div><h1>Species not found</h1><p><Link href="/browse" className="text-brand underline">Back to the database</Link></p></div> : <ApiNote message={error} />;
  const ev = s.evidence.filter((e) => !onlyHeadline || e.headline === 1);
  const env = s.environment;
  return (
    <article>
      <p className="text-sm"><Link href="/browse" className="text-brand underline">Database</Link> / {s.family}</p>
      <h1 className="italic">{s.name}</h1>
      <p><span className="chip">{s.family}</span> <span className="chip">best tier {s.best_tier_headline ?? s.best_tier_all}{s.best_tier_headline ? '' : ' (all evidence)'}</span> <span className="chip">WCVP id {s.species_id}</span> <span className="chip">{s.rank === 'species' ? 'species' : 'infraspecific taxa only'}</span></p>
      <section aria-labelledby="names"><h2 id="names">Names</h2>
        <p>Accepted name (WCVP): <em>{s.name}</em>. Names as published in the sources: {s.names_published.length ? s.names_published.map((n, i) => (<span key={n}>{i ? '; ' : ''}<em>{n}</em></span>)) : 'none recorded'}.</p>
        {s.taxa.length > 1 && <p>WCVP taxa folded into this species: {s.taxa.map((t) => `${t.name} (${t.rank}, id ${t.wcvp_id})`).join('; ')}.</p>}
      </section>
      <section aria-labelledby="elements"><h2 id="elements">Elements and tiers</h2>
        <div className="overflow-x-auto"><table className="data"><caption className="sr-only">Elements reported for this species</caption>
          <thead><tr><th scope="col">Element</th><th scope="col">Tier (headline / all)</th><th scope="col">Class</th><th scope="col">Threshold class</th><th scope="col">Scope</th><th scope="col">Evidence rows</th></tr></thead>
          <tbody>{s.elements.map((e) => (
            <tr key={e.element}><td><span className="chip"><span aria-hidden="true" className="inline-block h-2.5 w-2.5 rounded-full" style={{ background: elementColor(e.element) }} />{e.element}</span></td>
              <td>{e.best_tier_headline ?? 'none'} / {e.best_tier_all}</td><td>{e.class_headline ?? e.class_all}</td><td>{e.threshold_class_headline ?? e.threshold_class_all}</td><td>{e.scope_headline ?? e.scope_all}</td><td>{e.n_evidence_headline} / {e.n_evidence_all}</td></tr>))}</tbody></table></div>
      </section>
      <section aria-labelledby="evidence"><h2 id="evidence">Evidence ({ev.length} rows shown)</h2>
        <label className="mb-2 flex items-center gap-2 text-sm"><input type="checkbox" checked={onlyHeadline} onChange={(e) => setOnlyHeadline(e.target.checked)} /> headline view only (hide suspect-source, weakened and inferred-citation rows)</label>
        <div className="overflow-x-auto"><table className="data"><caption className="sr-only">Evidence rows</caption>
          <thead><tr><th scope="col">Element</th><th scope="col">Source type</th><th scope="col">Tier</th><th scope="col">Scope</th><th scope="col">Name as published</th><th scope="col">Citation</th><th scope="col">Flags</th></tr></thead>
          <tbody>{ev.map((e) => (
            <tr key={e.evidence_id}><td>{e.element}</td><td>{e.evidence_type.replace(/_/g, ' ')}</td><td>{e.tier}</td><td>{e.scope}</td><td className="italic">{e.name_as_published}</td>
              <td><Citation text={e.citation} />{e.citation_note ? <div className="text-xs text-gray-600">{e.citation_note}</div> : null}</td>
              <td className="text-xs">{[e.weakened === 'Y' && 'not confirmed in source', e.suspect_source === 'Y' && 'suspect source', e.citation_inferred === 'Y' && 'citation inferred'].filter(Boolean).join('; ') || ''}</td></tr>))}</tbody></table></div>
      </section>
      <section aria-labelledby="env"><h2 id="env">Environment</h2>
        {env ? (
          <div>
            <p>Where the species was recorded in its native range (non-NC GBIF records, cleaned, one record per CHELSA cell): {String(env.n_cells)} native cells in {String(env.regions)}.</p>
            <table className="data"><caption className="sr-only">Environment summary</caption><thead><tr><th scope="col">Variable</th><th scope="col">Median</th><th scope="col">25th to 75th percentile</th></tr></thead>
              <tbody>
                <tr><td>Mean annual temperature, bio1 (degrees C)</td><td>{num(env.bio1_median_C)}</td><td>{num(env.bio1_q25)} to {num(env.bio1_q75)}</td></tr>
                <tr><td>Annual precipitation, bio12 (mm)</td><td>{num(env.bio12_median_mm, 0)}</td><td>{num(env.bio12_q25, 0)} to {num(env.bio12_q75, 0)}</td></tr>
                <tr><td>Soil pH (water, 0-5 cm)</td><td>{num(env.ph_median, 2)}</td><td>{num(env.ph_q25, 2)} to {num(env.ph_q75, 2)}</td></tr>
              </tbody></table>
            {Number(env.bio12_n_at_ceiling) > 0 && <p className="note mt-3">bio12 is saturated at 6,553.5 mm in {String(env.bio12_n_at_ceiling)} cells of this species; the true value there is higher.</p>}
          </div>
        ) : (<p>{s.environment_status}.</p>)}
        <p>Ultramafic substrate: {ULTRAMAFIC_TEXT}.</p>
      </section>
      <section aria-labelledby="cite"><h2 id="cite">How to cite the occurrence data</h2><p>{s.occurrence_citation}</p><p className="text-sm text-gray-700">Licence of this release: {s.licence}</p></section>
    </article>
  );
}
