"""Fig 3g: licence status of the evidence rows (donut)."""
import numpy as np
from figures import style as S, figdata as FD, layout as L
FIG, LET = 3, 'g'
META = dict(chart='donut', data=['release/evidence.csv'], filter='all evidence rows of rc3; licence recorded for the source of each row')
COL = {'CC BY': S.MAIN, 'CC BY-NC': '#D9A441', 'CC BY-NC-ND': S.TIER['T2'], 'not stated or unknown': '#B8B8B8'}


def lic(s):
    s = s.lower()
    return 'CC BY-NC-ND' if 'by-nc-nd' in s else 'CC BY-NC' if 'by-nc' in s else 'CC BY' if 'cc by' in s else 'not stated or unknown'


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = fig.add_axes([0.3 / w, 1.0 / h, (w - 0.6) / w, (h - 1.6) / h])
    E = FD.evidence_all(); c = E.source_license.map(lic).value_counts().reindex(list(COL)).fillna(0); ax.pie(c.values, colors=[COL[k] for k in c.index], startangle=90, counterclock=False, wedgeprops=dict(width=0.38, edgecolor=S.BACKGROUNDS[bg], linewidth=1))
    ax.text(0, 0, '%s\nrows' % format(len(E), ','), ha='center', va='center', fontsize=S.TICK, color=S.fg(bg), fontweight='bold')
    for j, (k, v) in enumerate(c.items()):
        fig.add_artist(__import__('matplotlib').patches.Rectangle((0.45 / w, (0.78 - 0.17 * j) / h), 0.1 / w, 0.1 / h, transform=fig.transFigure, color=COL[k], lw=0)); fig.text(0.62 / w, (0.83 - 0.17 * j) / h, '%s  %s (%.0f%%)' % (k, format(int(v), ','), 100 * v / len(E)), fontsize=S.TICK - 2, color=S.fg(bg), va='center')
    S.title(fig, 'Licence of the evidence sources'); return fig, len(E)
