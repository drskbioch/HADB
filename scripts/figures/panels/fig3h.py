"""Fig 3h: families x elements, species counts (heatmap, top 15 families)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 3, 'h'
META = dict(chart='heatmap', data=['release/evidence.csv', 'release/species_element.csv'], filter='headline view; distinct species per family and element (Ni Mn Zn Co Cd Se); 15 families with most species')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=1.0, bottom=0.55, right=0.1, top=0.5)
    P = FD.pairs(); P = P[P.element.isin(FD.SIX)]; top = P.drop_duplicates('sp').family.value_counts().head(15).index; M = P[P.family.isin(top)].groupby(['family', 'element']).sp.nunique().unstack(fill_value=0).reindex(index=top, columns=FD.SIX, fill_value=0)
    from matplotlib.colors import LinearSegmentedColormap
    cm = LinearSegmentedColormap.from_list('hadb', S.SEQ); im = ax.imshow(np.log1p(M.values), cmap=cm, aspect='auto')
    for i in range(M.shape[0]):
        for j in range(M.shape[1]): ax.text(j, i, M.values[i, j], ha='center', va='center', fontsize=S.TICK - 3, color='white' if np.log1p(M.values[i, j]) > 3.2 else '#1A1A1A')
    ax.set_xticks(range(6)); ax.set_xticklabels(FD.SIX); ax.set_yticks(range(len(M))); ax.set_yticklabels(M.index, fontsize=S.TICK - 2); ax.tick_params(length=0)
    for s in ax.spines.values(): s.set_visible(False)
    fig.text(0.1 / w, 0.15 / h, 'colour = log(1 + species)', fontsize=S.TICK - 2.5, color=S.muted(bg)); S.title(fig, 'Families by element'); return fig, int(P.sp.nunique())
