"""Fig 3b: how the master rows were matched to WCVP names (lollipop)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 3, 'b'
META = dict(chart='lollipop', data=['derived/master_species_v2.csv'], filter='all master rows by match_type (log axis)')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=1.25, bottom=0.55, right=0.2, top=0.5)
    M = pd.read_csv(FD.DER / 'master_species_v2.csv', usecols=['match_type'], low_memory=False); c = M.match_type.value_counts().sort_values(); y = np.arange(len(c))
    ax.hlines(y, 1, c.values, color=S.MAIN, lw=S.LW_LINE); ax.scatter(c.values, y, s=20, color=S.MAIN, zorder=3)
    for yi, v in zip(y, c.values): ax.text(v * 1.18, yi, format(int(v), ','), va='center', fontsize=S.TICK - 2, color=S.fg(bg))
    ax.set_yticks(y); ax.set_yticklabels([s.replace('decided_', 'decided ').replace('_', ' ').replace('abbreviation full genus', 'abbrev. + genus') for s in c.index], fontsize=S.TICK - 2); ax.set_xscale('log'); ax.set_xlim(1, 3e4)
    ax.set_xlabel('Master rows (n, log axis)'); ax.grid(axis='x', color=S.grid_color(bg), lw=S.LW_GRID); ax.set_axisbelow(True); S.title(fig, 'Name match types'); return fig, int(len(M))
