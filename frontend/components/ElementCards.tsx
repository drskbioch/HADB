'use client';
// Home page: one card per headline element with the species count and the T1/T2/T3 split; each links to Browse filtered by that element.
import Link from 'next/link';
import { useApi } from '@/lib/useApi';
import { elementColor, SIDEBAR_ELEMENTS } from '@/lib/elements';
import ApiNote from './ApiNote';

type Row = { element: string; species_headline: number; t1_headline: number; t2_headline: number; t3_headline: number };

const TIER_BAR = ['bg-navy', 'bg-accent', 'bg-gray-400'];

export default function ElementCards() {
  const { data, error, loading } = useApi<{ items: Row[] }>('/api/v1/elements');
  if (loading) return <p aria-live="polite">Loading elements...</p>;
  if (error || !data) return <ApiNote message={error} />;
  const rows = SIDEBAR_ELEMENTS.map((e) => data.items.find((r) => r.element === e)).filter((r): r is Row => !!r);
  return (
    <ul className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
      {rows.map((r) => {
        const tiers = [r.t1_headline, r.t2_headline, r.t3_headline];
        const total = tiers.reduce((a, b) => a + b, 0) || 1;
        return (
          <li key={r.element} className="max-w-none">
            <Link href={`/browse?element=${r.element}`} className="card flex h-full flex-col gap-2 hover:border-brand">
              <span className="flex items-center gap-2">
                <span aria-hidden="true" className="inline-block h-4 w-4 rounded-full" style={{ background: elementColor(r.element) }} />
                <span className="text-2xl font-bold text-navy">{r.element}</span>
                <span className="ml-auto text-sm text-gray-700"><strong className="text-lg text-brand">{r.species_headline.toLocaleString('en-US')}</strong> species</span>
              </span>
              <span aria-hidden="true" className="flex h-2.5 overflow-hidden rounded-full bg-gray-200">
                {tiers.map((n, i) => (n > 0 ? <span key={i} className={TIER_BAR[i]} style={{ width: `${(n / total) * 100}%` }} /> : null))}
              </span>
              <span className="text-xs text-gray-700">T1 {r.t1_headline} · T2 {r.t2_headline} · T3 {r.t3_headline}</span>
            </Link>
          </li>
        );
      })}
    </ul>
  );
}
