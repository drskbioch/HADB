"""Fig 4e: T1 species by the region studied in the source (lollipop)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 4, 'e'
META = dict(chart='lollipop', data=['release/evidence.csv', 'release/species_element.csv'], filter='headline view, tier T1 evidence rows; region = region studied by the source (Gei 2020 XRF: New Caledonia; Sabah paper: Sabah, Borneo; Purwadi 2023: Queensland); a species counts once per source')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=1.15, bottom=0.55, right=0.3, top=0.5)
    E = FD.evidence(); E = E[E.tier == 'T1']; reg = np.where(E.evidence_type == 'gei_xrf_taxon', 'New Caledonia (Gei 2020 XRF)', np.where(E.citation.str.contains('Purwadi'), 'Queensland (Purwadi 2023)', np.where(E.citation.str.contains('2019b'), 'Sabah (van der Ent 2019)', 'other')))
    E = E.assign(reg=reg); c = E.groupby('reg').sp.nunique().sort_values(); y = np.arange(len(c))
    ax.hlines(y, 0, c.values, color=S.MAIN, lw=S.LW_LINE); ax.scatter(c.values, y, s=24, color=S.MAIN, zorder=3)
    for yi, v in zip(y, c.values): ax.text(v + 6, yi, str(v), va='center', fontsize=S.TICK - 1.5, color=S.fg(bg))
    ax.set_yticks(y); ax.set_yticklabels(c.index, fontsize=S.TICK - 2.5); ax.set_xlabel('T1 species (n)'); ax.set_xlim(0, c.max() * 1.18)
    S.small(fig, 'a species counts once per source; sources overlap'); S.title(fig, 'T1 species by source region'); return fig, int(E.sp.nunique())
