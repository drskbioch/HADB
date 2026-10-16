"""Fig 5a: mean annual temperature (bio1) of species by element (raincloud: density of species medians, box, points = species medians)."""
import numpy as np
from scipy.stats import gaussian_kde
from figures import style as S, figdata as FD, layout as L
FIG, LET = 5, 'a'
META = dict(chart='raincloud', data=['derived/species_environment_summary.csv'], filter='species with >= 20 native cells (198); one value per species (its median over native cells); a species counts under every element')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.5, bottom=0.55, right=0.15, top=0.45); Sm = FD.env_ok(); E = FD.species_by_element(Sm).merge(Sm[['accepted_name', 'bio1_median_C']], left_on='sp', right_on='accepted_name'); xs = np.linspace(0, 32, 200); rng = np.random.default_rng(1)
    for i, e in enumerate(FD.CORE[::-1]):
        v = E[E.element == e].bio1_median_C.values; d = gaussian_kde(v)(xs); d = d / d.max() * 0.42
        ax.fill_between(xs, i + 0.12, i + 0.12 + d, color=S.elem_color(e), alpha=0.8, lw=0); ax.scatter(v, i - 0.16 + rng.uniform(-0.1, 0.1, len(v)), s=3, color=S.elem_color(e), alpha=0.7, lw=0)
        q = np.percentile(v, [25, 50, 75]); ax.plot([q[0], q[2]], [i + 0.02, i + 0.02], color=S.fg(bg), lw=1.6, solid_capstyle='butt'); ax.scatter(q[1], i + 0.02, s=8, color='white', edgecolor=S.fg(bg), lw=0.5, zorder=3)
        ax.text(31.5, i + 0.15, 'n=%d' % len(v), ha='right', fontsize=S.TICK - 2.5, color=S.muted(bg))
    ax.set_yticks(range(4)); ax.set_yticklabels(FD.CORE[::-1]); ax.set_xlim(0, 32); ax.set_xlabel('bio1, species median (degrees C)'); S.title(fig, 'Temperature (bio1)'); return fig, len(Sm)
