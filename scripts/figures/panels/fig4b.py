"""Fig 4b: records and native cells per species (ECDF, log axis) with the 20-record line."""
import numpy as np
from figures import style as S, figdata as FD, layout as L
FIG, LET = 4, 'b'
META = dict(chart='ECDF', data=['derived/species_environment_summary.csv'], filter='279 species; cleaned records (before one-per-cell) and native cells; vertical line at 20')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.6, bottom=0.55, right=0.15, top=0.45); Sm = FD.env()
    for col, lab, c in (('n_records', 'cleaned records', S.GREY), ('n_cells', 'native cells', S.MAIN)):
        x = np.sort(Sm[col].values); ax.step(x, np.arange(1, len(x) + 1) / len(x), where='post', color=c, lw=S.LW_LINE + 0.3, label=lab)
    ax.axvline(20, color=S.TIER['T2'], ls='--', lw=S.LW_LINE); ax.set_xscale('log'); ax.set_xlabel('Per species (n, log axis)'); ax.set_ylabel('Share of species'); ax.set_ylim(0, 1.02)
    k = int((Sm.n_cells >= 20).sum()); ax.text(22, 0.08, '%d of %d species\n>= 20 native cells' % (k, len(Sm)), fontsize=S.TICK - 2, color=S.fg(bg)); ax.legend(loc='upper left'); ax.grid(color=S.grid_color(bg), lw=S.LW_GRID); ax.set_axisbelow(True)
    S.title(fig, 'Records per species'); return fig, len(Sm)
