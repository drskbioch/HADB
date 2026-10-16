"""Fig 5j: median environment by family and element (three heatmaps)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
from matplotlib.colors import LinearSegmentedColormap
FIG, LET = 5, 'j'
META = dict(chart='heatmap', data=['derived/species_environment_summary.csv'], filter='species with >= 20 native cells; median of species medians per family (12 families with most species) and element; grey = no species')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); Sm = FD.env_ok(); E = FD.species_by_element(Sm).merge(Sm[['accepted_name', 'family', 'bio1_median_C', 'bio12_median_mm', 'ph_median']], left_on='sp', right_on='accepted_name')
    fams = Sm.family.value_counts().head(12).index; cm = LinearSegmentedColormap.from_list('hadb', S.SEQ); cm.set_bad(S.MISSING); pw = (w - 1.6) / 3
    for k, (c, lab, fmt) in enumerate((('bio1_median_C', 'bio1 (degrees C)', '%.0f'), ('bio12_median_mm', 'bio12 (mm)', '%.0f'), ('ph_median', 'pH', '%.1f'))):
        ax = fig.add_axes([(1.3 + k * (pw + 0.12)) / w, 0.6 / h, pw / w, (h - 1.1) / h]); M = E.groupby(['family', 'element'])[c].median().unstack().reindex(index=fams, columns=FD.CORE)
        ax.imshow(np.ma.masked_invalid(M.values), cmap=cm, aspect='auto')
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                v = M.values[i, j]
                if not np.isnan(v): ax.text(j, i, fmt % v, ha='center', va='center', fontsize=S.TICK - 3.5, color='white' if (v - np.nanmin(M.values)) / (np.nanmax(M.values) - np.nanmin(M.values) + 1e-9) > 0.6 else '#1A1A1A')
        ax.set_xticks(range(4)); ax.set_xticklabels(FD.CORE, fontsize=S.TICK - 2); ax.set_title(lab, fontsize=S.TICK - 1, color=S.fg(bg), pad=2); ax.tick_params(length=0)
        ax.set_yticks(range(len(fams)) if k == 0 else []); ax.set_yticklabels(list(fams) if k == 0 else [], fontsize=S.TICK - 2.5)
        for s in ax.spines.values(): s.set_visible(False)
    S.title(fig, 'Median environment by family and element'); return fig, len(Sm)
