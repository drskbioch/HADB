import Image from 'next/image';
import Link from 'next/link';
import StatsStrip from '@/components/StatsStrip';
import { CORE_ELEMENTS, elementColor } from '@/lib/elements';

export default function Home() {
  return (
    <div>
      <section className="overflow-hidden rounded-lg bg-navy text-white">
        <Image src="/images/website-hadb.webp" alt="HADB banner: Hyperaccumulator Database title graphic" width={1900} height={828} priority className="h-auto w-full" />
        <div className="p-6">
          <h1 className="!text-white">HADB: a database of hyperaccumulator plants</h1>
          <p>HADB records which plant species are reported to accumulate or hyperaccumulate which chemical elements, with the evidence behind each statement, a tier for how strong that evidence is, and a summary of the climate and soil where the species grows. It records <strong>which</strong> elements, not how much.</p>
          <p className="mb-0"><Link href="/browse" className="btn">Browse the database</Link> <Link href="/about" className="ml-3 underline">About HADB</Link></p>
        </div>
      </section>
      <section aria-label="HADB in numbers" className="mt-6">
        <StatsStrip />
      </section>
      <section aria-labelledby="start" className="mt-6">
        <h2 id="start">Start with an element</h2>
        <ul className="flex flex-wrap gap-3">
          {CORE_ELEMENTS.map((e) => (
            <li key={e}><Link href={`/browse?element=${e}`} className="card flex w-28 items-center gap-2 hover:border-brand"><span aria-hidden="true" className="inline-block h-4 w-4 rounded-full" style={{ background: elementColor(e) }} /><span className="text-lg font-bold">{e}</span></Link></li>
          ))}
        </ul>
        <p className="mt-4">Or read how the evidence is graded in <Link href="/evidence-tiers" className="text-brand underline">Evidence and tiers</Link>, see the paper figures on the <Link href="/statistics" className="text-brand underline">Statistics</Link> page, or <Link href="/downloads" className="text-brand underline">download the data</Link>.</p>
      </section>
    </div>
  );
}
