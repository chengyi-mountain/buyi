# -*- coding: utf-8 -*-
"""把配图 PDF 按页导出为 jpg。

用法：
  python tools/split_book.py <pdf> <out_dir> [--mode full|crop] [--dpi 150] [--start 1]

mode=full 导出整页（含卦名标题与「卦圖象解」文字）；
mode=crop 只裁中间那一幅白描画（自动按墨色密度找上下边界）。
页码 n -> 文件名 001.jpg ... 按 --start 偏移对齐卦号。
"""
import argparse
import os
import pymupdf
from PIL import Image


def _profile(img, axis, band=None, thresh=110):
    """沿 axis 统计墨色占比；axis='row' 逐行，axis='col' 逐列。"""
    g = img.convert("L")
    w, h = g.size
    px = g.load()
    if axis == "row":
        rng, step, fixed = h, max(1, w // 500), w
    else:
        rng, step, fixed = w, max(1, h // 500), h
    prof = []
    for i in range(rng):
        dark = 0
        total = 0
        for j in range(0, fixed, step):
            total += 1
            key = (j, i) if axis == "row" else (i, j)
            if px[key] < thresh:
                dark += 1
        prof.append(dark / total if total else 0)
    return prof


def _longest_run(flags):
    best = (0, -1)
    start = None
    for i, f in enumerate(flags):
        if f and start is None:
            start = i
        elif not f and start is not None:
            if i - start > best[1] - best[0]:
                best = (start, i - 1)
            start = None
    if start is not None and len(flags) - start > best[1] - best[0]:
        best = (start, len(flags) - 1)
    return best


def crop_drawing(img, edge=0.02):
    """只保留中间那幅白描画：先按最长的连续墨迹行带定上下，再按列定左右。"""
    rows = _profile(img, "row")
    top, bottom = _longest_run([v > edge for v in rows])
    if bottom <= top:
        return img
    w, h = img.size
    pad_y = 6
    top = max(0, top - pad_y)
    bottom = min(h, bottom + pad_y)
    cols = _profile(img.crop((0, top, w, bottom)), "col")
    left, right = _longest_run([v > edge for v in cols])
    if right <= left:
        left, right = 0, w
    pad_x = 6
    left = max(0, left - pad_x)
    right = min(w, right + pad_x)
    return img.crop((left, top, right, bottom))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("out")
    ap.add_argument("--mode", default="full", choices=["full", "crop"])
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--start", type=int, default=1, help="第 1 页对应第几卦")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    doc = pymupdf.open(args.pdf)
    count = doc.page_count
    for i in range(count):
        num = args.start + i
        pix = doc[i].get_pixmap(dpi=args.dpi)
        tmp = os.path.join(args.out, "_tmp_page.png")
        pix.save(tmp)
        img = Image.open(tmp).convert("RGB")
        if args.mode == "crop":
            img = crop_drawing(img)
        out = os.path.join(args.out, "%03d.jpg" % num)
        img.save(out, "JPEG", quality=88, optimize=True)
        os.remove(tmp)
    doc.close()
    print("done:", args.start, "->", args.start + count - 1, "files in", args.out)


if __name__ == "__main__":
    main()
