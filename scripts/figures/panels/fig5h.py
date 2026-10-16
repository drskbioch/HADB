"""Fig 5h: species medians of T1 vs T2 species (dumbbells)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 5, 'h'
META = dict(chart='dumbbell', data=['release/evidence.csv', 'release/species_element.csv', 'derived/species_environment_summary.csv'], filter='species with >= 20 native cells; T1 = best tier T1 in the headline view, T2 = best tier T2; median of species medians with quartile range')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); Sm = FD.env_ok(); t = FD.species_tier(); Sm = Sm.assign(tier=Sm.accepted_name.map(t)).dropna(subset=['tier']); vars_ = [('bio1_median_C', 'bio1 (degrees C)'), ('bio12_median_mm', 'bio12 (mm)'), ('ph_median', 'pH')]
    n1, n2 = int((Sm.tier == 'T1').sum()), int((Sm.tier == 'T2').sum())
    for k, (c, lab) in enumerate(vars_):
        ax = fig.add_axes([0.5 / w, (h - 0.5 - 0.2 - k * 0.5) / h, (w - 0.75) / w, 0.2 / h]); S.style_ax(ax, bg)
        for tt, yy in (('T1', 0.3), ('T2', -0.3)):
            v = Sm[Sm.tier == tt][c].dropna(); q = np.percentile(v, [25, 50, 75]); ax.plot([q[0], q[2]], [yy, yy], color=S.TIER[tt], lw=3, solid_capstyle='butt', alpha=0.5); ax.scatter(q[1], yy, s=22, color=S.TIER[tt], zorder=3); ax.text(q[2], yy, '  %s %.1f' % (tt, q[1]) if c != 'bio12_median_mm' else '  %s %.0f' % (tt, q[1]), va='center', fontsize=S.TICK - 2.5, color=S.fg(bg))
        ax.set_ylim(-0.7, 0.7); ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.set_xlabel(lab, fontsize=S.TICK - 1, labelpad=1)
    S.small(fig, 'T1 n=%d, T2 n=%d species; bar = quartile range' % (n1, n2), x=0.5); S.title(fig, 'T1 vs T2 species'); return fig, n1 + n2
