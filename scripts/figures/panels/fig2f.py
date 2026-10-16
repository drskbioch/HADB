"""Fig 2f: cumulative species vs number of citing articles (step)."""
import numpy as np
from figures import style as S, figdata as FD, layout as L
FIG, LET = 2, 'f'
META = dict(chart='step curve', data=['release/evidence.csv', 'release/species_element.csv'], filter='headline view; citations ordered by the number of species each cites (largest first); y = cumulative distinct species')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.6, bottom=0.55, right=0.15, top=0.5)
    E = FD.evidence(); g = E.groupby('citation').sp.apply(set); order = g.map(len).sort_values(ascending=False).index; seen = set(); y = []
    for c in order: seen |= g[c]; y.append(len(seen))
    x = np.arange(1, len(y) + 1); tot = y[-1]; ax.step(x, y, where='post', color=S.MAIN, lw=S.LW_LINE + 0.4); ax.set_xscale('log')
    for fr in (0.5, 0.9):
        k = int(np.argmax(np.array(y) >= fr * tot)) + 1; ax.scatter(k, y[k - 1], s=18, color=S.TIER['T2'], zorder=3); ax.text(k * 0.8, y[k - 1] - 0.05 * tot, '%d%% of species\nin %d citations' % (fr * 100, k), fontsize=S.TICK - 2, color=S.fg(bg), va='top', ha='right')
    ax.set_xlabel('Citations, largest first (n, log axis)'); ax.set_ylabel('Cumulative species (n)'); ax.set_ylim(0, tot * 1.05); ax.grid(color=S.grid_color(bg), lw=S.LW_GRID); ax.set_axisbelow(True)
    S.title(fig, 'Species vs citing articles'); return fig, len(y)
