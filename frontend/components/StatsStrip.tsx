'use client';
import { useApi } from '@/lib/useApi';
import ApiNote from './ApiNote';

type Stats = { species: number; species_headline: number; species_with_environment: number; versions: Record<string, string> };

export default function StatsStrip() {
  const { data, error, loading } = useApi<Stats>('/api/v1/stats');
  if (loading) return <p aria-live="polite">Loading numbers from the database...</p>;
  if (error || !data) return <ApiNote message={error} />;
  const items = [
    ['Species in the database', data.species.toLocaleString('en-US')], ['Species in the headline view', data.species_headline.toLocaleString('en-US')],
    ['Species with environment summary', data.species_with_environment.toLocaleString('en-US')],
  ];
  return (
    <dl className="grid grid-cols-2 gap-3 md:grid-cols-3">
      {items.map(([k, v]) => (<div key={k} className="card"><dt className="text-xs uppercase tracking-wide text-gray-600">{k}</dt><dd className="mt-1 text-2xl font-bold text-brand">{v}</dd></div>))}
    </dl>
  );
}
