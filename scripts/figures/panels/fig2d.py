"""Fig 2d: best threshold class per species and element (radial stacked bars, square-root radius)."""
import numpy as np
from figures import style as S, figdata as FD, layout as L
FIG, LET = 2, 'd'
META = dict(chart='radial stacked bars', data=['release/evidence.csv', 'release/species_element.csv'], filter='headline view, Ni Mn Zn Co, best threshold class per species x element; radius = sqrt(cumulative species)')
RANK = {'high-range': 0, 'standard': 1, 'label-only': 2}


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg)
    ax = fig.add_axes([0.2 / w, 0.7 / h, (w - 0.4) / w, (h - 1.3) / h], projection='polar'); ax.set_facecolor('none')
    E = FD.evidence(); E = E[E.element.isin(FD.CORE)].assign(r=lambda d: d.threshold_class.map(RANK)); P = E.groupby(['sp', 'element']).r.min().reset_index()
    ang = np.linspace(0, 2 * np.pi, 4, endpoint=False) + np.pi / 4; n = len(P)
    for a, e in zip(ang, FD.CORE):
        c = P[P.element == e].r.value_counts().reindex([0, 1, 2], fill_value=0); cum = 0
        for r, al in ((0, 1.0), (1, 0.6), (2, 0.28)):
            lo, hi = np.sqrt(cum), np.sqrt(cum + c[r]); ax.bar(a, hi - lo, width=np.pi / 2 * 0.78, bottom=lo, color=S.elem_color(e), alpha=al, lw=0); cum += c[r]
        ax.text(a, np.sqrt(cum) + 2.2, '%s\n%d' % (e, cum), ha='center', va='center', fontsize=S.TICK - 1, color=S.fg(bg), fontweight='bold')
    ax.set_ylim(0, 27); ax.set_yticks([]); ax.set_xticks([]); ax.spines['polar'].set_visible(False); ax.grid(False)
    from matplotlib.patches import Rectangle
    for j, (t, al) in enumerate((('high-range', 1.0), ('standard', 0.6), ('label-only', 0.28))):
        x0 = 0.3 + 0.7 * j; fig.add_artist(Rectangle((x0 / w, 0.3 / h), 0.1 / w, 0.1 / h, transform=fig.transFigure, color=S.fg(bg), alpha=al, lw=0)); fig.text((x0 + 0.14) / w, 0.35 / h, t, fontsize=S.TICK - 2, color=S.fg(bg), va='center')
    S.title(fig, 'Threshold class by element'); return fig, n
