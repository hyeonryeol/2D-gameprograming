"""Generate the sample game's PNG assets with the standard library only.

No external download and no Pillow required: PNG chunks are written by hand
so the sample can run on a fresh machine right after `pip install pico2d`.

Run:  python tools/make_assets.py
"""
import math
import os
import struct
import zlib

RES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'res')


def write_png(path, width, height, rows):
    """rows: list of `height` lists, each holding `width` (r, g, b, a) tuples."""
    raw = bytearray()
    for row in rows:
        raw.append(0)  # filter type 0 (None)
        for r, g, b, a in row:
            raw += bytes((r, g, b, a))

    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data +
                struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff))

    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    print('wrote', os.path.relpath(path, os.path.dirname(RES_DIR)), '%dx%d' % (width, height))


def blank(width, height, color=(0, 0, 0, 0)):
    return [[color for _ in range(width)] for _ in range(height)]


def fill_circle(rows, cx, cy, radius, color):
    height, width = len(rows), len(rows[0])
    for y in range(max(0, cy - radius), min(height, cy + radius + 1)):
        for x in range(max(0, cx - radius), min(width, cx + radius + 1)):
            if (x - cx) ** 2 + (y - cy) ** 2 <= radius * radius:
                rows[y][x] = color


def fill_rect(rows, x0, y0, x1, y1, color):
    height, width = len(rows), len(rows[0])
    for y in range(max(0, y0), min(height, y1 + 1)):
        for x in range(max(0, x0), min(width, x1 + 1)):
            rows[y][x] = color


def make_background(path, width=800, height=600):
    """Sky gradient with a few hills and a ground strip."""
    rows = blank(width, height)
    for y in range(height):
        t = y / (height - 1)                      # 0 = top row, 1 = bottom row
        r = int(28 + (150 - 28) * t)
        g = int(42 + (200 - 42) * t)
        b = int(85 + (235 - 85) * t)
        rows[y] = [(r, g, b, 255) for _ in range(width)]

    ground_top = int(height * 0.78)               # in PNG rows (y grows downward)
    for y in range(ground_top, height):
        t = (y - ground_top) / max(1, height - ground_top)
        color = (int(70 - 25 * t), int(120 - 40 * t), int(60 - 20 * t), 255)
        rows[y] = [color for _ in range(width)]

    for cx, radius, shade in ((180, 120, 8), (420, 90, 0), (650, 140, 14)):
        for x in range(max(0, cx - radius), min(width, cx + radius)):
            dy = int(math.sqrt(max(0, radius ** 2 - (x - cx) ** 2)))
            for y in range(ground_top - dy, ground_top):
                if 0 <= y < height:
                    rows[y][x] = (52 + shade, 96 + shade, 62 + shade, 255)

    write_png(path, width, height, rows)


def make_character_sheet(path, frame_w=64, frame_h=64, frames=4):
    """A 4-frame walk cycle laid out left to right in one sheet."""
    rows = blank(frame_w * frames, frame_h)
    body = (245, 196, 92, 255)
    outline = (60, 44, 20, 255)
    cloth = (72, 132, 214, 255)
    eye = (30, 30, 40, 255)

    for i in range(frames):
        ox = i * frame_w
        swing = (-8, 0, 8, 0)[i]                  # leg swing per frame
        bob = (0, -2, 0, -2)[i]                   # small vertical bounce

        cx, cy = ox + frame_w // 2, frame_h // 2 + bob
        fill_rect(rows, cx - 12, cy - 6, cx + 11, cy + 16, cloth)     # torso
        fill_rect(rows, cx - 13, cy - 7, cx + 12, cy - 6, outline)
        fill_circle(rows, cx, cy - 18, 13, body)                      # head
        fill_circle(rows, cx, cy - 18, 13, body)
        for x in range(cx - 13, cx + 14):                             # head outline
            for y in range(cy - 31, cy - 4):
                if 12 * 12 < (x - cx) ** 2 + (y - (cy - 18)) ** 2 <= 13 * 13:
                    if 0 <= y < frame_h and 0 <= x < frame_w * frames:
                        rows[y][x] = outline
        fill_rect(rows, cx - 6, cy - 22, cx - 3, cy - 19, eye)        # eyes
        fill_rect(rows, cx + 3, cy - 22, cx + 6, cy - 19, eye)
        fill_rect(rows, cx - 5 + swing, cy + 16, cx - 1 + swing, cy + 28, outline)  # legs
        fill_rect(rows, cx + 1 - swing, cy + 16, cx + 5 - swing, cy + 28, outline)
        fill_rect(rows, cx - 17, cy - 4, cx - 13, cy + 10, body)      # arms
        fill_rect(rows, cx + 12, cy - 4, cx + 16, cy + 10, body)

    write_png(path, frame_w * frames, frame_h, rows)


def main():
    os.makedirs(RES_DIR, exist_ok=True)
    make_background(os.path.join(RES_DIR, 'background.png'))
    make_character_sheet(os.path.join(RES_DIR, 'character.png'))


if __name__ == '__main__':
    main()
