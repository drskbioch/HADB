'use client';
// Top navigation + left sidebar (quick links to all pages, element shortcuts, tier filters). The sidebar collapses on mobile.
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { elementColor, FAMILIES, SIDEBAR_ELEMENTS, TIERS } from '@/lib/elements';
import { RELEASE_LICENSE } from '@/lib/api';

const TOP = [
  { href: '/', label: 'Home' }, { href: '/about', label: 'About' }, { href: '/browse', label: 'Database' }, { href: '/statistics', label: 'Statistics' },
  { href: '/downloads', label: 'Downloads' }, { href: '/api-docs', label: 'API' }, { href: '/contact', label: 'Contact Us' },
];
const PAGES = [
  { href: '/', label: 'Home' }, { href: '/about', label: 'About' }, { href: '/browse', label: 'Browse the database' }, { href: '/statistics', label: 'Statistics (Figures 2 to 5)' },
  { href: '/evidence-tiers', label: 'Evidence and tiers' }, { href: '/downloads', label: 'Downloads' }, { href: '/api-docs', label: 'API documentation' }, { href: '/citation', label: 'Citation and versions' },
  { href: '/contact', label: 'Contact Us' },
];

function cls(...a: (string | false)[]) { return a.filter(Boolean).join(' '); }

export default function Shell({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  const [open, setOpen] = useState(false);
  const link = 'block rounded px-2 py-1 hover:bg-sky focus-visible:outline focus-visible:outline-2 focus-visible:outline-brand';
  return (
    <div className="flex min-h-screen flex-col bg-white text-ink">
      <a href="#content" className="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:z-50 focus:rounded focus:bg-white focus:p-2 focus:text-brand">Skip to content</a>
      <header className="bg-navy text-white">
        <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-3">
          <button type="button" className="rounded border border-white/60 px-3 py-1 text-sm md:hidden" aria-expanded={open} aria-controls="sidebar" onClick={() => setOpen(!open)}>
            {open ? 'Close menu' : 'Menu'}
          </button>
          <Link href="/" className="text-xl font-bold tracking-wide focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent">
            HADB <span className="hidden text-sm font-normal text-accent sm:inline">Hyperaccumulator Database</span>
          </Link>
          <nav aria-label="Main" className="ml-auto hidden md:block">
            <ul className="flex gap-1">
              {TOP.map((t) => (
                <li key={t.href}>
                  <Link href={t.href} aria-current={path === t.href ? 'page' : undefined}
                    className={cls('rounded px-3 py-1.5 text-sm hover:bg-white/15 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent', path === t.href && 'bg-white/20 font-semibold')}>
                    {t.label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </div>
        <div className="h-1 bg-accent" aria-hidden="true" />
      </header>
      <div className="mx-auto flex w-full max-w-7xl flex-1 flex-col md:flex-row">
        <aside id="sidebar" aria-label="Quick links" className={cls('border-b border-gray-200 bg-sky p-4 text-sm md:block md:w-64 md:shrink-0 md:border-b-0 md:border-r', open ? 'block' : 'hidden')}>
          <nav aria-label="Pages">
            <h2 className="mb-1 text-xs font-bold uppercase tracking-wide text-navy">Pages</h2>
            <ul className="mb-4">{PAGES.map((p) => (<li key={p.href}><Link href={p.href} className={cls(link, path === p.href && 'font-semibold text-brand')} onClick={() => setOpen(false)}>{p.label}</Link></li>))}</ul>
          </nav>
          <nav aria-label="Elements">
            <h2 className="mb-1 text-xs font-bold uppercase tracking-wide text-navy">Elements</h2>
            <ul className="mb-4 flex flex-wrap gap-2">
              {SIDEBAR_ELEMENTS.map((e) => (
                <li key={e}><Link href={`/browse?element=${e}`} className="inline-flex items-center gap-1 rounded border border-gray-300 bg-white px-2 py-1 hover:border-brand focus-visible:outline focus-visible:outline-2 focus-visible:outline-brand" onClick={() => setOpen(false)}>
                  <span aria-hidden="true" className="inline-block h-3 w-3 rounded-full" style={{ background: elementColor(e) }} />{e}</Link></li>
              ))}
            </ul>
          </nav>
          <nav aria-label="Tiers">
            <h2 className="mb-1 text-xs font-bold uppercase tracking-wide text-navy">Tiers</h2>
            <ul className="mb-4 flex gap-2">{TIERS.map((t) => (<li key={t}><Link href={`/browse?tier=${t}`} className="rounded border border-gray-300 bg-white px-2 py-1 hover:border-brand focus-visible:outline focus-visible:outline-2 focus-visible:outline-brand" onClick={() => setOpen(false)}>{t}</Link></li>))}</ul>
          </nav>
          <nav aria-label="Families">
            <h2 className="mb-1 text-xs font-bold uppercase tracking-wide text-navy">Families</h2>
            <ul>{FAMILIES.map((f) => (<li key={f}><Link href={`/browse?family=${f}`} className={link} onClick={() => setOpen(false)}>{f}</Link></li>))}</ul>
          </nav>
        </aside>
        <main id="content" tabIndex={-1} className="min-w-0 flex-1 p-4 md:p-8">{children}</main>
      </div>
      <footer className="border-t border-gray-200 bg-sky px-4 py-4 text-xs text-gray-700">
        <div className="mx-auto max-w-7xl">
          <p>HADB v1 (release candidate 3). No cookies and no analytics are used on this site. Release licence: {RELEASE_LICENSE === 'TBC' ? 'to be confirmed (TBC)' : RELEASE_LICENSE}.</p>
          <p className="mt-1">Occurrence data: GBIF.org (13 October 2026) GBIF Occurrence Download https://doi.org/10.15468/dl.kb25da</p>
        </div>
      </footer>
    </div>
  );
}
