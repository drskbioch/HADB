"""Fig 5c: species medians of bio1 vs bio12 with marginal histograms."""
import numpy as np
from figures import style as S, figdata as FD, layout as L
FIG, LET = 5, 'c'
META = dict(chart='scatter + marginals', data=['derived/species_environment_summary.csv'], filter='species with >= 20 native cells; colour = first element present in the order Ni, Co, Mn, Zn')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); Sm = FD.env_ok(); col = [S.elem_color(FD.primary_element(FD.elements_of(s))) for s in Sm.elements_in_hadb]
    ax = fig.add_axes([0.5 / w, 0.55 / h, (w - 1.0) / w, (h - 1.5) / h]); S.style_ax(ax, bg); ax.scatter(Sm.bio1_median_C, Sm.bio12_median_mm, s=7, c=col, alpha=0.85, lw=0)
    ax.set_xlabel('bio1 species median (degrees C)'); ax.set_ylabel('bio12 species median (mm)')
    top = fig.add_axes([0.5 / w, (h - 0.95) / h, (w - 1.0) / w, 0.5 / h]); S.style_ax(top, bg); top.hist(Sm.bio1_median_C, bins=24, color=S.GREY, lw=0); top.set_xlim(ax.get_xlim()); top.set_xticks([]); top.set_yticks([]); top.spines['left'].set_visible(False)
    rt = fig.add_axes([(w - 0.5) / w, 0.55 / h, 0.4 / w, (h - 1.5) / h]); S.style_ax(rt, bg); rt.hist(Sm.bio12_median_mm, bins=24, orientation='horizontal', color=S.GREY, lw=0); rt.set_ylim(ax.get_ylim()); rt.set_xticks([]); rt.set_yticks([]); rt.spines['bottom'].set_visible(False)
    for j, e in enumerate(FD.CORE): fig.text((0.55 + 0.45 * j) / w, 0.12 / h, e, color=S.elem_color(e), fontsize=S.TICK - 1, fontweight='bold')
    S.title(fig, 'Climate space of the species'); return fig, len(Sm)
