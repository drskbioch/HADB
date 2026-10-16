"""Figure CLI.  python scripts/make_figures.py --panel 4d | --figure 4 | --all | --assemble [--force]
Each panel renders once at 1200 dpi into manuscript/figures/panels/figureNx.png and is cached by a hash of its code, style.py, layout.py, figdata.py and its data files
(cache and manifests live in manuscript/figure_meta/, so manuscript/figures holds PNG only). --assemble builds manuscript/figures/multipanel/figureN.png with bold panel
letters (integer-pixel paste, no resampling)."""
import argparse, csv, hashlib, importlib, json, sys, time
from pathlib import Path
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from figures import style as S, layout as L
PAN, MULTI, META = ROOT / 'manuscript/figures/panels', ROOT / 'manuscript/figures/multipanel', ROOT / 'manuscript/figure_meta'
for d in (PAN, MULTI, META / 'cache'): d.mkdir(parents=True, exist_ok=True)
DR = ROOT / 'data_release'


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()


def key_of(modfile, meta):
    h = hashlib.sha256()
    for f in (modfile, ROOT / 'scripts/figures/style.py', ROOT / 'scripts/figures/layout.py', ROOT / 'scripts/figures/figdata.py'): h.update(Path(f).read_bytes())
    for d in meta['data']: h.update(sha(DR / d).encode())
    return h.hexdigest()


def panels_of(fig=None):
    out = []
    for f in sorted((ROOT / 'scripts/figures/panels').glob('fig[2-5][a-j].py')):
        n, l = int(f.stem[3]), f.stem[4]
        if fig is None or n == fig: out.append((n, l, f))
    return out


def render_panel(n, l, f, force=False):
    mod = importlib.import_module('figures.panels.' + f.stem); importlib.reload(mod); name = 'figure%d%s' % (n, l); png = PAN / (name + '.png'); cj = META / 'cache' / (name + '.json')
    k = key_of(f, mod.META)
    if not force and png.exists() and cj.exists() and json.loads(cj.read_text())['key'] == k: return 'cached'
    t = time.time(); fig, nn = mod.render(); S.save(fig, png)
    with Image.open(png) as im: size, dpi = im.size, im.info.get('dpi')
    info = dict(key=k, panel=name, chart=mod.META['chart'], data=mod.META['data'], sources={d: sha(DR / d) for d in mod.META['data']}, filter=mod.META['filter'], n=int(nn), size_px=size, dpi=dpi, seconds=round(time.time() - t, 1),
                timestamp=time.strftime('%Y-%m-%dT%H:%M:%S'))
    cj.write_text(json.dumps(info, indent=1)); return 'rendered %.1fs' % info['seconds']


def write_manifest():
    rows, plan = [], []
    for cj in sorted((META / 'cache').glob('figure*.json')):
        i = json.loads(cj.read_text()); rows.append((i['panel'], i['chart'], ' | '.join('%s [%s]' % (d, s) for d, s in i['sources'].items()), i['filter'], i['n'], i['timestamp']))
        plan.append((i['panel'], i['chart'], '; '.join(i['data']), i['filter'], i['n']))
    pd.DataFrame(rows, columns=['panel', 'chart', 'source_files_and_sha256', 'filter', 'n', 'timestamp']).to_csv(META / 'figure_manifest.csv', index=False, lineterminator='\n')
    pd.DataFrame(plan, columns=['panel', 'chart', 'data_file', 'filter', 'n']).to_csv(META / 'plan.csv', index=False, lineterminator='\n')


def font(px):
    for p in (r'C:\Windows\Fonts\arialbd.ttf', r'C:\Windows\Fonts\Arialbd.ttf'):
        if Path(p).exists(): return ImageFont.truetype(p, px)
    import matplotlib; return ImageFont.truetype(str(Path(matplotlib.get_data_path()) / 'fonts/ttf/DejaVuSans-Bold.ttf'), px)


def assemble(n):
    W, Hh = L.multipanel_size(n); wpx, hpx = round(W * S.DPI), round(Hh * S.DPI); bg = S.BACKGROUNDS[S.DEFAULT_BG[n]]
    canvas = Image.new('RGB', (wpx, hpx), bg); fnt = font(round(S.LETTER / 72 * S.DPI)); dr = ImageDraw.Draw(canvas); col = S.fg(S.DEFAULT_BG[n])
    for l in L.PANELS[n]:
        x, y = L.panel_xy(n, l); X, Y = round(x * S.DPI), round(y * S.DPI)
        with Image.open(PAN / ('figure%d%s.png' % (n, l))) as im: canvas.paste(im.convert('RGB'), (X, Y))
        dr.text((X + round(0.05 * S.DPI), Y + round(0.0 * S.DPI)), l, font=fnt, fill=col)
    dst = MULTI / ('figure%d.png' % n)
    for attempt in range(8):                      # Windows can refuse a write while a viewer, indexer or antivirus holds the file: retry
        try: canvas.save(dst, dpi=(S.DPI, S.DPI), compress_level=3); break
        except OSError:
            if attempt == 7: raise
            time.sleep(3 * (attempt + 1))
    return canvas.size


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--panel'); ap.add_argument('--figure', type=int); ap.add_argument('--all', action='store_true'); ap.add_argument('--assemble', action='store_true'); ap.add_argument('--force', action='store_true')
    a = ap.parse_args(); todo = []
    if a.panel: todo = [t for t in panels_of() if '%d%s' % (t[0], t[1]) == a.panel]
    elif a.figure: todo = panels_of(a.figure)
    elif a.all: todo = panels_of()
    for n, l, f in todo:
        try: print('fig%d%s' % (n, l), render_panel(n, l, f, a.force), flush=True)
        except Exception as e: print('fig%d%s FAILED: %r' % (n, l, e)[:300], flush=True)
    if todo: write_manifest()
    if a.assemble or a.all:
        for n in ([a.figure] if a.figure else [2, 3, 4, 5]):
            miss = [l for l in L.PANELS[n] if not (PAN / ('figure%d%s.png' % (n, l))).exists()]
            print('assemble fig%d' % n, 'SKIPPED, missing panels %s' % miss if miss else assemble(n))
