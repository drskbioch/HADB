"""Fig 2b: evidence rows by evidence type (waffle)."""
import numpy as np
from matplotlib.patches import Rectangle
from figures import style as S, figdata as FD, layout as L
FIG, LET = 2, 'b'
META = dict(chart='waffle', data=['release/evidence.csv', 'release/species_element.csv'], filter='headline view evidence rows by evidence_type; one square = 1% of rows')
LAB = {'block_b_label': 'Block B labels', 'gei_xrf_taxon': 'Gei XRF tables', 'gei_literature_update': 'Gei compiled lists', 'paper_table': 'Sabah / Queensland tables'}


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = fig.add_axes([0.45 / w, 1.15 / h, (w - 0.9) / w, (h - 1.15 - 0.5) / h]); ax.axis('off')
    E = FD.evidence(); vc = E.evidence_type.value_counts(); tot = vc.sum(); raw = vc / tot * 100; k = np.floor(raw).astype(int); rem = 100 - k.sum()
    for t in (raw - k).sort_values(ascending=False).index[:rem]: k[t] += 1
    seq = [t for t in vc.index for _ in range(k[t])]; side = min((w - 0.9) / 10, (h - 1.65) / 10)
    for i, t in enumerate(seq):
        r, c = divmod(i, 10); ax.add_patch(Rectangle((c * 1.0, 9 - r), 0.88, 0.88, color=S.SRC[t], lw=0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect('equal')
    for j, t in enumerate(vc.index):
        fig.text(0.62 / w, (0.88 - 0.2 * j) / h, '%s  %s rows (%.0f%%)' % (LAB[t], format(int(vc[t]), ','), 100 * vc[t] / tot), fontsize=S.TICK - 1.5, color=S.fg(bg), va='center')
        fig.add_artist(Rectangle((0.42 / w, (0.88 - 0.2 * j - 0.05) / h), 0.12 / w, 0.1 / h, transform=fig.transFigure, color=S.SRC[t], lw=0))
    S.title(fig, 'Evidence rows by source'); return fig, int(tot)
