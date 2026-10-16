"""Fig 2c: Ni species by combination of evidence sources (UpSet-style)."""
import numpy as np
from figures import style as S, figdata as FD, layout as L
FIG, LET = 2, 'c'
META = dict(chart='upset-style', data=['release/evidence.csv', 'release/species_element.csv'], filter='headline view, element Ni, species by set of evidence types')
LAB = {'block_b_label': 'Block B', 'gei_xrf_taxon': 'Gei XRF', 'gei_literature_update': 'Gei lists', 'paper_table': 'Papers'}
ORD = ['block_b_label', 'gei_literature_update', 'gei_xrf_taxon', 'paper_table']


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg)
    E = FD.evidence(); E = E[E.element == 'Ni']; sets = E.groupby('sp').evidence_type.apply(lambda s: tuple(t for t in ORD if t in set(s)))
    cnt = sets.value_counts().head(7); n = int(sets.shape[0]); ax = S.axes_in(fig, left=0.55, bottom=1.25, right=0.12, top=0.5)
    x = np.arange(len(cnt)); ax.bar(x, cnt.values, color=S.elem_color('Ni'), width=0.62, lw=0)
    for xi, v in zip(x, cnt.values): ax.text(xi, v + 3, str(v), ha='center', fontsize=S.TICK - 2, color=S.fg(bg))
    ax.set_xticks([]); ax.set_ylabel('Ni species (n)'); ax.set_xlim(-0.6, len(cnt) - 0.4)
    ax2 = fig.add_axes([0.55 / w, 0.3 / h, (w - 0.67) / w, 0.9 / h]); ax2.axis('off'); ax2.set_xlim(-0.6, len(cnt) - 0.4); ax2.set_ylim(-0.5, len(ORD) - 0.5)
    for j, t in enumerate(ORD):
        yy = len(ORD) - 1 - j; ax2.text(-0.7, yy, LAB[t], ha='right', va='center', fontsize=S.TICK - 1.5, color=S.fg(bg))
        for xi in x: ax2.scatter(xi, yy, s=10, color=S.grid_color(bg), zorder=1)
    for xi, comb in zip(x, cnt.index):
        ys = [len(ORD) - 1 - ORD.index(t) for t in comb]; ax2.scatter([xi] * len(ys), ys, s=16, color=S.fg(bg), zorder=3)
        if len(ys) > 1: ax2.plot([xi, xi], [min(ys), max(ys)], color=S.fg(bg), lw=1.0, zorder=2)
    ax.set_xlim(-0.6, len(cnt) - 0.4); S.title(fig, 'Ni: overlap of evidence sources'); return fig, n
