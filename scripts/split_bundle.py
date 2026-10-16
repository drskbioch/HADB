"""Split a bundle file (sections starting with '#### figNx.py') into scripts/figures/panels/figNx.py. Usage: python scripts/split_bundle.py scripts/bundle_fig2.txt"""
import sys
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'scripts' / 'figures' / 'panels'
txt = Path(sys.argv[1]).read_text(encoding='utf-8'); name, buf, n = None, [], 0
for line in txt.splitlines(keepends=True) + ['#### END\n']:
    if line.startswith('#### '):
        if name: (P / name).write_text(''.join(buf), encoding='utf-8', newline='\n'); n += 1
        name, buf = line[5:].strip(), []
    else: buf.append(line)
print('wrote', n, 'panel files')
