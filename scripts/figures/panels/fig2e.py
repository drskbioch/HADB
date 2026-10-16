"""Fig 2e: top-20 families, species with best tier T1 vs T2 (dumbbell)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 2, 'e'
META = dict(chart='dumbbell', data=['release/evidence.csv', 'release/species_element.csv'], filter='headline view; species counted once at best tier over all elements; top 20 families by species')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=1.05, bottom=0.5, right=0.12, top=0.45)
    E = FD.evidence(); fam = E.drop_duplicates('sp').set_index('sp').family; t = FD.species_tier(); D = pd.DataFrame({'family': fam, 'tier': t}).dropna()
    g = D.groupby(['family', 'tier']).size().unstack(fill_value=0).reindex(columns=['T1', 'T2'], fill_value=0); g['tot'] = g.sum(axis=1); g = g.sort_values('tot', ascending=False).head(20).iloc[::-1]
    y = np.arange(len(g)); ax.hlines(y, g.T2, g.T1, color=S.GREY, lw=1.0); ax.scatter(g.T1, y, s=14, color=S.TIER['T1'], zorder=3, label='T1'); ax.scatter(g.T2, y, s=14, color=S.TIER['T2'], zorder=3, label='T2')
    ax.set_yticks(y); ax.set_yticklabels(g.index, fontsize=S.TICK - 2); ax.set_xscale('symlog', linthresh=10); ax.set_xlim(0, 300); ax.set_xticks([0, 10, 30, 100, 300]); ax.set_xticklabels(['0', '10', '30', '100', '300'])
    ax.set_xlabel('Species (n, symlog axis)'); ax.grid(axis='x', color=S.grid_color(bg), lw=S.LW_GRID); ax.set_axisbelow(True); ax.legend(loc='lower right', handletextpad=0.2)
    S.title(fig, 'Families: T1 vs T2 species'); return fig, int(D.shape[0])
