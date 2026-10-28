'use client';
// Home page: the largest plant families by species in the headline view, as horizontal bars; each row links to Browse filtered by that family.
import Link from 'next/link';
import { useApi } from '@/lib/useApi';
import ApiNote from './ApiNote';

type Family = { family: string; species: number; species_headline: number };

const SHOWN = 8;

export default function FamilyList() {
  const { data, error, loading } = useApi<{ total: number; items: Family[] }>('/api/v1/families');
  if (loading) return <p aria-live="polite">Loading families...</p>;
  if (error || !data) return <ApiNote message={error} />;
  const top = [...data.items].sort((a, b) => b.species_headline - a.species_headline).slice(0, SHOWN);
  const max = top[0]?.species_headline || 1;
  return (
    <>
      <p>The {top.length} largest of {data.total.toLocaleString('en-US')} plant families in the headline view. Select one to browse its species.</p>
      <ul className="grid gap-x-8 gap-y-1.5 lg:grid-cols-2">
        {top.map((f) => (
          <li key={f.family} className="max-w-none">
            <Link href={`/browse?family=${encodeURIComponent(f.family)}`} className="grid grid-cols-[8.5rem_1fr_2rem] items-center gap-3 rounded-lg px-2 py-1 hover:bg-sky">
              <span className="truncate font-semibold text-brand">{f.family}</span>
              <span aria-hidden="true" className="h-3 overflow-hidden rounded-full bg-gray-200">
                <span className="block h-full rounded-full bg-accent" style={{ width: `${(f.species_headline / max) * 100}%` }} />
              </span>
              <span className="text-right text-sm font-bold text-navy">{f.species_headline.toLocaleString('en-US')}<span className="sr-only"> species</span></span>
            </Link>
          </li>
        ))}
      </ul>
    </>
  );
}
