"""Fig 4f: basis of record of the native cells by element (100% stacked)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 4, 'f'
META = dict(chart='100% stacked bars', data=['work/records_environment_primary.csv.gz', 'derived/species_environment_summary.csv'], filter='native cells of the primary basis; a cell counts under every element of its species')
COL = {'HUMAN_OBSERVATION': S.ACCENT, 'PRESERVED_SPECIMEN': S.MAIN, 'MATERIAL_SAMPLE': '#D9A441', 'OBSERVATION': '#8C8C8C'}


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.7, bottom=0.95, right=0.15, top=0.45)
    E = FD.species_by_element(FD.env()); C = FD.cells_all()[['species_level_name', 'basisOfRecord']].merge(E, left_on='species_level_name', right_on='sp'); P = pd.crosstab(C.element, C.basisOfRecord).reindex(index=FD.CORE, columns=list(COL), fill_value=0)
    Q = P.div(P.sum(axis=1), axis=0) * 100; left = np.zeros(4); y = np.arange(4)[::-1]
    for k in COL: ax.barh(y, Q[k], left=left, color=COL[k], height=0.62, lw=0, label=k.replace('_', ' ').lower()); left += Q[k].values
    ax.set_yticks(y); ax.set_yticklabels(['%s (%s)' % (e, format(int(P.loc[e].sum()), ',')) for e in FD.CORE], fontsize=S.TICK - 2); ax.set_xlim(0, 100); ax.set_xlabel('Share of native cells (%)')
    ax.legend(loc='upper center', bbox_to_anchor=(0.4, -0.3), ncol=2, handlelength=1, columnspacing=0.8, fontsize=S.TICK - 2.5); S.title(fig, 'Basis of record'); return fig, int(P.values.sum())
