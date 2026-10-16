"""Figure checks (prints failures only; exit 1 on failure): names, PNG-only, dpi metadata, multipanel size within layout limits, panel counts, manifest traceability."""
import hashlib, re, sys
from pathlib import Path
import pandas as pd
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / 'scripts'))
from figures import layout as L
F = ROOT / 'manuscript' / 'figures'; fails = []


def bad(m): fails.append(m)


allf = [p for p in F.rglob('*') if p.is_file()]
for p in allf:
    if p.suffix != '.png': bad('non-PNG file under manuscript/figures: %s' % p.name)
for fig, letters in L.PANELS.items():
    pn = sorted(p.name for p in (F / 'panels').glob('figure%d*.png' % fig)); want = ['figure%d%s.png' % (fig, l) for l in letters]
    if pn != want: bad('panels of figure %d: expected %d files, found %d (%s)' % (fig, len(want), len(pn), sorted(set(want) ^ set(pn))))
    mp = F / 'multipanel' / ('figure%d.png' % fig)
    if not mp.exists(): bad('missing multipanel figure%d.png' % fig); continue
    with Image.open(mp) as im:
        W, H = L.multipanel_size(fig)
        if im.size[0] > L.WIDTH * 1200 + 1 or im.size[1] > L.MAX_HEIGHT * 1200 + 1: bad('multipanel figure%d too large: %s' % (fig, im.size))
        if abs(im.size[0] - W * 1200) > 1 or abs(im.size[1] - H * 1200) > 1: bad('multipanel figure%d size %s differs from layout %s' % (fig, im.size, (W * 1200, H * 1200)))
        if not im.info.get('dpi') or abs(im.info['dpi'][0] - 1200) > 0.01: bad('multipanel figure%d dpi %s' % (fig, im.info.get('dpi')))
for p in (F / 'panels').glob('*.png'):
    if not re.fullmatch(r'figure[2-5][a-j]\.png', p.name): bad('bad panel name %s' % p.name)
    with Image.open(p) as im:
        if not im.info.get('dpi') or abs(im.info['dpi'][0] - 1200) > 0.01: bad('panel %s dpi %s' % (p.name, im.info.get('dpi')))
        if (im.size[0] / 1200, im.size[1] / 1200) != tuple(round(v, 4) for v in (im.size[0] / 1200, im.size[1] / 1200)): bad('size ' + p.name)
        fig, l = int(p.name[6]), p.name[7]; w, h = L.panel_size(fig, l)
        if abs(im.size[0] - w * 1200) > 1 or abs(im.size[1] - h * 1200) > 1: bad('panel %s size %s differs from layout %s' % (p.name, im.size, (w * 1200, h * 1200)))
M = pd.read_csv(ROOT / 'manuscript/figure_meta/figure_manifest.csv', keep_default_na=False)
for fig, letters in L.PANELS.items():
    for l in letters:
        r = M[M.panel == 'figure%d%s' % (fig, l)]
        if len(r) != 1: bad('manifest row missing for figure%d%s' % (fig, l)); continue
        r = r.iloc[0]
        if not (r.chart and r.source_files_and_sha256 and r['filter'] and int(r.n) > 0 and r.timestamp): bad('manifest incomplete for ' + r.panel)
        for part in str(r.source_files_and_sha256).split(' | '):
            m = re.match(r'(.+) \[([0-9A-F]{64})\]$', part)
            if not m or hashlib.sha256((ROOT / 'data_release' / m.group(1)).read_bytes()).hexdigest().upper() != m.group(2): bad('source hash does not match for %s: %s' % (r.panel, part[:60]))
for f in fails: print('FAIL', f)
sys.exit(1 if fails else 0)
