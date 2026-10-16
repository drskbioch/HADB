"""Phase 0 step 5: theme.json (k-means dominant colours of usable images; main colour; sky-blue accent; colour-blind-safe element colours) and web-optimised images."""
import colorsys, json, io
from pathlib import Path
import numpy as np, pandas as pd
from PIL import Image
from sklearn.cluster import KMeans
Image.MAX_IMAGE_PIXELS = None
P = Path(__file__).resolve().parents[1]
inv = pd.read_csv(P/'docs'/'image_inventory_hadb.csv')
BS = chr(92)
inv['name'] = inv.path.str.split(BS, regex=False).str[-2:].str.join('/')
inv['usable'] = np.where(inv.width < 400, 'N', 'Y')
inv['reason'] = np.where(inv.width < 400, 'low resolution (276 px)', 'HADB banner/header image (project-owned); not viewed (read blocked outside the working directory); possible people/copyright NOT verified')
inv.to_csv(P/'docs'/'image_usability.csv', index=False)
def lum(rgb):
    c = [(v/255)/12.92 if v/255 <= .03928 else (((v/255)+.055)/1.055)**2.4 for v in rgb]; return .2126*c[0]+.7152*c[1]+.0722*c[2]
def contrast(a, b): la, lb = lum(a), lum(b); return (max(la, lb)+.05)/(min(la, lb)+.05)
px = []
for r in inv[inv.usable == 'Y'].itertuples():
    im = Image.open(r.path).convert('RGB'); im.thumbnail((200, 200)); px.append(np.asarray(im).reshape(-1, 3))
px = np.vstack(px) if px else None
FALL = dict(main='#0B6E4F', accent='#5BC0EB')
theme = dict(source='k-means (k=8) on %d usable HADB images' % int((inv.usable == 'Y').sum()), dominant=[], main=None, accent=None, fallback_used=False)
cand = []
if px is not None:
    km = KMeans(8, n_init=5, random_state=1).fit(px[::7]); cnt = np.bincount(km.labels_, minlength=8)
    for c, n in sorted(zip(km.cluster_centers_, cnt), key=lambda t: -t[1]):
        rgb = tuple(int(round(v)) for v in c); h, l, s = colorsys.rgb_to_hls(*[v/255 for v in rgb]); theme['dominant'].append(dict(hex='#%02X%02X%02X' % rgb, share=round(float(n/cnt.sum()), 3), saturation_hsl=round(s, 3), contrast_white=round(contrast(rgb, (255, 255, 255)), 2)))
        if contrast(rgb, (255, 255, 255)) >= 4.5 and s > .25: cand.append((s, rgb))
if cand: theme['main'] = '#%02X%02X%02X' % max(cand)[1]
else: theme['main'] = FALL['main']; theme['fallback_used'] = True
# accent: sky blue, hue 195-205 deg, lightness 60-75%
h, l, s = 200/360, .66, .78; r, g, b = colorsys.hls_to_rgb(h, l, s); theme['accent'] = '#%02X%02X%02X' % (round(r*255), round(g*255), round(b*255))
theme['accent_hsl'] = dict(hue=200, lightness=66, saturation=78); theme['accent_note'] = 'sky blue; decorative only (contrast with white < 3:1); text uses main or navy'
theme['navy'] = '#0B2545'; theme['sky_tint'] = '#EAF6FC'
theme['elements'] = dict(Ni='#0077BB', Mn='#EE7733', Zn='#009988', Co='#EE3377', other='#BBBBBB')
theme['tiers'] = dict(T1=theme['main'], T2='#CC3311'); theme['palette_note'] = 'Paul Tol vibrant (colour-blind safe); one fixed colour per element across all figures and the web'
theme['text'] = '#1A1A1A'
(P/'frontend'/'theme.json').write_text(json.dumps(theme, indent=1), encoding='utf-8')
(P/'theme.json').write_text(json.dumps(theme, indent=1), encoding='utf-8')
print('main', theme['main'], '| fallback used:', theme['fallback_used'], '| dominant', [d['hex'] for d in theme['dominant']][:5], '| accent', theme['accent'])
# web-optimised copies: <=1920 px, <300 KB, no EXIF
alts = {'HADB.png': 'HADB banner: Hyperaccumulator Database title graphic', 'HABD-1.png': 'HADB banner variant', 'Picture1.png': 'HADB illustration'}
out = []
for r in inv[(inv.usable == 'Y') & (inv.width >= 900)].itertuples():
    im = Image.open(r.path).convert('RGB'); im.thumbnail((1920, 1920)); name = Path(r.path).parent.name + '-' + Path(r.path).stem.replace(' ', '-').lower() + '.webp'
    for q in (90, 80, 70, 60, 50, 40):
        buf = io.BytesIO(); im.save(buf, 'WEBP', quality=q); 
        if buf.tell() < 300_000: break
    if buf.tell() >= 300_000:
        im2 = im.copy(); im2.thumbnail((1400, 1400)); buf = io.BytesIO(); im2.save(buf, 'WEBP', quality=60)
    (P/'frontend'/'public'/'images'/name).write_bytes(buf.getvalue()); out.append(dict(file=name, bytes=buf.tell(), source_sha256=r.sha256, alt='Draft: ' + alts.get(Path(r.path).name, 'HADB banner image') + ' (check and edit)'))
(P/'frontend'/'public'/'images'/'images.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
print('web images:', [(o['file'], o['bytes']) for o in out])
