"""Fig 3d: reconciliation from Block B rows to evidence rows (waterfall)."""
import numpy as np, pandas as pd
from matplotlib.patches import Rectangle
from figures import style as S, figdata as FD, layout as L
FIG, LET = 3, 'd'
META = dict(chart='waterfall', data=['release/block_b_row_accounting.csv', 'derived/master_species_v2.csv', 'release/evidence.csv', 'release/species_element.csv'], filter='Block B only; units change between steps (rows, master rows, evidence rows, species x element pairs)')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.65, bottom=1.0, right=0.2, top=0.5)
    A = pd.read_csv(FD.REL / 'block_b_row_accounting.csv'); M = pd.read_csv(FD.DER / 'master_species_v2.csv', usecols=['evidence_type'], low_memory=False); E = FD.evidence_all(); Eb = E[E.evidence_type == 'block_b_label']
    n0, n1 = len(A), int((A.bucket == 'master').sum()); mrows = int((M.evidence_type == 'block_b_label').sum()); ev = len(Eb); prs = Eb.drop_duplicates(['species', 'element']).shape[0]
    steps = [('Block B rows', n0, 'total'), ('not in master\n(genus, non-taxon,\nunresolved, blank)', n1 - n0, 'delta'), ('rows in master', n1, 'total'), ('master rows\n(name x element)', mrows - n1, 'delta'), ('master rows', mrows, 'total'),
             ('one row per\ncitation', ev - mrows, 'delta'), ('evidence rows', ev, 'total'), ('merged to\nspecies x element', prs - ev, 'delta'), ('species x element\npairs', prs, 'total')]
    level = 0
    for i, (lab, v, kind) in enumerate(steps):
        if kind == 'total': ax.bar(i, v, color=S.MAIN, width=0.7, lw=0); level = v; ax.text(i, v + 60, format(v, ','), ha='center', fontsize=S.TICK - 1.5, color=S.fg(bg))
        else:
            lo, hi = (level, level + v) if v >= 0 else (level + v, level); ax.bar(i, hi - lo, bottom=lo, color=S.ACCENT if v >= 0 else S.TIER['T2'], width=0.7, lw=0); ax.text(i, hi + 60, ('+' if v >= 0 else '') + format(v, ','), ha='center', fontsize=S.TICK - 1.5, color=S.fg(bg)); level += v
    ax.set_xticks(range(len(steps))); ax.set_xticklabels([s[0] for s in steps], fontsize=S.TICK - 2.5, rotation=0); ax.set_ylabel('Count (n)'); ax.set_ylim(0, max(mrows, ev) * 1.12); S.title(fig, 'From Block B rows to evidence rows'); return fig, n0
