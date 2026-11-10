# -*- coding: utf-8 -*-
"""检查配图 PDF 的结构：页数、画幅、每页图片对象。"""
import sys
import pymupdf

def main(path):
    doc = pymupdf.open(path)
    print("pages:", doc.page_count)
    for i in range(min(3, doc.page_count)):
        pg = doc[i]
        imgs = pg.get_images(full=True)
        text = pg.get_text().strip()
        print("page", i + 1, "rect", round(pg.rect.width), "x", round(pg.rect.height),
              "imgs", len(imgs), "text_len", len(text))
        for im in imgs[:3]:
            print("    xref", im[0], "px", im[2], "x", im[3])
        if text:
            print("    text head:", text[:60].replace("\n", " "))
    last = doc[-1]
    print("last page: imgs", len(last.get_images(full=True)),
          "text", last.get_text().strip()[:60].replace("\n", " "))
    doc.close()

if __name__ == "__main__":
    main(sys.argv[1])
