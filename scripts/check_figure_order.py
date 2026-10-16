"""Check that the FIRST citations of figures (Fig 2a, 2b ... 5j) and of tables (Table 1 ... 3) appear in ascending order in .md / .txt / .docx files.
Usage: python scripts/check_figure_order.py [file or folder ...]   (default: manuscript/results_skeleton.md). Prints failures only; exit 1 on failure."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FIG = re.compile(r'\bFig(?:ure|s)?\.?\s*(\d)\s*([a-j])?\b'); TAB = re.compile(r'\bTables?\s+(\d)\b')


def text_of(p):
    if p.suffix == '.docx':
        from docx import Document
        return '\n'.join(x.text for x in Document(p).paragraphs)
    return p.read_text(encoding='utf-8', errors='ignore')


def check(p):
    t = text_of(p); bad = []; seen = []
    for m in FIG.finditer(t):
        k = (int(m.group(1)), m.group(2) or '')
        if k not in seen: seen.append(k)
    if seen != sorted(seen, key=lambda k: (k[0], k[1] or '')): bad.append('%s: figure first-citation order %s' % (p.name, ['%d%s' % k for k in seen]))
    seen = []
    for m in TAB.finditer(t):
        k = int(m.group(1))
        if k not in seen: seen.append(k)
    if seen != sorted(seen): bad.append('%s: table first-citation order %s' % (p.name, seen))
    return bad


if __name__ == '__main__':
    args = [Path(a) for a in sys.argv[1:]] or [ROOT / 'manuscript' / 'results_skeleton.md']; files = []
    for a in args: files += [f for f in a.rglob('*') if f.suffix in ('.md', '.txt', '.docx')] if a.is_dir() else [a]
    fails = [b for f in files for b in check(f)]
    for b in fails: print('FAIL', b)
    sys.exit(1 if fails else 0)
