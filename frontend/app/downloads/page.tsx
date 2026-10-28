'use client';
import { API_BASE, DownloadItem, RELEASE_LICENSE } from '@/lib/api';
import { useApi } from '@/lib/useApi';
import ApiNote from '@/components/ApiNote';

export default function Downloads() {
  const { data, error, loading } = useApi<{ licence: string; zenodo_doi: string; items: DownloadItem[] }>('/api/v1/downloads');
  return (
    <div>
      <h1>Downloads</h1>
      <p>Release files of HADB v1. Check the SHA256 after download. Record-level occurrence data are not distributed here; cite the GBIF download instead (see <a className="text-brand underline" href="/citation">Citation</a>).</p>
      <p className="note">Release licence: {RELEASE_LICENSE}.</p>
      {loading && <p aria-live="polite">Loading the file list...</p>}
      {error && <ApiNote message={error} />}
      {data && (
        <div className="overflow-x-auto"><table className="data"><caption className="sr-only">Release files</caption>
          <thead><tr><th scope="col">File</th><th scope="col">What it is</th><th scope="col">Size (bytes)</th><th scope="col">SHA256</th></tr></thead>
          <tbody>{data.items.filter((d) => !d.name.toLowerCase().endsWith('.md')).map((d) => (
            <tr key={d.name}><td><a className="font-semibold text-brand underline" href={`${API_BASE}/api/v1/downloads/${encodeURIComponent(d.name)}`}>{d.name}</a></td><td>{d.description}</td><td>{d.bytes.toLocaleString('en-US')}</td><td className="break-all font-mono text-xs">{d.sha256}</td></tr>))}</tbody></table></div>
      )}
    </div>
  );
}
