"""Multipanel layout: width 7.2 in, max height 9.5 in. LAYOUT[fig] = (n_cols, row_heights_in_inches, {letter: (row, col, row_span, col_span)}).
Edit grid and spans here; panels re-render at the new size automatically (the cache key includes this file). Letters (16 pt bold) are added at assembly."""
WIDTH, MAX_HEIGHT = 7.2, 9.5
LAYOUT = {
    2: (3, [3.1, 3.1, 3.1], {'a': (0, 0, 1, 1), 'b': (0, 1, 1, 1), 'c': (0, 2, 1, 1), 'd': (1, 0, 1, 1), 'e': (1, 1, 1, 1), 'f': (1, 2, 1, 1), 'g': (2, 0, 1, 1), 'h': (2, 1, 1, 1), 'i': (2, 2, 1, 1)}),
    3: (3, [3.1, 3.1, 3.1], {'a': (0, 0, 1, 1), 'b': (0, 1, 1, 1), 'c': (0, 2, 1, 1), 'd': (1, 0, 1, 2), 'e': (1, 2, 1, 1), 'f': (2, 0, 1, 1), 'g': (2, 1, 1, 1), 'h': (2, 2, 1, 1)}),
    4: (3, [2.35, 2.35, 2.35, 2.35], {'a': (0, 0, 1, 2), 'b': (0, 2, 1, 1), 'c': (1, 0, 1, 1), 'd': (1, 1, 1, 1), 'e': (1, 2, 1, 1), 'f': (2, 0, 1, 1), 'g': (2, 1, 1, 1), 'h': (2, 2, 1, 1), 'i': (3, 0, 1, 3)}),
    5: (3, [2.35, 2.35, 2.35, 2.35], {'a': (0, 0, 1, 1), 'b': (0, 1, 1, 1), 'c': (0, 2, 1, 1), 'd': (1, 0, 1, 1), 'e': (1, 1, 1, 1), 'f': (1, 2, 1, 1), 'g': (2, 0, 1, 1), 'h': (2, 1, 1, 1), 'i': (2, 2, 2, 1), 'j': (3, 0, 1, 2)}),
}
PANELS = {2: 'abcdefghi', 3: 'abcdefgh', 4: 'abcdefghi', 5: 'abcdefghij'}


def col_w(fig): return WIDTH / LAYOUT[fig][0]


def panel_size(fig, letter):
    n, rows, P = LAYOUT[fig]; r, c, rs, cs = P[letter]
    return cs * WIDTH / n, sum(rows[r:r + rs])


def panel_xy(fig, letter):
    n, rows, P = LAYOUT[fig]; r, c, rs, cs = P[letter]
    return c * WIDTH / n, sum(rows[:r])


def multipanel_size(fig):
    return WIDTH, sum(LAYOUT[fig][1])
