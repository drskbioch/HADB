import Link from 'next/link';

export default function NotFound() {
  return (
    <div>
      <h1>Page not found</h1>
      <p><Link href="/" className="text-brand underline">Home</Link> or <Link href="/browse" className="text-brand underline">browse the database</Link>.</p>
    </div>
  );
}
