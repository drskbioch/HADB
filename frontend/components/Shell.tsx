'use client';
// Page frame in the style of the parent S Khan Lab sites: image banner, pill navigation, left sidebar (lab network + quick links) and lab footer.
// The sidebar collapses on mobile.
import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { elementColor, FAMILIES, SIDEBAR_ELEMENTS, TIERS } from '@/lib/elements';
import { RELEASE_LICENSE } from '@/lib/api';

const TOP = [
  { href: '/', label: 'Home' }, { href: '/about', label: 'About' }, { href: '/browse', label: 'Database' },
  { href: '/downloads', label: 'Downloads' }, { href: '/api-docs', label: 'API' }, { href: '/contact', label: 'Contact Us' },
];
const PAGES = [
  { href: '/', label: 'Home' }, { href: '/about', label: 'About' }, { href: '/browse', label: 'Browse the database' },
  { href: '/evidence-tiers', label: 'Evidence and tiers' }, { href: '/downloads', label: 'Downloads' }, { href: '/api-docs', label: 'API documentation' }, { href: '/citation', label: 'Citation and versions' },
  { href: '/contact', label: 'Contact Us' },
];
// Sibling databases of the same research group (Phyto Databases). BEDB is left out until its site is online.
const NETWORK = [
  { name: 'AVPCD', href: 'https://avpcd.habdsk.org/' }, { name: 'HADB', href: '/', current: true },
  { name: 'MPDB', href: 'https://www.mpdb.habdsk.org/' }, { name: 'PTDB', href: 'https://www.ptdb.habdsk.org/' },
];

function cls(...a: (string | false)[]) { return a.filter(Boolean).join(' '); }

function Banner() {
  return (
    <Link href="/" className="block">
      <Image src="/images/hadb-banner.webp" alt="HADB: Hyper Accumulators Data Base. A comprehensive resource for metal hyperaccumulator plants and their elemental accumulation. S Khan Lab." width={2161} height={568} priority className="h-auto w-full" />
    </Link>
  );
}

