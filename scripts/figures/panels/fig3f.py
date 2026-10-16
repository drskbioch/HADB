"""Fig 3f: what the headline view removes, by reason (dot plot)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 3, 'f'
META = dict(chart='dot plot', data=['release/evidence.csv', 'release/species_element.csv'], filter='all evidence rows of rc3; pairs = species x element lost when every row of the pair is removed')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=1.25, bottom=0.7, right=0.2, top=0.5)
    E = FD.evidence_all(); flags = {'suspect source (CORE PDF)': E.suspect_source == 'Y', 'weakened (red, not confirmed)': E.weakened == 'Y', 'inferred citation (DOI replaced)': E.citation_inferred == 'Y', 'any reason': ~E.headline}
    g = E.assign(rm=~E.headline).groupby(['species', 'element']).rm.all(); lost = set(g[g].index); rows = []
    for k, m in flags.items():
        gg = E.assign(m=m).groupby(['species', 'element']).m.all(); rows.append((k, int(m.sum()), len(set(gg[gg].index) & lost) if k != 'any reason' else len(lost)))
    D = pd.DataFrame(rows, columns=['reason', 'rows', 'pairs']).iloc[::-1]; y = np.arange(len(D))
    ax.hlines(y, D.pairs.clip(lower=0.8), D.rows, color=S.GREY, lw=S.LW_LINE); ax.scatter(D.rows, y, s=24, color=S.MAIN, zorder=3, label='evidence rows'); ax.scatter(D.pairs.clip(lower=0.8), y, s=24, color=S.TIER['T2'], zorder=3, label='pairs lost')
    for yi, a, b in zip(y, D.rows, D.pairs): ax.text(max(a, b) * 1.3, yi, '%d / %d' % (a, b), va='center', fontsize=S.TICK - 2.5, color=S.fg(bg))
    ax.set_xscale('log'); ax.set_xlim(0.7, 2000); ax.set_yticks(y); ax.set_yticklabels(D.reason, fontsize=S.TICK - 2.5); ax.set_xlabel('Count (n, log axis)'); ax.legend(loc='lower right'); ax.grid(axis='x', color=S.grid_color(bg), lw=S.LW_GRID); ax.set_axisbelow(True)
    S.title(fig, 'Removed from the headline view'); return fig, len(E)
