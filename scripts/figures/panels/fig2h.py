"""Fig 2h: scope of evidence rows by source (100% stacked)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 2, 'h'
META = dict(chart='100% stacked bars', data=['release/evidence.csv'], filter='headline view evidence rows, evidence_type x scope')
SC = {'hyperaccumulation': S.MAIN, 'phytoremediation': '#D9A441', 'unknown': '#B8B8B8', 'other': '#5C6B7A'}
LAB = {'block_b_label': 'Block B', 'gei_xrf_taxon': 'Gei XRF', 'gei_literature_update': 'Gei lists', 'paper_table': 'Papers'}


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.8, bottom=0.95, right=0.15, top=0.5)
    E = FD.evidence(); E['scope2'] = E.scope.where(E.scope.isin(['hyperaccumulation', 'phytoremediation', 'unknown']), 'other')
    P = pd.crosstab(E.evidence_type, E.scope2).reindex(index=list(LAB), columns=list(SC), fill_value=0); Q = P.div(P.sum(axis=1), axis=0) * 100; left = np.zeros(len(Q)); y = np.arange(len(Q))[::-1]
    for sc in SC: ax.barh(y, Q[sc], left=left, color=SC[sc], height=0.62, lw=0, label=sc); left += Q[sc].values
    ax.set_yticks(y); ax.set_yticklabels([LAB[i] + ' (n=%d)' % P.loc[i].sum() for i in Q.index], fontsize=S.TICK - 1.5); ax.set_xlim(0, 100); ax.set_xlabel('Share of evidence rows (%)')
    ax.legend(loc='upper center', bbox_to_anchor=(0.45, -0.28), ncol=2, handlelength=1, columnspacing=0.8); S.title(fig, 'Scope of the evidence by source'); return fig, int(P.values.sum())
