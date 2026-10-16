"""Fig 4a: density of cleaned native cells (hexbin on a Natural Earth base map; no point dots)."""
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from figures import style as S, figdata as FD, layout as L
FIG, LET = 4, 'a'
META = dict(chart='hexbin map', data=['work/records_environment_primary.csv.gz'], filter='primary basis (non-NC, cleaned, one record per species per cell), native only; hexagon counts only, log colour scale; base map Natural Earth 110 m (pyogrio fixture)')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.35, bottom=0.45, right=0.55, top=0.42)
    C = FD.cells_all(); FD.land().plot(ax=ax, color='#E4E4E4' if bg != 'navy' else '#1F3A63', edgecolor='none', zorder=0)
    cm = LinearSegmentedColormap.from_list('hadb', S.SEQ[1:]); hb = ax.hexbin(C.lon, C.lat, gridsize=(110, 45), extent=(-180, 180, -58, 80), bins='log', mincnt=1, cmap=cm, linewidths=0, zorder=2)
    ax.set_xlim(-180, 180); ax.set_ylim(-58, 80); ax.set_aspect('equal'); ax.set_xticks([-120, -60, 0, 60, 120]); ax.set_yticks([-40, 0, 40, 80]); ax.tick_params(labelsize=S.TICK - 1.5)
    cb = fig.colorbar(hb, ax=ax, fraction=0.025, pad=0.01, shrink=0.8); cb.ax.tick_params(labelsize=S.TICK - 2, length=1.5, colors=S.fg(bg)); cb.set_label('Native cells per hexagon (log)', fontsize=S.TICK - 1.5, color=S.fg(bg)); cb.outline.set_linewidth(0.3)
    S.title(fig, 'Where the cleaned native cells are'); return fig, int(len(C))