export default function Shell({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  const [open, setOpen] = useState(false);
  const link = 'dblink border-transparent hover:border-accent';
  return (
    <div className="flex min-h-screen flex-col text-ink">
      <a href="#content" className="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:z-50 focus:rounded focus:bg-white focus:p-2 focus:text-brand">Skip to content</a>
      <div className="mx-auto w-full max-w-7xl px-3 pt-3">
        <header>
          <Banner />
          <div className="mt-1 flex items-center gap-2 rounded-2xl border-2 border-accent bg-white px-3 py-1.5">
            <button type="button" className="rounded-full border border-navy px-3 py-1 text-sm font-semibold text-navy md:hidden" aria-expanded={open} aria-controls="sidebar" onClick={() => setOpen(!open)}>
              {open ? 'Close menu' : 'Menu'}
            </button>
            <nav aria-label="Main" className="ml-auto hidden md:block">
              <ul className="flex gap-1">
                {TOP.map((t) => (
                  <li key={t.href}>
                    <Link href={t.href} aria-current={path === t.href ? 'page' : undefined}
                      className={cls('block rounded-[25px] px-3 py-1 text-sm font-bold text-black transition-colors hover:bg-navy hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent', path === t.href && 'bg-navy text-white')}>
                      {t.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </nav>
          </div>
        </header>
        <div className="mt-3 flex flex-1 flex-col gap-3 md:flex-row">
          <aside id="sidebar" aria-label="Quick links" className={cls('rounded-2xl border border-accent/40 bg-skydeep p-3 text-sm md:block md:w-64 md:shrink-0 md:self-start', open ? 'block' : 'hidden')}>
            <section aria-labelledby="supervisor" className="mb-3 overflow-hidden rounded-xl bg-sky">
              <h2 id="supervisor" className="!m-0 bg-skydeep px-2 py-1.5 text-center text-base font-bold">Supervised by</h2>
              <p className="!mb-0 p-2 text-center font-bold">Dr. Shahid Ullah</p>
            </section>
            <nav aria-label="Phyto databases" className="mb-3 overflow-hidden rounded-xl bg-sky">
              <h2 className="!m-0 bg-skydeep px-2 py-1.5 text-center text-base font-bold">Our Services</h2>
              <p className="!mb-0 px-2 pt-2 text-center text-xs font-bold uppercase tracking-wide text-navy">Phyto Databases</p>
              <ul className="space-y-1 p-2">
                {NETWORK.map((n) => (
                  <li key={n.name}>
                    {n.current
                      ? <Link href={n.href} aria-current="true" className="dblink text-center">{n.name}</Link>
                      : <a href={n.href} rel="noopener" className="dblink text-center">{n.name}</a>}
                  </li>
                ))}
              </ul>
            </nav>
            <nav aria-label="Pages">
              <h2 className="!mt-0 mb-1 text-xs font-bold uppercase tracking-wide text-navy">Pages</h2>
              <ul className="mb-4 space-y-1">{PAGES.map((p) => (<li key={p.href}><Link href={p.href} aria-current={path === p.href ? 'page' : undefined} className={link} onClick={() => setOpen(false)}>{p.label}</Link></li>))}</ul>
            </nav>
            <nav aria-label="Elements">
              <h2 className="!mt-0 mb-1 text-xs font-bold uppercase tracking-wide text-navy">Elements</h2>
              <ul className="mb-4 flex flex-wrap gap-2">
                {SIDEBAR_ELEMENTS.map((e) => (
                  <li key={e}><Link href={`/browse?element=${e}`} className="dblink inline-flex items-center gap-1 bg-white" onClick={() => setOpen(false)}>
                    <span aria-hidden="true" className="inline-block h-3 w-3 rounded-full" style={{ background: elementColor(e) }} />{e}</Link></li>
                ))}
              </ul>
            </nav>
            <nav aria-label="Tiers">
              <h2 className="!mt-0 mb-1 text-xs font-bold uppercase tracking-wide text-navy">Tiers</h2>
              <ul className="mb-4 flex gap-2">{TIERS.map((t) => (<li key={t}><Link href={`/browse?tier=${t}`} className="dblink bg-white" onClick={() => setOpen(false)}>{t}</Link></li>))}</ul>
            </nav>
            <nav aria-label="Families">
              <h2 className="!mt-0 mb-1 text-xs font-bold uppercase tracking-wide text-navy">Families</h2>
              <ul className="space-y-1">{FAMILIES.map((f) => (<li key={f}><Link href={`/browse?family=${f}`} className={link} onClick={() => setOpen(false)}>{f}</Link></li>))}</ul>
            </nav>
          </aside>
          <main id="content" tabIndex={-1} className="min-w-0 flex-1 rounded-2xl border border-accent/40 bg-white p-4 shadow-sm md:p-8">{children}</main>
        </div>
      </div>
      <footer className="mx-auto mb-3 mt-6 w-full max-w-7xl px-3">
        <div className="rounded-2xl border border-accent/40 bg-skydeep px-6 py-6 text-sm">
          <div className="grid gap-6 md:grid-cols-3">
            <div>
              <p className="!mb-1 text-3xl font-bold"><span className="text-[#c80000]">S </span><span className="text-[#2e8b3a]">Khan </span><span className="text-[#1565c0]">Lab</span></p>
              <p className="!mb-1"><Link href="/" className="text-brand underline">Home</Link></p>
              <p className="!mb-0 text-xs text-gray-700">2010 - 2026 Designed by Dr. Shahid Ullah &amp; Team</p>
            </div>
            <div>
              <h2 className="!mt-0 text-base">Contact</h2>
              <p className="!mb-1">Phone: <a href="tel:+14243938809" className="text-brand underline">+1 424 393 8809</a></p>
              <p className="!mb-1">Email: <a href="mailto:drskbioch@gmail.com" className="text-brand underline">drskbioch@gmail.com</a></p>
              <p className="!mb-0"><a href="https://www.facebook.com/skhan.lab.3/timeline" target="_blank" rel="noopener noreferrer" className="text-brand underline">Facebook</a></p>
            </div>
            <div>
              <h2 className="!mt-0 text-base">Our Aims</h2>
              <p className="!mb-0">We aim to uncover the molecular mechanisms of important proteins in life sciences, provide comprehensive open data sharing for the global scientific community, and contribute to societal betterment.</p>
            </div>
          </div>
          <div className="mt-5 border-t border-accent/40 pt-3 text-xs text-gray-700">
            <p>HADB v1. No cookies and no analytics are used on this site. Release licence: {RELEASE_LICENSE}.</p>
            <p className="!mb-0 mt-1">Occurrence data: GBIF.org (13 October 2026) GBIF Occurrence Download https://doi.org/10.15468/dl.kb25da</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
