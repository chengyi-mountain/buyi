# -*- coding: utf-8 -*-
"""把 assets/renjiandao 的整页图解缩到指定宽度（默认 800px），原图另存备份。

用法：
    python tools/shrink_images.py            # 800px
    python tools/shrink_images.py 900        # 自定义宽度

说明：页面里图最宽只显示 420px，800px 足够 2 倍屏，体积约为原图三分之一。
原图会先复制到仓库相邻的 `buyi-原图备份/renjiandao/`，不进入版本库。
"""
import os
import shutil
import sys

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "assets", "renjiandao")
BAK = os.path.join(os.path.dirname(REPO), "buyi-原图备份", "renjiandao")


def main():
    width = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    files = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".jpg"))
    if not files:
        print("no jpg found in", SRC)
        return 1

    if not os.path.isdir(BAK):
        os.makedirs(BAK, exist_ok=True)
    for f in files:
        dst = os.path.join(BAK, f)
        if not os.path.exists(dst):
            shutil.copy2(os.path.join(SRC, f), dst)
    print("backup ->", BAK, len(files), "files")

    before = after = 0
    for f in files:
        p = os.path.join(SRC, f)
        size0 = os.path.getsize(p)
        before += size0
        im = Image.open(p).convert("RGB")
        if im.width > width:
            h = round(im.height * width / im.width)
            im = im.resize((width, h), Image.LANCZOS)
        im.save(p, "JPEG", quality=86, optimize=True, progressive=True)
        after += os.path.getsize(p)

    print("resized to width <= %d" % width)
    print("total %.1f MB -> %.1f MB" % (before / 1048576, after / 1048576))
    return 0


if __name__ == "__main__":
    sys.exit(main())
