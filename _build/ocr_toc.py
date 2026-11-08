#!/usr/bin/env python3
"""OCR 书籍前若干页，用于抓目录结构。输出到 _build/ocr/<slug>_pNN.txt"""
import os, subprocess, sys, tempfile
import pymupdf

ATT = "/home/user/.doubao/agent_mode/workspace/.sessions/38451120534976514/attachments"
OUT = "/home/user/Doubao/chats/38451120534976514/常微分方程点化学习系统/_build/ocr"

BOOKS = {
    "wanggaoxiong": "常微分方程 （第四版） (王高雄,周之铭,朱思铭,王寿松) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
    "zhusiming": "常微分方程学习辅导与习题解答 (朱思铭) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
    "xitijiexi": "常微分方程（第四版）习题详解.pdf",
    "dingtongren": "常微分方程教程 第三版 (丁同仁，李承治) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
    "liubin": "常微分方程 (柳斌) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
    "pontryagin": "常微分方程 (庞特里亚金) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
    "arnold": "常微分方程 (阿诺尔德) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
}

def ocr_page(doc, pno, dpi=200):
    page = doc[pno]
    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
        pix.save(tf.name)
        p = tf.name
    try:
        r = subprocess.run(
            ["tesseract", p, "stdout", "-l", "chi_sim", "--psm", "6"],
            capture_output=True, text=True, timeout=120)
        return r.stdout
    finally:
        os.unlink(p)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:] or list(BOOKS)
    n = int(os.environ.get("N_PAGES", "24"))
    for slug in only:
        f = os.path.join(ATT, BOOKS[slug])
        doc = pymupdf.open(f)
        txt = []
        for i in range(min(n, doc.page_count)):
            txt.append(f"\n\n===== [p{i+1}] =====\n" + ocr_page(doc, i))
        with open(os.path.join(OUT, f"{slug}_toc.txt"), "w") as fh:
            fh.write("".join(txt))
        print(slug, "done", doc.page_count, "pages total")
        doc.close()
