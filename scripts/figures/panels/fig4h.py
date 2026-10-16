"""Fig 4h: collection year of the native cells by element (ridgeline)."""
import numpy as np, pandas as pd
from scipy.stats import gaussian_kde
from figures import style as S, figdata as FD, layout as L
FIG, LET = 4, 'h'
META = dict(chart='ridgeline', data=['work/records_environment_primary.csv.gz', 'derived/species_environment_summary.csv'], filter='native cells of the primary basis with a year (1850 to 2026); Gaussian kernel density, area-normalised')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.55, bottom=0.55, right=0.15, top=0.45)
    E = FD.species_by_element(FD.env()); C = FD.cells_all()[['species_level_name', 'year']].merge(E, left_on='species_level_name', right_on='sp'); C['year'] = pd.to_numeric(C.year, errors='coerce'); C = C[C.year.between(1850, 2026)]; xs = np.linspace(1850, 2026, 300); n = 0
    for i, e in enumerate(FD.CORE[::-1]):
        v = C[C.element == e].year.values; n += len(v); d = gaussian_kde(v, bw_method=0.12)(xs); d = d / d.max() * 0.95; ax.fill_between(xs, i, i + d, color=S.elem_color(e), alpha=0.85, lw=0); ax.plot(xs, i + d, color=S.fg(bg), lw=0.4)
        ax.text(1852, i + 0.12, '%s (n=%s)' % (e, format(len(v), ',')), fontsize=S.TICK - 2, color=S.fg(bg), va='bottom')
    ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.set_xlabel('Collection year'); ax.set_xlim(1850, 2026); S.title(fig, 'Collection year'); return fig, n
