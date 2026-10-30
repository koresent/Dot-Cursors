import os
import shutil
from PIL import Image

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = [
    (
        os.path.join(ROOT_DIR, "src", "Black", "01_normal_select.png"),
        os.path.join(ROOT_DIR, "src", "Black", "frames"),
    ),
    (
        os.path.join(ROOT_DIR, "src", "White", "01_normal_select.png"),
        os.path.join(ROOT_DIR, "src", "White", "frames"),
    ),
]


def generate_frames(input_path, output_dir, frame_count=32, sat=120):
    if not os.path.exists(input_path):
        return
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    try:
        img = Image.open(input_path).convert("RGBA")
    except Exception:
        return

    alpha = img.getchannel("A")
    v = Image.new("L", img.size, 255)
    s = Image.new("L", img.size, sat)

    for i in range(frame_count):
        h = Image.new("L", img.size, int((i / frame_count) * 255))
        hsv_rgb = Image.merge("HSV", (h, s, v)).convert("RGB")
        frame = Image.merge("RGBA", (*hsv_rgb.split(), alpha))
        frame.save(os.path.join(output_dir, f"frame_{i:03d}.png"), "PNG")


def main():
    for in_path, out_dir in CONFIG:
        generate_frames(in_path, out_dir)


if __name__ == "__main__":
    main()
