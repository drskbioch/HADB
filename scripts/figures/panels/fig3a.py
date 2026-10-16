"""Fig 3a: Block B rows by name class (treemap)."""
import pandas as pd, squarify
from figures import style as S, figdata as FD, layout as L
FIG, LET = 3, 'a'
META = dict(chart='treemap', data=['release/name_class_table.csv'], filter='1,065 Block B rows by name class')
COL = {'species_resolved': S.MAIN, 'rank_genus_by_design': '#D9A441', 'non_taxon': '#8C8C8C', 'unresolved': S.TIER['T2']}
LAB = {'species_resolved': 'resolved to a species', 'rank_genus_by_design': 'genus only (by design)', 'non_taxon': 'non-taxon', 'unresolved': 'unresolved'}


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = fig.add_axes([0.2 / w, 0.25 / h, (w - 0.4) / w, (h - 0.95) / h]); ax.axis('off')
    T = pd.read_csv(FD.REL / 'name_class_table.csv'); T = T[T['class'].isin(COL)].sort_values('block_b_rows', ascending=False)
    rects = squarify.squarify(squarify.normalize_sizes(T.block_b_rows.tolist(), 100, 100), 0, 0, 100, 100)
    for r, (_, row) in zip(rects, T.iterrows()):
        ax.add_patch(__import__('matplotlib').patches.Rectangle((r['x'], r['y']), r['dx'], r['dy'], facecolor=COL[row['class']], edgecolor=S.BACKGROUNDS[bg], lw=1.5))
        big = row.block_b_rows > 200; ax.text(r['x'] + r['dx'] / 2, r['y'] + r['dy'] / 2, '%s\n%d (%.1f%%)' % (LAB[row['class']], row.block_b_rows, row.pct_of_block_b_rows) if big else '%d' % row.block_b_rows, ha='center', va='center',
                                              fontsize=S.TICK - 0.5 if big else S.TICK - 2, color='white' if row['class'] != 'rank_genus_by_design' else '#1A1A1A', fontweight='bold')
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    fig.text(0.25 / w, 0.12 / h, 'genus only = 72, non-taxon = 15, unresolved = 48 rows', fontsize=S.TICK - 2, color=S.muted(bg)); S.title(fig, 'Names of the Block B rows'); return fig, int(T.block_b_rows.sum())
