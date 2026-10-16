// API access. Pages never fetch at build time: every call happens in the browser (client components), so the build passes with the API unreachable.
export const API_BASE = (process.env.NEXT_PUBLIC_API_BASE ?? (process.env.NODE_ENV === 'production' ? 'https://api.habdsk.org' : 'http://localhost:8000')).replace(/\/$/, '');
export const RELEASE_LICENSE = process.env.NEXT_PUBLIC_RELEASE_LICENSE ?? 'CC BY 4.0';
export const GBIF_CITATION = 'GBIF.org (13 October 2026) GBIF Occurrence Download https://doi.org/10.15468/dl.kb25da';
export const ULTRAMAFIC_TEXT = 'not assessed (no coverage outside the Americas)';

export type Params = Record<string, string | number | undefined | null>;

export async function api<T>(path: string, params?: Params, signal?: AbortSignal): Promise<T> {
  const url = new URL(API_BASE + path);
  if (params) for (const [k, v] of Object.entries(params)) if (v !== undefined && v !== null && v !== '') url.searchParams.set(k, String(v));
  const res = await fetch(url.toString(), { signal, headers: { Accept: 'application/json' } });
  if (!res.ok) throw new Error(res.status === 404 ? 'not found' : res.status === 422 ? 'invalid request' : `API error ${res.status}`);
  return (await res.json()) as T;
}

export type SpeciesItem = {
  species_id: number; name: string; family: string; genus: string; rank: string; best_tier: string | null; elements: string[]; n_evidence: number; env_status: string;
};
export type SpeciesList = { total: number; page: number; page_size: number; view: string; items: SpeciesItem[] };
export type ElementRow = { element: string; species_all: number; species_headline: number; t1_headline: number; t2_headline: number; t3_headline: number };
export type EvidenceRow = {
  evidence_id: string; taxon_name: string; element: string; evidence_type: string; tier: string; scope: string; citation: string; doi: string; class: string; threshold_class: string;
  weakened: string; suspect_source: string; citation_inferred: string; citation_note: string; name_as_published: string; source_license: string; headline: number;
};
export type ElementEvidence = {
  element: string; best_tier_headline: string | null; best_tier_all: string; class_headline: string | null; class_all: string; threshold_class_headline: string | null; threshold_class_all: string;
  scope_headline: string | null; scope_all: string; n_evidence_headline: number; n_evidence_all: number; in_headline: number;
};
export type Environment = Record<string, string | number | null>;
export type SpeciesDetail = {
  species_id: number; name: string; family: string; genus: string; rank: string; n_taxa: number; taxa: { wcvp_id: number; name: string; rank: string }[]; names_published: string[];
  best_tier_headline: string | null; best_tier_all: string; elements: ElementEvidence[]; evidence: EvidenceRow[]; environment: Environment | null; environment_status: string;
  ultramafic: string; occurrence_citation: string; licence: string;
};
export type DownloadItem = { name: string; bytes: number; sha256: string; description: string; version: string };
