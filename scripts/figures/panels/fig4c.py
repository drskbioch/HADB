"""Fig 4c: records left after each cleaning step (waterfall from the logged step counts)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 4, 'c'
META = dict(chart='waterfall', data=['work/survival_table.csv', 'work/records_environment_primary.csv.gz'], filter='primary basis (non-NC records); steps from survival_table.csv; uncertainty-missing share from the final native cells')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=1.15, bottom=0.55, right=0.2, top=0.45)
    V = pd.read_csv(FD.WRK / 'survival_table.csv'); V = V[V.variant == 'primary'].reset_index(drop=True); rec = V.records.tolist(); st = V.step.tolist()
    def at(prefix): return rec[[i for i, s in enumerate(st) if s.startswith(prefix)][0]]
    start, zero, eq, unc, hq, cen, inst, cell, nat = at('0 '), at('1b'), at('1c'), at('2 '), at('3a'), at('3b'), at('3c'), at('4 '), at('5 ')
    steps = [('start (non-NC)', start, 'total'), ('zero / equal coordinates', zero - start + eq - zero, 'delta'), ('uncertainty > 10 km', unc - eq, 'delta'), ('GBIF HQ, centroid', cen - unc, 'delta'), ('institution text proxy', inst - cen, 'delta'),
             ('one per species per cell', cell - inst, 'delta'), ('native only', nat - cell, 'delta'), ('final native cells', nat, 'total')]
    y = np.arange(len(steps))[::-1]; level = 0
    for yi, (lab, v, kind) in zip(y, steps):
        if kind == 'total': ax.barh(yi, v, color=S.MAIN, height=0.62, lw=0); level = v; ax.text(v + 1500, yi, format(v, ','), va='center', fontsize=S.TICK - 2, color=S.fg(bg))
        else: ax.barh(yi, -v, left=level + v, color=S.TIER['T2'], height=0.62, lw=0); ax.text(level + 1500, yi, format(v, ','), va='center', fontsize=S.TICK - 2, color=S.fg(bg)); level += v
    ax.set_yticks(y); ax.set_yticklabels([s[0] for s in steps], fontsize=S.TICK - 2); ax.set_xlabel('Records (n)'); ax.set_xlim(0, start * 1.2); share = 100 * FD.cells_all().unc_null.mean()
    S.small(fig, 'no coordinate uncertainty recorded in %.1f%% of final cells (kept, flagged)' % share); S.title(fig, 'Cleaning of the occurrence records'); return fig, int(start)
