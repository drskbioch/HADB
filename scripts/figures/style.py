"""ALL look-and-feel of the figures lives here: fonts, sizes, palette (from theme.json), backgrounds, line widths, spines, grids.
Edit this file and re-render (see docs/EDIT_FIGURES.md). Sizes are in points at FINAL PRINT SIZE (multipanel 7.2 in wide)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]
THEME = json.loads((ROOT / 'theme.json').read_text(encoding='utf-8'))
DPI = 1200
TICK, LABEL, TITLE, LETTER = 8, 9, 10, 16          # points
LW_AXIS, LW_LINE, LW_GRID, LW_BAR = 0.6, 1.0, 0.4, 0.4
FAMILY = 'Arial' if any('Arial' in f.name for f in font_manager.fontManager.ttflist) else 'DejaVu Sans'
BACKGROUNDS = {'white': '#FFFFFF', 'sky': THEME['sky_tint'], 'navy': THEME['navy']}
DEFAULT_BG = {2: 'white', 3: 'white', 4: 'white', 5: 'white'}      # change per figure here
MAIN, ACCENT, NAVY = THEME['main'], THEME['accent'], THEME['navy']
ELEM = dict(THEME['elements'])                                     # Ni, Mn, Zn, Co, other: one fixed colour per element in every figure
TIER = dict(THEME['tiers'])                                        # T1 = main colour, T2 = red
SRC = {'block_b_label': '#5C6B7A', 'gei_xrf_taxon': MAIN, 'gei_literature_update': '#D9A441', 'paper_table': ACCENT}
SEQ = ['#F4F1E8', '#C9DCE6', '#7FB5CF', '#2F7FA8', '#0B2545']      # sequential ramp for heatmaps / density
MISSING, GREY = '#B8B8B8', '#8C8C8C'


def elem_color(e):
    return ELEM.get(e, ELEM['other'])


def fg(bg):
    return '#FFFFFF' if bg == 'navy' else THEME['text']


def muted(bg):
    return '#C8D3E0' if bg == 'navy' else '#555555'


def grid_color(bg):
    return '#2E4A73' if bg == 'navy' else '#DDDDDD'


def rc():
    plt.rcParams.update({'font.family': FAMILY, 'font.size': TICK, 'axes.linewidth': LW_AXIS, 'xtick.major.width': LW_AXIS, 'ytick.major.width': LW_AXIS, 'xtick.major.size': 2.5, 'ytick.major.size': 2.5,
                         'xtick.labelsize': TICK, 'ytick.labelsize': TICK, 'axes.labelsize': LABEL, 'axes.titlesize': TITLE, 'legend.fontsize': TICK - 1, 'legend.frameon': False,
                         'savefig.dpi': DPI, 'figure.dpi': 100, 'pdf.fonttype': 42, 'svg.fonttype': 'none', 'axes.unicode_minus': False, 'lines.solid_capstyle': 'round'})


def new_fig(w, h, bg='white'):
    rc(); fig = plt.figure(figsize=(w, h), facecolor=BACKGROUNDS[bg]); fig._bg = bg; fig._w, fig._h = w, h
    return fig


def axes_in(fig, left=0.5, bottom=0.45, right=0.12, top=0.42, **kw):
    """axes with margins given in inches (left, bottom, right, top)"""
    w, h = fig._w, fig._h
    ax = fig.add_axes([left / w, bottom / h, (w - left - right) / w, (h - bottom - top) / h], **kw)
    style_ax(ax, fig._bg); return ax


def style_ax(ax, bg='white', grid=None):
    ax.set_facecolor('none'); c = fg(bg)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'): ax.spines[s].set_color(c); ax.spines[s].set_linewidth(LW_AXIS)
    ax.tick_params(colors=c, labelcolor=c); ax.xaxis.label.set_color(c); ax.yaxis.label.set_color(c)
    if grid in ('x', 'y', 'both'): ax.grid(True, axis=grid, color=grid_color(bg), linewidth=LW_GRID); ax.set_axisbelow(True)


def _width(fig, t):
    fig.canvas.draw(); return t.get_window_extent(fig.canvas.get_renderer()).width / fig.dpi


def title(fig, text):
    """panel title at the top, right of the corner reserved for the panel letter (added at assembly); shrinks, then wraps, to fit the panel width"""
    avail = fig._w - 0.34 - 0.06; size = TITLE
    t = fig.text(0.34 / fig._w, 1 - 0.17 / fig._h, text, ha='left', va='center', fontsize=size, fontweight='bold', color=fg(fig._bg))
    while _width(fig, t) > avail and size > 8.5: size -= 0.5; t.set_fontsize(size)
    if _width(fig, t) > avail:
        w = text.split(); k = max(1, len(w) // 2); t.set_text(' '.join(w[:k]) + '\n' + ' '.join(w[k:])); size = 8.5; t.set_fontsize(size); t.set_position((0.34 / fig._w, 1 - 0.2 / fig._h))
        while _width(fig, t) > avail and size > 6.5: size -= 0.5; t.set_fontsize(size)
    return t


def small(fig, text, x=0.1, y=0.05, size=None):
    """small grey note at the bottom of the panel; wrapped onto two lines when too wide"""
    avail = fig._w - x - 0.05; size = size or TICK - 2
    t = fig.text(x / fig._w, y / fig._h, text, ha='left', va='bottom', fontsize=size, color=muted(fig._bg))
    if _width(fig, t) > avail:
        w = text.split(); k = max(1, len(w) // 2); t.set_text(' '.join(w[:k]) + '\n' + ' '.join(w[k:]))
        while _width(fig, t) > avail and size > 5: size -= 0.5; t.set_fontsize(size)
    return t


def save(fig, path):
    fig.savefig(path, dpi=DPI, facecolor=fig.get_facecolor(), metadata={'Software': 'HADB figures'}); plt.close(fig)
