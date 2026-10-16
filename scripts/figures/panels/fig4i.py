"""Fig 4i: latitude of the native cells by element (violin; density summary only)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 4, 'i'
META = dict(chart='violin', data=['work/records_environment_primary.csv.gz', 'derived/species_environment_summary.csv'], filter='native cells of the primary basis; kernel density of latitude per element (no points drawn); white dot = median')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=1.0, bottom=0.55, right=0.2, top=0.45)
    E = FD.species_by_element(FD.env()); C = FD.cells_all()[['species_level_name', 'lat']].merge(E, left_on='species_level_name', right_on='sp'); data = [C[C.element == e].lat.values for e in FD.CORE]
    vp = ax.violinplot(data, positions=range(4), vert=False, widths=0.8, showextrema=False, bw_method=0.08)
    for b, e in zip(vp['bodies'], FD.CORE): b.set_facecolor(S.elem_color(e)); b.set_alpha(0.9); b.set_edgecolor(S.fg(bg)); b.set_linewidth(0.4)
    for i, d in enumerate(data): ax.scatter(np.median(d), i, s=12, color='white', edgecolor=S.fg(bg), lw=0.5, zorder=3)
    ax.set_yticks(range(4)); ax.set_yticklabels(['%s (n=%s)' % (e, format(len(d), ',')) for e, d in zip(FD.CORE, data)], fontsize=S.TICK - 1); ax.invert_yaxis(); ax.set_xlabel('Latitude (degrees)'); ax.axvline(0, color=S.GREY, lw=0.4, ls=':')
    S.title(fig, 'Latitude of the native cells'); return fig, int(sum(len(d) for d in data))
