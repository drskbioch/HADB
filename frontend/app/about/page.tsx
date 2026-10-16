import type { Metadata } from 'next';
import Link from 'next/link';
import StatsStrip from '@/components/StatsStrip';
import { GBIF_CITATION, ULTRAMAFIC_TEXT } from '@/lib/api';

export const metadata: Metadata = { title: 'About' };

export default function About() {
  return (
    <div>
      <h1>About HADB</h1>
      <p>HADB (Hyperaccumulator Database) is a table of which plant species are reported to accumulate or hyperaccumulate which chemical elements, with the evidence behind each statement. Version 1 was built from the literature-mined HADB table (Block B), the species tables of Gei et al. (2020) for New Caledonia, and two regional papers (Sabah and Queensland).</p>
      <StatsStrip />
      <h2>Contents</h2>
      <ul className="list">
        <li><strong>Species and elements:</strong> accepted WCVP names (Kew), the names as published, the element, a tier (T1 to T3), the class and threshold class of the strongest evidence, and the scope of the source.</li>
        <li><strong>Evidence:</strong> every citation behind a statement, with PMID or DOI links, and flags for rows from a source that could not be read, rows marked as not confirmed in the source, and rows whose citation was inferred.</li>
        <li><strong>Environment summaries:</strong> for species with at least 20 native occurrence cells, the median and quartiles of mean annual temperature (CHELSA bio1), annual precipitation (CHELSA bio12) and soil pH (SoilGrids). Other species are shown as &quot;insufficient records&quot; and have no statistics.</li>
        <li><strong>Counts and downloads:</strong> unique species per element by tier, the figures of the paper, and the release files with checksums.</li>
      </ul>
      <h2>Functions of the web interface</h2>
      <ul className="list">
        <li><Link href="/browse" className="text-brand underline">Browse</Link>: search by name, filter by element, tier, scope, family and rank; the element, family and tier shortcuts in the sidebar are saved filters.</li>
        <li>Species pages: names, evidence with links, tier and scope per element, and the environment summary.</li>
        <li><Link href="/statistics" className="text-brand underline">Statistics</Link>: Figures 2 to 5 of the paper. <Link href="/downloads" className="text-brand underline">Downloads</Link> and the <Link href="/api-docs" className="text-brand underline">API</Link> give the same data as files and as JSON.</li>
      </ul>
      <h2>Usage cases</h2>
      <ul className="list">
        <li>Which species have a taxon-level measurement above the threshold for Ni, and in which families do they cluster?</li>
        <li>Which candidate species for phytoremediation or phytomining grow in a given climate or soil pH range?</li>
        <li>How strong is the evidence behind a species listed as a hyperaccumulator, and which article is it from?</li>
      </ul>
      <h2>Limitations</h2>
      <ul className="list">
        <li>HADB records <strong>which</strong> elements, not how much. Only the Gei et al. and paper rows carry thresholds (tier T1).</li>
        <li>Most Block B rows are second-hand extractions from reviews; one review supplies about a third of the evidence rows. The manual audit of Block B is not coded, so its error rate is unknown. Species appear because a screen or review reported them (screening bias).</li>
        <li>There is no measured negative set: absence from HADB is not evidence of absence.</li>
        <li>Scope (hyperaccumulation, phytoremediation, unknown) is unknown for most Block B rows.</li>
        <li>Environment: built from GBIF records under CC0 and CC BY only (CC BY-NC records are excluded); cleaning did not test country capitals or institution coordinates; 64.6% of the final native cells have no recorded coordinate uncertainty (kept, flagged). Only species with at least 20 native cells have statistics (198 of 279 species in v1); the others show &quot;insufficient records&quot;.</li>
        <li>CHELSA bio12 is saturated at 6,553.5 mm in the wettest places (20 native cells of the primary basis in v1); the true rainfall there is higher. Soil pH is SoilGrids stored value divided by 10; some cells have no value.</li>
        <li>Ultramafic substrate: {ULTRAMAFIC_TEXT}. The available layers cover the Americas only, so it is never shown as zero.</li>
        <li>The native-range filter follows the WCVP distribution; for example <em>Noccaea caerulescens</em> is listed as introduced in Scandinavia and <em>Nicotiana tabacum</em> as native only in Bolivia, so those species have few native cells.</li>
      </ul>
      <p className="note">Occurrence data: {GBIF_CITATION}</p>
    </div>
  );
}
