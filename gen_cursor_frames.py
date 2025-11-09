import os, shutil
from PIL import Image

C = [("Black/src/01_normal_select.png", "Black/src/frames"), ("White/src/01_normal_select.png", "White/src/frames")]

def g(i_p, o_d, fc=32, sat=120):
    if not os.path.exists(i_p): return
    if os.path.exists(o_d): shutil.rmtree(o_d)
    os.makedirs(o_d)
    try: img = Image.open(i_p).convert('RGBA')
    except: return
    a = img.getchannel('A')
    v = Image.new('L', img.size, 255)
    s = Image.new('L', img.size, sat)
    for i in range(fc):
        Image.merge('RGBA', (*Image.merge('HSV', (Image.new('L', img.size, int((i/fc)*255)), s, v)).convert('RGB').split(), a)).save(os.path.join(o_d, f"frame_{i:03d}.png"), "PNG")

if __name__ == '__main__': [g(i, o) for i, o in C]