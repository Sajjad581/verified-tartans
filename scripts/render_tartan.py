"""
render_tartan.py — render a Scottish tartan as a 2/2 twill woven-cloth image.

Given a threadcount (sett) and palette, produces a true-scale PNG:
528 threads = 12" x 12" at 44 threads/inch, 3 px/thread, 2/2 Z-twill
with round-yarn shading. See docs/RENDERING.md for the full method.

Usage:
    from render_tartan import palette, weave, full_sett
    from PIL import Image
    pal = palette("K#101010 OG#5C6428 B#345064")
    arr = weave("B/28 K6 B6 K6 B6 K32 OG32 K6 OG32 K32 B32 K6 B/6", "yes", pal)
    Image.fromarray(arr).save("campbell.png")

Requires: numpy, Pillow
"""
import numpy as np, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TC  = re.compile(r'^([A-Za-z]+)(/?)(\d+)$')
PAL = re.compile(r'^([A-Za-z]+)#([0-9A-Fa-f]{6})$')
SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SANS  = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def palette(p):
    return {m.group(1).upper(): tuple(int(m.group(2)[i:i+2],16) for i in (0,2,4))
            for t in str(p).split() if (m := PAL.match(t.strip()))}

def full_sett(tc, symmetric):
    toks = [(m.group(1).upper(), m.group(2)=='/', int(m.group(3)))
            for t in str(tc).split() if (m := TC.match(t.strip()))]
    if str(symmetric).strip().lower() == 'yes' and len(toks) > 2:
        toks = toks + list(reversed(toks[1:-1]))
    s = []
    for c,_,n in toks: s.extend([c]*n)
    return s

def weave(tc, sym, pal, n=528, px=3):
    seq = full_sett(tc, sym)
    seq = (seq * (int(np.ceil(n/len(seq)))+1))[:n]
    line = np.array([pal[c] for c in seq], dtype=np.float32)
    x = np.arange(n)[None,:]; y = np.arange(n)[:,None]
    wu = ((x - y) % 4) < 2                                    # 2/2 Z-twill
    warp = np.broadcast_to(line[None,:,:], (n,n,3)); weft = np.broadcast_to(line[:,None,:], (n,n,3))
    base = np.where(wu[:,:,None], warp, weft)
    up = lambda a: np.repeat(np.repeat(a, px, 0), px, 1)
    img, wup = up(base), up(wu)
    t = (np.arange(px)+0.5)/px - 0.5
    prof = 1.0 - 0.42*(2*t)**2
    sh = np.where(wup, np.tile(prof,n)[None,:], np.tile(prof,n)[:,None]) * np.where(wup, 1.05, 0.93)
    return np.clip(img*sh[:,:,None], 0, 255).astype(np.uint8)

def emboss_text(arr, text='scottishkiltshop', width_frac=0.40, bevel=0.55, face=0.20, spec=140):
    """Press the wordmark into the cloth: bevel modulates the fabric's own luminance,
       so the weave still shows through the letters."""
    H, W = arr.shape[:2]
    size = 10
    f = ImageFont.truetype(SERIF, size)
    while f.getbbox(text)[2] < W*width_frac and size < 400:
        size += 2; f = ImageFont.truetype(SERIF, size)
    tmp = Image.new('L', (W, H), 0); dr = ImageDraw.Draw(tmp)
    b = dr.textbbox((0,0), text, font=f)
    dr.text(((W-(b[2]-b[0]))//2 - b[0], (H-(b[3]-b[1]))//2 - b[1]), text, 255, font=f)
    mask = np.asarray(tmp, np.float32)/255.0
    blur = np.asarray(tmp.filter(ImageFilter.GaussianBlur(1.5)), np.float32)/255.0
    d = max(2, int(W/450))
    relief = np.roll(np.roll(blur,-d,0),-d,1) - np.roll(np.roll(blur,d,0),d,1)
    out = arr.astype(np.float32)
    out += relief[:,:,None]*spec
    out *= (1.0 + relief[:,:,None]*bevel)
    lum = out.mean(2, keepdims=True)
    out = out*(1-face*mask[:,:,None]) + np.where(lum>128, 0.0, 255.0)*(face*mask[:,:,None])
    return np.clip(out,0,255).astype(np.uint8)

def with_rulers(cloth, inches=12.0, ppi=132, gut=82, pad=30, foot=44):
    """Ruler along the top and left edges so the swatch reads at true size."""
    S = cloth.size[0]
    W = S + gut + pad
    H = S + gut + foot
    canvas = Image.new('RGB', (W, H), (247,245,241))
    canvas.paste(cloth, (gut, gut))
    d = ImageDraw.Draw(canvas)
    fnum = ImageFont.truetype(SANS, 21)
    ink, rule = (26,26,26), (120,118,112)
    d.rectangle([gut-1, gut-1, gut+S, gut+S], outline=(60,60,60), width=2)   # frame the cloth

    n = int(round(inches*4))                                            # quarter-inch resolution
    for i in range(n+1):
        p = gut + i*ppi/4.0
        if   i % 4 == 0: L, w = 26, 2
        elif i % 2 == 0: L, w = 16, 1
        else:            L, w = 9, 1
        d.line([(p, gut-L), (p, gut-1)], fill=ink if i%4==0 else rule, width=w)   # top
        d.line([(gut-L, p), (gut-1, p)], fill=ink if i%4==0 else rule, width=w)   # left
        if i % 4 == 0:
            lbl = str(i//4)
            b = d.textbbox((0,0), lbl, font=fnum)
            d.text((p-(b[2]-b[0])/2, gut-L-6-(b[3]-b[1])), lbl, ink, font=fnum)
            d.text((gut-L-8-(b[2]-b[0]), p-(b[3]-b[1])/2-2), lbl, ink, font=fnum)
    f2 = ImageFont.truetype(SANS, 19)
    d.text((6, 6), "in", ink, font=f2)
    d.text((gut, gut+S+13), f'{inches:g}" \u00d7 {inches:g}" actual size  \u00b7  528 \u00d7 528 threads  \u00b7  44 threads/inch',
           (90,88,84), font=f2)
    return canvas

