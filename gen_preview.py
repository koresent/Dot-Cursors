import os, math
from PIL import Image, ImageDraw

CFG = {
    "Black": {"src": "Black/src", "fw": "Black/src/frames", "fb": "Black/src/frames", "out": ".github/showcase/black.png", "bg": (255, 255, 255, 255)},
    "White": {"src": "White/src", "fw": "White/src/frames", "fb": "White/src/frames", "out": ".github/showcase/white.png", "bg": (29, 32, 33, 255)}
}
ANIM = {"03_working_in_background": "frame_028.png", "04_busy": "frame_023.png"}
COLS, PAD, RAD, SS = 6, 40, 24, 4

def run(c):
    src, out = c["src"], c["out"]
    if not os.path.isdir(src): return
    fs = [f for f in os.listdir(src) if f.lower().endswith('.png') and os.path.isfile(os.path.join(src, f))]
    for k in ANIM:
        if not any(f.startswith(k) for f in fs): fs.append(k)
    fs.sort()
    if not fs: return
    imgs, mw, mh = [], 0, 0
    for b in fs:
        p = os.path.join(src, b) if b.lower().endswith('.png') else (os.path.join(c["fb"] if b == "04_busy" else c["fw"], ANIM[b]) if b in ANIM else None)
        if p and os.path.exists(p):
            i = Image.open(p).convert("RGBA")
            mw, mh = max(mw, i.width), max(mh, i.height)
            imgs.append(i)
    if not imgs: return
    cw, ch = mw + PAD * 2, mh + PAD * 2
    W, H = COLS * cw, math.ceil(len(imgs) / COLS) * ch
    bg = Image.new('RGBA', (W, H), c["bg"])
    for i, im in enumerate(imgs): bg.alpha_composite(im, ((i % COLS * cw + (cw // 2)) - (im.width // 2), (i // COLS * ch + (ch // 2)) - (im.height // 2)))
    m = Image.new('L', (W * SS, H * SS), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, W * SS, H * SS), RAD * SS, fill=255)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    Image.composite(bg, Image.new('RGBA', (W, H), (0,0,0,0)), m.resize((W, H), getattr(Image, 'Resampling', Image).LANCZOS)).save(out)

if __name__ == '__main__': [run(CFG[t]) for t in CFG]