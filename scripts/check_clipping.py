"""Finds text (titles, tick labels, annotations, legends) that extends beyond the edge of its panel, i.e. would be cut off in the PNG.
Renders each panel in memory (no files written) and measures every visible Text and Legend against the figure box. Prints the overshoot in inches.
Usage: python scripts/check_clipping.py [4d ...]"""
import importlib, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / 'scripts'))
import matplotlib
matplotlib.use('Agg')
from matplotlib.text import Text
from matplotlib.legend import Legend
from figures import layout as L, style as S

want = set(sys.argv[1:]); bad = 0
for fig_n, letters in L.PANELS.items():
    for l in letters:
        if want and '%d%s' % (fig_n, l) not in want: continue
        mod = importlib.import_module('figures.panels.fig%d%s' % (fig_n, l)); fig, _ = mod.render(); fig.set_dpi(100); fig.canvas.draw(); r = fig.canvas.get_renderer(); W, H = fig.bbox.width, fig.bbox.height; issues = []
        hidden = set()
        for ax in fig.axes:
            for axis in (ax.xaxis, ax.yaxis):
                lo, hi = sorted(axis.get_view_interval())
                for tk, loc in zip(axis.get_major_ticks(), axis.get_majorticklocs()):
                    if not (lo - 1e-9 <= loc <= hi + 1e-9): hidden.update([tk.label1, tk.label2])
        for a in fig.findobj(lambda o: isinstance(o, (Text, Legend))):
            if a in hidden: continue
            if isinstance(a, Text) and (not a.get_visible() or not a.get_text().strip()): continue
            if not a.get_visible(): continue
            try: b = a.get_window_extent(r)
            except Exception: continue
            ov = dict(left=-b.x0, right=b.x1 - W, bottom=-b.y0, top=b.y1 - H); worst = max(ov.items(), key=lambda kv: kv[1])
            if worst[1] > 1.5: issues.append((worst[1] / 100.0, worst[0], (a.get_text()[:40] if isinstance(a, Text) else 'legend')))
        if issues:
            bad += 1; issues.sort(reverse=True); print('%d%s  %.1f x %.1f in: %s' % (fig_n, l, W / 100, H / 100, '; '.join('%s %.2f in over %s (%r)' % (i[1], i[0], i[1], i[2]) for i in issues[:4])))
        import matplotlib.pyplot as plt; plt.close(fig)
print('panels with text beyond the panel edge: %d' % bad)
