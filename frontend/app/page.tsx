import Link from 'next/link';
import ElementCards from '@/components/ElementCards';
import StatsStrip from '@/components/StatsStrip';

export default function Home() {
  return (
    <div>
      <section className="overflow-hidden rounded-2xl border border-accent/40 bg-sky">
        <div className="p-6">
          <h1>HADB: a database of hyperaccumulator plants</h1>
          <p>HADB records which plant species are reported to accumulate or hyperaccumulate which chemical elements, with the evidence behind each statement, a tier for how strong that evidence is, and a summary of the climate and soil where the species grows. It records <strong>which</strong> elements, not how much.</p>
          <p className="mb-0"><Link href="/browse" className="btn">Browse the database</Link> <Link href="/about" className="ml-3 underline">About HADB</Link></p>
        </div>
      </section>
      <section aria-label="HADB in numbers" className="mt-6">
        <StatsStrip />
      </section>
      <section aria-labelledby="start" className="mt-6">
        <h2 id="start">Start with an element</h2>
        <p>Each card shows the species with that element in the headline view, split by evidence tier (T1 strongest). Select one to browse its species.</p>
        <ElementCards />
        <p className="mt-4">Or read how the evidence is graded in <Link href="/evidence-tiers" className="text-brand underline">Evidence and tiers</Link> or <Link href="/downloads" className="text-brand underline">download the data</Link>.</p>
      </section>
    </div>
  );
}
