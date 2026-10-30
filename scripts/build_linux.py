import os
import struct
from PIL import Image

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES = ["Black", "White"]

STATIC_CURSORS = {
    "01_normal_select.png": ("left_ptr", (16, 16)),
    "02_help_select.png": ("help", (16, 16)),
    "05_precision_select.png": ("crosshair", (16, 16)),
    "06_text_select.png": ("text", (16, 16)),
    "07_handwriting.png": ("pencil", (16, 16)),
    "08_unavailable.png": ("not-allowed", (16, 16)),
    "09_vertical_resize.png": ("ns-resize", (16, 16)),
    "10_horizontal_resize.png": ("ew-resize", (16, 16)),
    "11_diagonal_resize_1.png": ("nwse-resize", (16, 16)),
    "12_diagonal_resize_2.png": ("nesw-resize", (16, 16)),
    "13_move.png": ("move", (16, 16)),
    "14_alternate_select.png": ("up-arrow", (16, 16)),
    "15_link_select.png": ("pointer", (16, 16)),
    "16_location_select.png": ("pin", (16, 16)),
    "17_person_select.png": ("person", (16, 16)),
}

CURSOR_ALIASES = {
    "left_ptr": [
        "default",
        "arrow",
        "top_left_arrow",
        "left-arrow",
        "x-cursor",
        "right_ptr",
        "context-menu",
    ],
    "help": [
        "question_arrow",
        "whats_this",
        "help-arrow",
        "d963423704225097b2126e17002e7044",
        "5c6cd98b3f31e6a4b777d9995576a00e",
    ],
    "left_ptr_watch": [
        "progress",
        "half-busy",
        "00000000000000020006000e7e80c100",
        "08e8e1c95fe2fc01f976f1e063a24ccd",
        "3ecb610c1bf2410f44200f48c40d3599",
    ],
    "wait": [
        "watch",
    ],
    "crosshair": [
        "cross",
        "cross_reverse",
        "tcross",
        "cell",
        "diamond_cross",
    ],
    "text": [
        "xterm",
        "ibeam",
        "vertical-text",
    ],
    "pencil": [
        "draft",
        "draft_large",
        "draft_small",
    ],
    "not-allowed": [
        "forbidden",
        "crossed_circle",
        "circle",
        "no-drop",
        "03b6e0fcb3499374a867c041f528e629",
    ],
    "ns-resize": [
        "n-resize",
        "s-resize",
        "v_double_arrow",
        "row-resize",
        "size_ver",
        "size-ver",
        "top_side",
        "bottom_side",
        "split_v",
        "double_arrow",
        "00008160000006810000408080010102",
        "2870a09082c103050810ffdffffe0204",
    ],
    "ew-resize": [
        "e-resize",
        "w-resize",
        "h_double_arrow",
        "col-resize",
        "size_hor",
        "size-hor",
        "left_side",
        "right_side",
        "split_h",
        "028006030e0e7ebffc7f7070c0600140",
        "14fef782d02440884392942c11205230",
    ],
    "nwse-resize": [
        "nw-resize",
        "se-resize",
        "size_fdiag",
        "size-fdiag",
        "bd_double_arrow",
        "top_left_corner",
        "bottom_right_corner",
        "c7088f0f3e6c8088236ef8e1e3e70000",
        "38c5dff724d0077045e70801043142bf",
    ],
    "nesw-resize": [
        "ne-resize",
        "sw-resize",
        "size_bdiag",
        "size-bdiag",
        "fd_double_arrow",
        "top_right_corner",
        "bottom_left_corner",
        "fcf1c3c7cd4491d801f1e1c78f100000",
        "50585d75b494802d0151028115016902",
    ],
    "move": [
        "fleur",
        "all-scroll",
        "size_all",
        "size-all",
        "grab",
        "grabbing",
        "openhand",
        "closedhand",
        "4498f0e0c1937ffe01fd06f973665830",
        "9081237383d90e509aa00f00170e968f",
    ],
    "up-arrow": [
        "center_ptr",
    ],
    "pointer": [
        "pointing_hand",
        "hand",
        "hand1",
        "hand2",
        "link",
        "alias",
        "9d800770f22c15243dd15260e5b700f7",
        "e29285e634086352946a0e7090d73106",
    ],
    "pin": [
        "location",
        "waypoint",
    ],
    "person": [
        "contact",
        "user",
    ],
}


