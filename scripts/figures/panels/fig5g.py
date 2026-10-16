"""Fig 5g: PCA of species medians (bio1, bio12, pH), biplot."""
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from figures import style as S, figdata as FD, layout as L
FIG, LET = 5, 'g'
META = dict(chart='PCA biplot', data=['derived/species_environment_summary.csv'], filter='species with >= 20 native cells and a pH median; standardised species medians of bio1, bio12 and pH; colour = first element present in the order Ni, Co, Mn, Zn')


def render():
    w, h = L.panel_size(FIG, LET); bg = S.DEFAULT_BG[FIG]; fig = S.new_fig(w, h, bg); ax = S.axes_in(fig, left=0.6, bottom=0.6, right=0.15, top=0.45); Sm = FD.env_ok().dropna(subset=['bio1_median_C', 'bio12_median_mm', 'ph_median'])
    X = StandardScaler().fit_transform(Sm[['bio1_median_C', 'bio12_median_mm', 'ph_median']]); pca = PCA(2).fit(X); Z = pca.transform(X); col = [S.elem_color(FD.primary_element(FD.elements_of(s))) for s in Sm.elements_in_hadb]
    ax.scatter(Z[:, 0], Z[:, 1], s=7, c=col, alpha=0.8, lw=0); sc = 2.2
    for (a, b), lab in zip(pca.components_.T, ('bio1', 'bio12', 'pH')):
        ax.annotate('', xy=(a * sc, b * sc), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=S.fg(bg), lw=1.0)); ax.text(a * sc * 1.15, b * sc * 1.15, lab, ha='center', va='center', fontsize=S.TICK - 1, color=S.fg(bg), fontweight='bold')
    ev = pca.explained_variance_ratio_ * 100; ax.set_xlabel('PC1 (%.0f%%)' % ev[0]); ax.set_ylabel('PC2 (%.0f%%)' % ev[1]); ax.axhline(0, color=S.GREY, lw=0.3); ax.axvline(0, color=S.GREY, lw=0.3)
    for j, e in enumerate(FD.CORE): fig.text((0.65 + 0.45 * j) / w, 0.14 / h, e, color=S.elem_color(e), fontsize=S.TICK - 1, fontweight='bold')
    S.title(fig, 'PCA of the species medians'); return fig, len(Sm)
