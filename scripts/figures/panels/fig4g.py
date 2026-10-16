"""Fig 4g: licence of all downloaded records by element (stacked columns)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 4, 'g'
META = dict(chart='stacked columns', data=['work/records_flags_all.csv.gz', 'derived/species_environment_summary.csv'], filter='all 101,048 downloaded records (before cleaning); a record counts under every element of its species')
COL = {'CC0_1_0': S.ACCENT, 'CC_BY_4_0': S.MAIN, 'CC_BY_NC_4_0': S.TIER['T2']}


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.65, bottom=0.95, right=0.15, top=0.45)
    E = FD.species_by_element(FD.env()); F = FD.flags(); C = F.merge(E, left_on='species_level_name', right_on='sp'); P = pd.crosstab(C.element, C.licence).reindex(index=FD.CORE, columns=list(COL), fill_value=0); bottom = np.zeros(4); x = np.arange(4)
    for k in COL: ax.bar(x, P[k], bottom=bottom, color=COL[k], width=0.66, lw=0, label=k.replace('_', ' ').replace(' 1 0', ' 1.0').replace(' 4 0', ' 4.0').replace('NC 4.0', 'NC 4.0')); bottom += P[k].values
    ax.set_xticks(x); ax.set_xticklabels(FD.CORE); ax.set_ylabel('Records (n)'); ax.legend(loc='upper center', bbox_to_anchor=(0.45, -0.18), ncol=3, handlelength=1, columnspacing=0.6, fontsize=S.TICK - 2.5)
    ax.yaxis.set_major_formatter(__import__('matplotlib').ticker.FuncFormatter(lambda v, p: format(int(v), ','))); S.title(fig, 'Licence of the records'); return fig, int(len(F))