def pack_xcursor(images, hotspot=(16, 16), delay=50):
    ntoc = len(images)
    toc_entries = []
    chunks = []
    current_offset = 16 + ntoc * 12

    for img in images:
        w, h = img.size
        img_rgba = img.convert("RGBA")
        raw_pixels = bytearray(w * h * 4)
        idx = 0
        for y in range(h):
            for x in range(w):
                r, g, b, a = img_rgba.getpixel((x, y))
                if a == 0:
                    raw_pixels[idx : idx + 4] = b"\x00\x00\x00\x00"
                else:
                    b_p = (b * a + 127) // 255
                    g_p = (g * a + 127) // 255
                    r_p = (r * a + 127) // 255
                    raw_pixels[idx : idx + 4] = bytes([b_p, g_p, r_p, a])
                idx += 4

        chunk_header = struct.pack(
            "<9I",
            36,
            0xFFFD0002,
            w,
            1,
            w,
            h,
            hotspot[0],
            hotspot[1],
            delay,
        )
        chunk_data = chunk_header + bytes(raw_pixels)
        toc_entries.append(struct.pack("<3I", 0xFFFD0002, w, current_offset))
        chunks.append(chunk_data)
        current_offset += len(chunk_data)

    file_header = struct.pack("<4I", 0x58637572, 16, 0x00010000, ntoc)
    return file_header + b"".join(toc_entries) + b"".join(chunks)


def build_theme(theme_name):
    out_theme_dir = os.path.join(ROOT_DIR, "Linux", f"Dot-{theme_name}")
    cursors_dir = os.path.join(out_theme_dir, "cursors")
    src_dir = os.path.join(ROOT_DIR, "src", theme_name)
    frames_dir = os.path.join(src_dir, "frames")

    os.makedirs(cursors_dir, exist_ok=True)

    print(f"Building Linux theme Dot-{theme_name}...")

    # Build static cursors
    for src_file, (canon_name, hotspot) in STATIC_CURSORS.items():
        src_path = os.path.join(src_dir, src_file)
        if not os.path.exists(src_path):
            print(f"  [WARN] Source file missing: {src_path}")
            continue
        with Image.open(src_path) as im:
            data = pack_xcursor([im], hotspot=hotspot, delay=50)
        canon_path = os.path.join(cursors_dir, canon_name)
        with open(canon_path, "wb") as f:
            f.write(data)

    # Build animated cursors (left_ptr_watch and wait)
    frame_files = [
        os.path.join(frames_dir, f"frame_{i:03d}.png") for i in range(32)
    ]
    frame_imgs = []
    for fpath in frame_files:
        if os.path.exists(fpath):
            frame_imgs.append(Image.open(fpath))

    if len(frame_imgs) == 32:
        ani_data = pack_xcursor(frame_imgs, hotspot=(16, 16), delay=100)
        for canon_name in ["left_ptr_watch", "wait"]:
            canon_path = os.path.join(cursors_dir, canon_name)
            with open(canon_path, "wb") as f:
                f.write(ani_data)
        for im in frame_imgs:
            im.close()
    else:
        print(
            f"  [WARN] Frames incomplete for {theme_name} (found {len(frame_imgs)}/32)"
        )

    # Create aliases for all cursors
    for canon_name, aliases in CURSOR_ALIASES.items():
        canon_path = os.path.join(cursors_dir, canon_name)
        if not os.path.exists(canon_path):
            continue
        with open(canon_path, "rb") as f:
            canon_bytes = f.read()
        for alias in aliases:
            alias_path = os.path.join(cursors_dir, alias)
            with open(alias_path, "wb") as f:
                f.write(canon_bytes)

    # Generate index.theme and cursor.theme
    index_theme = f"""[Icon Theme]
Name=Dot-{theme_name}
Comment=Minimalist dot cursor theme for Linux ({theme_name})
Inherits=core
"""
    with open(
        os.path.join(out_theme_dir, "index.theme"), "w", encoding="utf-8", newline="\n"
    ) as f:
        f.write(index_theme)

    cursor_theme = f"""[Icon Theme]
Inherits=Dot-{theme_name}
"""
    with open(
        os.path.join(out_theme_dir, "cursor.theme"), "w", encoding="utf-8", newline="\n"
    ) as f:
        f.write(cursor_theme)

    print(
        f"  Successfully created Dot-{theme_name} with {len(os.listdir(cursors_dir))} cursor files!"
    )


def main():
    for theme in THEMES:
        build_theme(theme)


if __name__ == "__main__":
    main()
