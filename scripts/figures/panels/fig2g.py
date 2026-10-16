"""Fig 2g: Block B rows of the ten largest PMIDs with cumulative share (bars + line)."""
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 2, 'g'
META = dict(chart='bar + line', data=['release/top10_pmids_by_block_b_rows.csv'], filter='top 10 PMIDs by Block B rows; share of the 1,065 Block B rows')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.6, bottom=0.85, right=0.6, top=0.5)
    T = pd.read_csv(FD.REL / 'top10_pmids_by_block_b_rows.csv'); x = np.arange(len(T)); ax.bar(x, T.block_b_rows, color=S.MAIN, width=0.65, lw=0)
    ax.set_xticks(x); ax.set_xticklabels(T.pmid.astype(str), rotation=90, fontsize=S.TICK - 2); ax.set_ylabel('Block B rows (n)'); ax2 = ax.twinx(); ax2.plot(x, T.cumulative_share_of_1065 * 100, color=S.TIER['T2'], marker='o', ms=3, lw=S.LW_LINE)
    ax2.set_ylim(0, 100); ax2.set_ylabel('Cumulative share of 1,065 rows (%)', color=S.TIER['T2']); ax2.tick_params(colors=S.TIER['T2'], labelcolor=S.TIER['T2'])
    for s in ('top',): ax2.spines[s].set_visible(False)
    ax2.spines['right'].set_color(S.TIER['T2']); ax.set_xlabel('PMID, ranked by rows'); S.title(fig, 'Ten articles hold most Block B rows'); return fig, 1065
