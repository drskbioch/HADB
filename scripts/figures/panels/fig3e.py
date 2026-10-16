"""Fig 3e: Gei XRF species by threshold class vs headline T1 species."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 3, 'e'
META = dict(chart='grouped bars', data=['release/evidence.csv', 'release/species_element.csv', 'release/counts.csv'], filter='species per element: Gei XRF evidence (headline view) with best threshold class high-range or standard; all headline T1 species')
RANK = {'high-range': 0, 'standard': 1, 'label-only': 2}


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.55, bottom=0.75, right=0.12, top=0.5)
    E = FD.evidence(); G = E[(E.evidence_type == 'gei_xrf_taxon') & E.element.isin(FD.CORE)].assign(r=lambda d: d.threshold_class.map(RANK)); P = G.groupby(['sp', 'element']).r.min().reset_index(); C = FD.counts_headline(); x = np.arange(4); wd = 0.26
    hi = [int(((P.element == e) & (P.r == 0)).sum()) for e in FD.CORE]; st = [int(((P.element == e) & (P.r == 1)).sum()) for e in FD.CORE]; t1 = [FD.n_of(C, e, 'T1') for e in FD.CORE]
    for k, (vals, lab, al) in enumerate(((hi, 'Gei XRF, high-range', 1.0), (st, 'Gei XRF, standard only', 0.55), (t1, 'headline T1 (all sources)', 0.25))):
        for i, e in enumerate(FD.CORE): ax.bar(i + (k - 1) * wd, vals[i], width=wd * 0.92, color=S.elem_color(e), alpha=al, lw=0, label=lab if i == 0 else None)
        for i, v in enumerate(vals): ax.text(i + (k - 1) * wd, v + 3, str(v), ha='center', fontsize=S.TICK - 3, color=S.fg(bg))
    ax.set_xticks(x); ax.set_xticklabels(FD.CORE); ax.set_ylabel('Species (n)'); ax.legend(loc='upper right', handlelength=1, labelcolor=S.fg(bg)); S.title(fig, 'Thresholds in the Gei screen'); return fig, int(len(P))
