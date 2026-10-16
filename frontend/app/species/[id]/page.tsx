import type { Metadata } from 'next';
import SpeciesClient from '@/components/SpeciesClient';

export const metadata: Metadata = { title: 'Species' };

export default async function SpeciesPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <SpeciesClient id={id} />;
}
