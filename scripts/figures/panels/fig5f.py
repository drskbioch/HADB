"""Fig 5f: climate envelopes of families (bubble)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 5, 'f'
META = dict(chart='bubble', data=['derived/species_environment_summary.csv'], filter='species with >= 20 native cells; family median of species medians; bubble = species; families with >= 3 species drawn, >= 8 labelled')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.6, bottom=0.55, right=0.15, top=0.45); Sm = FD.env_ok()
    g = Sm.groupby('family').agg(n=('accepted_name', 'size'), t=('bio1_median_C', 'median'), p=('bio12_median_mm', 'median')).query('n >= 3')
    ax.scatter(g.t, g.p, s=g.n * 5, color=S.MAIN, alpha=0.6, edgecolor=S.fg(bg), lw=0.3)
    for fam, r in g[g.n >= 8].iterrows(): ax.text(r.t, r.p + 130, fam, ha='right' if r.t > g.t.quantile(0.8) else 'center', fontsize=S.TICK - 3, color=S.fg(bg))
    ax.set_xlabel('bio1 family median (degrees C)'); ax.set_ylabel('bio12 family median (mm)'); ax.grid(color=S.grid_color(bg), lw=S.LW_GRID); ax.set_axisbelow(True)
    fig.text(0.6 / w, 0.12 / h, 'bubble area = species (n = %d to %d)' % (g.n.min(), g.n.max()), fontsize=S.TICK - 2.5, color=S.muted(bg)); S.title(fig, 'Family climate envelopes'); return fig, int(g.n.sum())
