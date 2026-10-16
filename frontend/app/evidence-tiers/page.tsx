import type { Metadata } from 'next';
import { TIER_TEXT } from '@/lib/elements';

export const metadata: Metadata = { title: 'Evidence and tiers' };

const THR = [['Ni', '1,000', '5,000'], ['Mn', '10,000', '20,000'], ['Co', '300', '1,000'], ['Zn', '3,000', '10,000']];

export default function EvidenceTiers() {
  return (
    <div>
      <h1>Evidence and tiers</h1>
      <h2>Tiers</h2>
      <ul className="list">{Object.values(TIER_TEXT).map((t) => (<li key={t}>{t}.</li>))}</ul>
      <p>A species is shown at its <strong>best</strong> tier for each element. T1 comes from the Gei et al. (2020) XRF tables and from paper tables with their own value; T2 from literature labels (Block B), the compiled lists of Gei et al. and values cited from earlier work.</p>
      <h2>Thresholds</h2>
      <p>Used only for T1 and for the threshold class (micrograms per gram dry mass, as in the sources).</p>
      <table className="data"><caption className="sr-only">Hyperaccumulation thresholds</caption><thead><tr><th scope="col">Element</th><th scope="col">Standard (low-range)</th><th scope="col">High-range (Gei et al. 2020)</th></tr></thead>
        <tbody>{THR.map((r) => (<tr key={r[0]}><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>))}</tbody></table>
      <p className="mt-3">The threshold class is <em>high-range</em> if the listed maximum of the taxon is at or above the high-range threshold, <em>standard</em> if at or above the standard one, and <em>label-only</em> if there is no concentration or the element has no threshold.</p>
      <h2>Scope</h2>
      <p>Scope tags the kind of source: <em>hyperaccumulation</em> (a hyperaccumulator screen or species table, or an article whose title contains &quot;hyperaccumulat&quot;), <em>phytoremediation</em> (title contains &quot;remediation&quot; or &quot;phytoextraction&quot;) and <em>unknown</em> (all other Block B rows). It is a tag, not a finding.</p>
      <h2>Headline view</h2>
      <p>The headline view is used for all counts: Block B is included, and evidence rows are left out when they come from a source that could not be read (suspect source), are printed as not confirmed in the source (weakened), or have a citation that was inferred (a DOI replaced after a title check). The Browse page can include them again.</p>
      <h2>Names</h2>
      <p>Names as published are matched to the WCVP (Kew) names table; synonyms resolve to the accepted name. Abbreviated genera (for example &quot;V. zizanioides&quot;) are accepted only when the same row or article gives the full genus; spelling corrections were accepted by explicit decision. Rows with no species name are kept in a separate list of unresolved names.</p>
      <h2>Environment</h2>
      <p>Occurrence records come from GBIF (non-commercial-licence records excluded), are cleaned, thinned to one record per species per 30 arc-second CHELSA cell, and restricted to the native range in the WCVP distribution. A species needs at least 20 native cells to receive statistics.</p>
    </div>
  );
}
