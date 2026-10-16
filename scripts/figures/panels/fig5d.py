"""Fig 5d: soil pH of native cells by element (violin) with species medians (swarm)."""
import numpy as np
from figures import style as S, figdata as FD, layout as L
FIG, LET = 5, 'd'
META = dict(chart='violin + swarm', data=['work/records_environment_primary.csv.gz', 'derived/species_environment_summary.csv'], filter='native cells of species with >= 20 native cells with a SoilGrids value (violin); points = species medians; pH = stored integer / 10')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.5, bottom=0.55, right=0.15, top=0.45); Sm = FD.env_ok(); E = FD.species_by_element(Sm); rng = np.random.default_rng(2)
    C = FD.cells_ok()[['species_level_name', 'ph_h2o_0_5cm']].dropna().merge(E, left_on='species_level_name', right_on='sp'); M = E.merge(Sm[['accepted_name', 'ph_median']], left_on='sp', right_on='accepted_name').dropna(subset=['ph_median']); n = 0
    data = [C[C.element == e].ph_h2o_0_5cm.values for e in FD.CORE]; n = sum(len(d) for d in data)
    vp = ax.violinplot(data, positions=range(4), widths=0.85, showextrema=False, bw_method=0.15)
    for b, e in zip(vp['bodies'], FD.CORE): b.set_facecolor(S.elem_color(e)); b.set_alpha(0.55); b.set_edgecolor('none')
    for i, e in enumerate(FD.CORE):
        v = M[M.element == e].ph_median.values; ax.scatter(i + rng.uniform(-0.22, 0.22, len(v)), v, s=3.5, color=S.elem_color(e), edgecolor=S.fg(bg), lw=0.15, zorder=3)
    ax.set_xticks(range(4)); ax.set_xticklabels(FD.CORE); ax.set_ylabel('Soil pH (water, 0-5 cm)'); S.title(fig, 'Soil pH'); return fig, n
