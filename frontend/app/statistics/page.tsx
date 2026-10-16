import fs from 'fs';
import path from 'path';
import Image from 'next/image';
import type { Metadata } from 'next';

export const metadata: Metadata = { title: 'Statistics' };

const FIGS = [
  { n: 2, title: 'Figure 2. Evidence in HADB', text: 'Species per element and tier, evidence sources, overlap of sources for Ni, threshold classes, families, citation concentration, scope and the new-versus-known counts of the three screens.' },
  { n: 3, title: 'Figure 3. Names, thresholds and the headline view', text: 'How the Block B rows were resolved to names, match types and their similarity, the reconciliation to evidence rows, thresholds in the Gei screen, what the headline view removes, licences and family by element.' },
  { n: 4, title: 'Figure 4. The occurrence records', text: 'Density of cleaned native cells, records per species, the cleaning steps, native regions, source regions, basis of record, licences, collection year and latitude by element.' },
  { n: 5, title: 'Figure 5. Climate and soil', text: 'Temperature, precipitation and soil pH by element for species with at least 20 native cells, climate space, completeness of the environment data, families, PCA, T1 versus T2 and data-rich species.' },
];

export default function Statistics() {
  const dir = path.join(process.cwd(), 'public', 'figures');
  return (
    <div>
      <h1>Statistics: Figures 2 to 5</h1>
      <p>The figures of the paper (web copies, 1600 pixels wide). No individual occurrence records or coordinates are shown, only summaries.</p>
      {FIGS.map((f) => {
        const file = `figure${f.n}.png`;
        const have = fs.existsSync(path.join(dir, file));
        return (
          <section key={f.n} aria-labelledby={`f${f.n}`} className="mb-10">
            <h2 id={`f${f.n}`}>{f.title}</h2>
            {have ? (
              <Image src={`/figures/${file}`} alt={`${f.title}. ${f.text}`} width={1600} height={Math.round(1600 * (f.n < 4 ? 11160 : 11280) / 8640)} className="h-auto w-full max-w-3xl rounded border border-gray-200" />
            ) : (
              <div role="img" aria-label={`${f.title} (placeholder)`} className="flex h-64 max-w-3xl items-center justify-center rounded border-2 border-dashed border-gray-400 bg-sky p-4 text-center text-sm text-gray-700">Figure {f.n} will appear here when the web copy is added (run scripts/copy_figures.py).</div>
            )}
            <p className="mt-2 text-sm">{f.text}</p>
          </section>
        );
      })}
      <p className="note">Caveats: screening bias; non-commercial GBIF records are excluded; capitals and institutions were not tested in the cleaning; bio12 is saturated at 6,553.5 mm in the wettest places; ultramafic status is not assessed (no coverage outside the Americas) and is not shown.</p>
    </div>
  );
}
