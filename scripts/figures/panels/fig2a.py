"""Fig 2a: species per element by best tier (lollipop). Headline view counts.csv."""
from figures import style as S, figdata as FD, layout as L
FIG, LET = 2, 'a'
META = dict(chart='lollipop', data=['release/counts.csv'], filter='headline view, scope all, best tier T1 / T2, elements Ni Mn Zn Co Cd Se')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.5, bottom=0.62, right=0.2, top=0.5)
    C = FD.counts_headline(); els = FD.SIX[::-1]
    for i, e in enumerate(els):
        for t, dy, fill in (('T1', 0.17, True), ('T2', -0.17, False)):
            v = FD.n_of(C, e, t); col = S.elem_color(e)
            ax.hlines(i + dy, 0, v, color=col, lw=S.LW_LINE); ax.scatter(v, i + dy, s=26, facecolor=col if fill else S.BACKGROUNDS[bg], edgecolor=col, linewidth=1.0, zorder=3)
            ax.text(v + 9, i + dy, str(v), va='center', fontsize=S.TICK - 1.5, color=S.fg(bg))
    ax.set_yticks(range(len(els))); ax.set_yticklabels([e + (' *' if e in ('Cd', 'Se') else '') for e in els]); ax.set_xlim(0, 450); ax.set_ylim(-0.6, len(els) - 0.4)
    ax.set_xlabel('Species (n)'); ax.grid(axis='x', color=S.grid_color(bg), lw=S.LW_GRID); ax.set_axisbelow(True)
    S.small(fig, 'filled = best tier T1, open = best tier T2;  * label-only (Block B)', x=0.5)
    S.title(fig, 'Species per element and tier'); n = FD.n_of(C, 'ALL_ELEMENTS', 'T1') + FD.n_of(C, 'ALL_ELEMENTS', 'T2')
    return fig, n
