"""Fig 3c: spelling similarity of the fuzzy / spelling matches accepted by decision (histogram + rug)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 3, 'c'
META = dict(chart='histogram + rug', data=['derived/name_review.csv', 'derived/name_decisions_step6.csv', 'derived/pending_positives.csv', 'derived/unresolved_names_review_v3.csv'],
            filter='accepted non-exact name matches with a spelling similarity (abbreviations excluded: their similarity is an expansion, not a spelling score); one value per input name')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.55, bottom=0.55, right=0.15, top=0.5); v = {}
    a = pd.read_csv(FD.DER / 'name_review.csv'); a = a[a.decision == 'accept']; v.update({r.input: r.similarity for r in a.itertuples()})
    b = pd.read_csv(FD.DER / 'name_decisions_step6.csv'); b = b[(b.applied == 'Y') & b['sim'].notna()]; v.update({r.name_as_published: r.sim for r in b.itertuples() if r.name_as_published not in v})
    c = pd.read_csv(FD.DER / 'pending_positives.csv'); c = c[c.decision == 'accept']; v.update({r.gei_name: r.nearest1_similarity for r in c.itertuples() if r.gei_name not in v})
    d = pd.read_csv(FD.DER / 'unresolved_names_review_v3.csv', keep_default_na=False); d = d[(d.decision == 'accept') & (d.match_class == 'spelling_manual')]; v.update({r.input_name: float(r.similarity) for r in d.itertuples() if r.input_name not in v})
    x = np.array(list(v.values())) / 100.0; bins = np.arange(0.86, 1.0001, 0.01); ax.hist(x, bins=bins, color=S.MAIN, lw=0.4, edgecolor=S.BACKGROUNDS[bg]); ax.axvline(0.95, color=S.TIER['T2'], lw=S.LW_LINE, ls='--')
    ax.plot(x, np.full_like(x, -0.35), '|', color=S.fg(bg), ms=5, mew=0.5, clip_on=False); ax.set_xlim(0.86, 1.0); ax.set_ylim(0, None); ax.set_xlabel('Spelling similarity (0 to 1)'); ax.set_ylabel('Names (n)')
    ax.text(0.951, ax.get_ylim()[1] * 0.92, '0.95', color=S.TIER['T2'], fontsize=S.TICK - 1); fig.text(0.55 / w, 0.12 / h, '%d of %d below 0.95' % ((x < 0.95).sum(), len(x)), fontsize=S.TICK - 2, color=S.muted(bg))
    S.title(fig, 'Similarity of accepted matches'); return fig, len(x)
