"""Fig 5b: annual precipitation (bio12) of native cells by element (ridgeline), with the saturation cap."""
import numpy as np
from scipy.stats import gaussian_kde
from figures import style as S, figdata as FD, layout as L
FIG, LET = 5, 'b'
META = dict(chart='ridgeline', data=['work/records_environment_primary.csv.gz', 'derived/species_environment_summary.csv'], filter='native cells of species with >= 20 native cells; kernel density of cell values; dashed line = 6,553.5 mm uint16 ceiling of CHELSA bio12')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.5, bottom=0.55, right=0.15, top=0.45)
    E = FD.species_by_element(FD.env_ok()); C = FD.cells_ok()[['species_level_name', 'bio12_mm']].merge(E, left_on='species_level_name', right_on='sp'); xs = np.linspace(0, 7000, 300); n = 0
    for i, e in enumerate(FD.CORE[::-1]):
        v = C[C.element == e].bio12_mm.dropna().values; n += len(v); d = gaussian_kde(v, bw_method=0.1)(xs); d = d / d.max() * 0.95
        ax.fill_between(xs, i, i + d, color=S.elem_color(e), alpha=0.85, lw=0); ax.plot(xs, i + d, color=S.fg(bg), lw=0.4); ax.text(6900, i + 0.12, '%s (n=%s)' % (e, format(len(v), ',')), ha='right', fontsize=S.TICK - 2, color=S.fg(bg), va='bottom')
    ax.axvline(6553.5, color=S.TIER['T2'], ls='--', lw=S.LW_LINE); ax.text(6500, 3.75, 'cap 6,553.5 mm\n(saturated)', ha='right', va='top', fontsize=S.TICK - 2.5, color=S.TIER['T2'])
    ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.set_xlim(0, 7000); ax.set_ylim(0, 4.1); ax.set_xlabel('Annual precipitation (mm)'); S.title(fig, 'Precipitation (bio12)'); return fig, n
