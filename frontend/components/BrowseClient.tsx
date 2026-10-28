'use client';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { ElementRow, SpeciesList } from '@/lib/api';
import { elementColor, SCOPES, TIERS } from '@/lib/elements';
import { useApi } from '@/lib/useApi';
import ApiNote from './ApiNote';

const KEYS = ['q', 'element', 'tier', 'scope', 'family', 'rank', 'view', 'page', 'page_size'] as const;

export default function BrowseClient() {
  const sp = useSearchParams();
  const router = useRouter();
  const get = (k: string) => sp.get(k) ?? '';
  const params = { q: get('q'), element: get('element'), tier: get('tier'), scope: get('scope'), family: get('family'), rank: get('rank'), view: get('view') || 'headline', page: get('page') || '1', page_size: get('page_size') || '25' };
  const list = useApi<SpeciesList>('/api/v1/species', params);
  const els = useApi<{ items: ElementRow[] }>('/api/v1/elements');
  const [draft, setDraft] = useState<Record<string, string>>(Object.fromEntries(KEYS.map((k) => [k, get(k)])));
  const set = (k: string, v: string) => setDraft((d) => ({ ...d, [k]: v }));

  function go(next: Record<string, string>) {
    const u = new URLSearchParams();
    for (const k of KEYS) if (next[k]) u.set(k, next[k]);
    router.push('/browse' + (u.toString() ? '?' + u.toString() : ''));
  }
  function submit(e: FormEvent) { e.preventDefault(); go({ ...draft, page: '1' }); }
  const page = Number(params.page); const total = list.data?.total ?? 0; const ps = Number(params.page_size); const pages = Math.max(1, Math.ceil(total / ps));
  const field = 'mt-1 block w-full rounded border border-gray-400 bg-white px-2 py-1.5 text-sm';

  return (
    <div>
      <form onSubmit={submit} className="card mb-4 grid gap-3 md:grid-cols-4" aria-label="Filters">
        <label className="text-sm font-semibold md:col-span-2">Name search (species, genus or published name)
          <input className={field} type="search" value={draft.q} maxLength={80} onChange={(e) => set('q', e.target.value)} placeholder="for example Noccaea" />
        </label>
        <label className="text-sm font-semibold">Element
          <select className={field} value={draft.element} onChange={(e) => set('element', e.target.value)}>
            <option value="">all elements</option>
            {(els.data?.items ?? []).map((e) => (<option key={e.element} value={e.element}>{e.element} ({e.species_headline})</option>))}
          </select>
        </label>
        <label className="text-sm font-semibold">Tier
          <select className={field} value={draft.tier} onChange={(e) => set('tier', e.target.value)}><option value="">all tiers</option>{TIERS.map((t) => (<option key={t} value={t}>{t}</option>))}</select>
        </label>
        <label className="text-sm font-semibold">Scope
          <select className={field} value={draft.scope} onChange={(e) => set('scope', e.target.value)}><option value="">all scopes</option>{SCOPES.map((t) => (<option key={t} value={t}>{t}</option>))}</select>
        </label>
        <label className="text-sm font-semibold">Family
          <input className={field} value={draft.family} maxLength={60} onChange={(e) => set('family', e.target.value)} placeholder="for example Cunoniaceae" />
        </label>
        <label className="text-sm font-semibold">Rank
          <select className={field} value={draft.rank} onChange={(e) => set('rank', e.target.value)}><option value="">any</option><option value="species">species</option><option value="infraspecific">infraspecific only</option></select>
        </label>
        <label className="text-sm font-semibold">View
          <select className={field} value={draft.view || 'headline'} onChange={(e) => set('view', e.target.value)}><option value="headline">headline view</option><option value="all">all evidence</option></select>
        </label>
        <div className="flex items-end gap-3 md:col-span-4">
          <button type="submit" className="btn">Apply filters</button>
          <button type="button" className="rounded border border-gray-400 px-4 py-2 text-sm" onClick={() => { setDraft(Object.fromEntries(KEYS.map((k) => [k, '']))); go({}); }}>Clear</button>
        </div>
      </form>
      <p className="text-sm text-gray-700" aria-live="polite">{list.loading ? 'Loading...' : list.data ? `${total.toLocaleString('en-US')} species found (${params.view} view)` : ''}</p>
      {list.error && <ApiNote message={list.error} />}
      {list.data && (
        <div className="overflow-x-auto">
          <table className="data">
            <caption className="sr-only">Species matching the filters</caption>
            <thead><tr><th scope="col">Species</th><th scope="col">Family</th><th scope="col">Best tier</th><th scope="col">Elements</th><th scope="col">Evidence rows</th></tr></thead>
            <tbody>
              {list.data.items.map((s) => (
                <tr key={s.species_id}>
                  <td><Link href={`/species/${s.species_id}`} className="font-semibold italic text-brand underline">{s.name}</Link></td>
                  <td>{s.family}</td>
                  <td><span className="chip">{s.best_tier ?? 'none'}</span></td>
                  <td className="space-x-1">{s.elements.slice(0, 8).map((e) => (<span key={e} className="chip"><span aria-hidden="true" className="inline-block h-2.5 w-2.5 rounded-full" style={{ background: elementColor(e) }} />{e}</span>))}{s.elements.length > 8 && <span className="text-xs">+{s.elements.length - 8}</span>}</td>
                  <td>{s.n_evidence}</td>
                </tr>
              ))}
              {list.data.items.length === 0 && <tr><td colSpan={5}>No species match these filters.</td></tr>}
            </tbody>
          </table>
        </div>
      )}
      {list.data && (
        <nav aria-label="Pagination" className="mt-4 flex items-center gap-3 text-sm">
          <button type="button" className="rounded border border-gray-400 px-3 py-1 disabled:opacity-40" disabled={page <= 1} onClick={() => go({ ...params, ...{ page: String(page - 1) } } as Record<string, string>)}>Previous</button>
          <span>Page {page} of {pages}</span>
          <button type="button" className="rounded border border-gray-400 px-3 py-1 disabled:opacity-40" disabled={page >= pages} onClick={() => go({ ...params, ...{ page: String(page + 1) } } as Record<string, string>)}>Next</button>
        </nav>
      )}
    </div>
  );
}
