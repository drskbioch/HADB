"""Fig 5e: completeness of the environment data by layer and element (stacked bars)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 5, 'e'
META = dict(chart='stacked bars', data=['work/records_environment_primary.csv.gz', 'derived/species_environment_summary.csv'], filter='all native cells of the species of each element; insufficient records = cells of species with < 20 native cells (no statistics); saturated = bio12 raw value 65535; missing = SoilGrids nodata')
COL = {'valid': S.MAIN, 'saturated': '#D9A441', 'missing': '#8C8C8C', 'insufficient records': S.TIER['T2']}


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.85, bottom=1.0, right=0.15, top=0.45); Sm = FD.env(); ok = set(Sm[Sm.meets_20_cells == 'Y'].accepted_name)
    E = FD.species_by_element(Sm); C = FD.cells_all()[['species_level_name', 'bio12_raw', 'ph_h2o_0_5cm', 'bio1_c']].merge(E, left_on='species_level_name', right_on='sp'); C['ok'] = C.species_level_name.isin(ok); rows = []; labels = []
    for e in FD.CORE:
        g = C[C.element == e]; N = len(g); ins = int((~g.ok).sum()); gg = g[g.ok]
        for layer in ('bio1', 'bio12', 'pH'):
            sat = int((gg.bio12_raw == 65535).sum()) if layer == 'bio12' else 0; mis = int(gg.ph_h2o_0_5cm.isna().sum()) if layer == 'pH' else int(gg.bio1_c.isna().sum()) if layer == 'bio1' else 0
            rows.append([100 * (len(gg) - sat - mis) / N, 100 * sat / N, 100 * mis / N, 100 * ins / N]); labels.append('%s %s' % (e, layer))
    P = np.array(rows); y = np.array([i + (i // 3) * 0.5 for i in range(len(rows))])[::-1]; left = np.zeros(len(rows))
    for j, k in enumerate(COL): ax.barh(y, P[:, j], left=left, color=COL[k], height=0.8, lw=0, label=k); left += P[:, j]
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=S.TICK - 2.5); ax.set_xlim(0, 100); ax.set_xlabel('Share of native cells (%)'); ax.legend(loc='upper center', bbox_to_anchor=(0.35, -0.2), ncol=2, handlelength=1, columnspacing=0.8, fontsize=S.TICK - 2.5)
    S.title(fig, 'Completeness of the environment data'); return fig, int(len(FD.cells_all()))
