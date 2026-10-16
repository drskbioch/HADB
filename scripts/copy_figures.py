"""Make 1600 px wide PNG web copies of the multipanel figures in frontend/public/figures (the originals are not touched)."""
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
R = Path(__file__).resolve().parents[1]; out = R / 'frontend/public/figures'; out.mkdir(parents=True, exist_ok=True)
for n in (2, 3, 4, 5):
    src = R / f'manuscript/figures/multipanel/figure{n}.png'
    if not src.exists(): print('missing', src.name); continue
    with Image.open(src) as im:
        h = round(im.height * 1600 / im.width); im.convert('RGB').resize((1600, h), Image.LANCZOS).save(out / f'figure{n}.png', optimize=True); print(f'figure{n}.png 1600 x {h}')
