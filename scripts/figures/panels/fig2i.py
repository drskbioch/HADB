"""Fig 2i: previously known vs total taxa quoted by the three screens (slope)."""
import re
import numpy as np, pandas as pd
from figures import style as S, figdata as FD, layout as L
FIG, LET = 2, 'i'
META = dict(chart='slope', data=['derived/new_vs_known_counts_papers.csv'], filter='quoted_new_vs_known rows with a previously-known count and a total (first integer of the quoted text); Queensland Mn: known 9 and total 27 taken from two quoted rows')


def first_int(s):
    m = re.match(r'\s*(\d+)', str(s)); return int(m.group(1)) if m else (0 if 'none known' in str(s) else None)


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.45, bottom=0.75, right=0.9, top=0.5)
    N = pd.read_csv(FD.DER / 'new_vs_known_counts_papers.csv', keep_default_na=False); N = N[N.row_type == 'quoted_new_vs_known']; rows = []
    for r in N.itertuples():
        if r.element_or_scope in FD.CORE:
            k, t = first_int(r.previously_known_as_quoted), first_int(r.total_as_quoted)
            if k is not None and t is not None: rows.append((r.paper.split(' ')[0], r.element_or_scope, k, t))
    q = N[N.paper.str.startswith('Queensland')]; rows.append(('Queensland', 'Mn', first_int(q[q.element_or_scope == 'Mn (Myrtaceae)'].previously_known_as_quoted.iloc[0]), first_int(q[q.element_or_scope == 'Mn'].total_as_quoted.iloc[0])))
    D = pd.DataFrame(rows, columns=['paper', 'element', 'known', 'total']).drop_duplicates(['paper', 'element'])
    for r in D.itertuples():
        ax.plot([0, 1], [r.known, r.total], color=S.elem_color(r.element), lw=S.LW_LINE, marker='o', ms=3.5)
        ax.text(1.04, r.total, '%s %s' % (r.paper, r.element), fontsize=S.TICK - 2.5, va='center', color=S.fg(bg))
    ax.set_xticks([0, 1]); ax.set_xticklabels(['previously\nknown', 'total\nquoted']); ax.set_xlim(-0.15, 1.05); ax.set_ylabel('Taxa (n)'); ax.set_yscale('symlog', linthresh=10); ax.set_ylim(-0.5, 130); ax.set_yticks([0, 5, 10, 30, 100]); ax.set_yticklabels(['0', '5', '10', '30', '100'])
    S.title(fig, 'New vs known in the three screens'); return fig, len(D)
