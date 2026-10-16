import { Suspense } from 'react';
import type { Metadata } from 'next';
import BrowseClient from '@/components/BrowseClient';

export const metadata: Metadata = { title: 'Browse the database' };

export default function BrowsePage() {
  return (
    <div>
      <h1>Browse the database</h1>
      <p>Search by name and filter by element, tier, scope, family and rank. The element, family and tier shortcuts in the sidebar are saved filters of this page. The headline view leaves out evidence from a source that could not be read, rows marked as not confirmed, and rows whose citation was inferred; switch to &quot;all evidence&quot; to include them.</p>
      <Suspense fallback={<p>Loading filters...</p>}><BrowseClient /></Suspense>
    </div>
  );
}
