import type { Metadata } from 'next';
import { API_BASE } from '@/lib/api';

export const metadata: Metadata = { title: 'API documentation' };

const EP = [
  ['GET /api/v1/species', 'q, element, tier (T1|T2|T3), scope, family, genus, rank (species|infraspecific), view (headline|all), page, page_size (max 100)', 'Paged list of species with best tier, elements, evidence rows and environment status.'],
  ['GET /api/v1/species/{wcvp_id}', 'wcvp_id: integer', 'One species: names, taxa, elements, evidence, environment summary or "insufficient records", ultramafic status ("not assessed"), citation.'],
  ['GET /api/v1/elements', '', 'Species per element by best tier.'], ['GET /api/v1/families', 'page, page_size', 'Families with species counts.'], ['GET /api/v1/stats', '', 'Totals and headline counts by element and tier.'],
  ['GET /api/v1/versions', '', 'Release, rc3 manifest hash, GBIF DOI, build date, licence status.'], ['GET /api/v1/downloads', '', 'Public files with SHA256.'], ['GET /api/v1/downloads/{name}', 'name from the list', 'The file itself.'],
  ['GET /api/v1/health', '', 'Service status.'], ['GET /api/v1/openapi.json', '', 'OpenAPI description.'],
];

export default function ApiDocs() {
  return (
    <div>
      <h1>API documentation</h1>
      <p>Read-only JSON API. Base URL of this site&apos;s API: <code className="rounded bg-sky px-1">{API_BASE}</code>. Public scope: species, elements, classes, tiers, scopes, citations, names and environment summaries. There are no concentration values, no occurrence points and no coordinates. Inputs are validated; list calls return at most 100 items per page; requests are rate limited.</p>
      <div className="overflow-x-auto"><table className="data"><caption className="sr-only">Endpoints</caption><thead><tr><th scope="col">Endpoint</th><th scope="col">Parameters</th><th scope="col">Returns</th></tr></thead>
        <tbody>{EP.map((e) => (<tr key={e[0]}><td className="whitespace-nowrap font-mono text-xs">{e[0]}</td><td>{e[1]}</td><td>{e[2]}</td></tr>))}</tbody></table></div>
      <h2>Examples</h2>
      <pre className="overflow-x-auto rounded bg-sky p-3 text-xs">{`curl "${API_BASE}/api/v1/species?element=Ni&tier=T1&page_size=10"
curl "${API_BASE}/api/v1/species?q=Noccaea"
curl "${API_BASE}/api/v1/versions"`}</pre>
      <p>Machine-readable description: <a className="text-brand underline" href={`${API_BASE}/api/v1/openapi.json`}>openapi.json</a>.</p>
    </div>
  );
}
