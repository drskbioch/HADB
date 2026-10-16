// Turns PMID:..., DOI:... and URL:... tokens of a citation string into safe external links (http/https only).
import React from 'react';

const TOKEN = /(PMID:\s*\d{6,8}|DOI:\s*10\.\d{4,9}\/[^\s,;|)]+|URL:\s*https?:\/\/[^\s|]+)/g;

export default function Citation({ text }: { text: string }) {
  if (!text) return <span className="text-gray-600">no citation</span>;
  const parts = text.split(TOKEN);
  return (
    <span>
      {parts.map((p, i) => {
        if (i % 2 === 0) return <React.Fragment key={i}>{p}</React.Fragment>;
        const v = p.replace(/^(PMID|DOI|URL):\s*/, '');
        const href = p.startsWith('PMID') ? `https://pubmed.ncbi.nlm.nih.gov/${v}/` : p.startsWith('DOI') ? `https://doi.org/${v}` : v;
        return (
          <a key={i} href={href} target="_blank" rel="noopener noreferrer" className="text-brand underline underline-offset-2 break-all">
            {p.startsWith('URL') ? 'link' : p}
          </a>
        );
      })}
    </span>
  );
}
