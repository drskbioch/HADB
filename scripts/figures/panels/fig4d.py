"""Fig 4d: species by native WGSRPD region, top 20 (bars)."""
import re
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 4, 'd'
META = dict(chart='bars', data=['derived/species_environment_summary.csv', 'work/wgsrpd_level3.geojson'], filter='279 species; a species counts once per WGSRPD level-3 region with at least one native cell; top 20 regions')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=1.0, bottom=0.5, right=0.15, top=0.45); Sm = FD.env(); nm = FD.region_names(); cnt = {}
    for s in Sm.regions.dropna():
        for code in set(re.findall(r'([A-Z]{3}) \(', s)): cnt[code] = cnt.get(code, 0) + 1
    c = pd.Series(cnt).sort_values(ascending=False).head(20).iloc[::-1]; y = np.arange(len(c)); ax.barh(y, c.values, color=S.MAIN, height=0.7, lw=0)
    ax.set_yticks(y); ax.set_yticklabels([nm.get(k, k) for k in c.index], fontsize=S.TICK - 2.5); ax.set_xlabel('Species (n)')
    for yi, v in zip(y, c.values): ax.text(v + 1.5, yi, str(v), va='center', fontsize=S.TICK - 2.5, color=S.fg(bg))
    S.title(fig, 'Native regions'); return fig, len(Sm)
