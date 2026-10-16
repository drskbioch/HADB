"""Fig 5i: climate space of the four data-rich T1 species (small multiples)."""
import numpy as np
from figures import style as S, figdata as FD, layout as L
FIG, LET = 5, 'i'
META = dict(chart='small multiples (2D histogram)', data=['release/evidence.csv', 'release/species_element.csv', 'derived/species_environment_summary.csv', 'work/records_environment_primary.csv.gz'],
            filter='rule: the 4 species with most native cells among species with tier T1 evidence from a hyperaccumulation-scope source (headline view) and >= 20 native cells; 2D histogram of bio1 vs bio12 of the native cells (no points)')


def pick():
    E = FD.evidence(); t1 = set(E[(E.tier == 'T1') & (E.scope == 'hyperaccumulation')].sp); Sm = FD.env_ok(); Sm = Sm[Sm.accepted_name.isin(t1)].sort_values('n_cells', ascending=False).head(4); return list(Sm.accepted_name), list(Sm.n_cells)


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); sp, ncl = pick(); C = FD.cells_ok(); from matplotlib.colors import LinearSegmentedColormap; cm = LinearSegmentedColormap.from_list('hadb', S.SEQ)
    for k, (s, nn) in enumerate(zip(sp, ncl)):
        ax = fig.add_axes([0.55 / w, (h - 0.5 - 0.68 - k * 0.91) / h, (w - 0.75) / w, 0.68 / h]); S.style_ax(ax, bg); d = C[C.species_level_name == s]
        ax.hist2d(d.bio1_c, d.bio12_mm.clip(upper=6553.5), bins=(28, 28), cmap=cm, cmin=1); ax.text(0.97, 0.9, '%s\nn=%s cells' % (s, format(nn, ',')), transform=ax.transAxes, ha='right', va='top', fontsize=S.TICK - 2.5, color=S.fg(bg), style='italic')
        ax.tick_params(labelsize=S.TICK - 2.5)
        if k == len(sp) - 1: ax.set_xlabel('bio1 (degrees C)', fontsize=S.TICK - 1.5)
        if k == 1: ax.set_ylabel('bio12 (mm)', fontsize=S.TICK - 1.5)
    S.title(fig, 'Data-rich T1 species'); return fig, int(sum(ncl))
