#!/usr/bin/env python3
"""从 _build/books/<mod>.py 生成 quiz.md / flashcards.md / manifest.json"""
import importlib, json, os, sys

ROOT = "/home/user/Doubao/chats/38451120534976514/常微分方程点化学习系统"
sys.path.insert(0, os.path.join(ROOT, "_build", "books"))

def load(mod):
    return importlib.import_module(mod)

def write_quiz(b, out):
    lines = [f"# {b.TITLE} 测验", ""]
    ch_titles = {c[0]: c[1] for c in b.CHAPTERS}
    for cid in [c[0] for c in b.CHAPTERS] + ["__all"]:
        qs = [q for q in b.QUIZ if q[0] == cid]
        if not qs:
            continue
        head = "## 综合测验（跨章）" if cid == "__all" else f"## {ch_titles[cid]} 测验"
        lines.append(head); lines.append("")
        for i, (_, typ, q, opts, ans, exp) in enumerate(qs, 1):
            lines.append(f"### Q{i}. {q}")
            if typ == "single":
                labels = "ABCD"
                for j, o in enumerate(opts):
                    lines.append(f"- {labels[j]}. {o}")
                lines.append("")
                lines.append(f"**答案**：{labels[ans]}")
            else:
                lines.append("")
                lines.append(f"**答案**：{ans}")
            lines.append(f"**解析**：{exp}")
            lines.append("")
    lines.append("## 最终检验")
    lines.append("给一个洛伦茨系统，先用线性化判断三个平衡点的稳定性，再说明为什么 ρ=28 时无法长期预测；要求写出雅可比矩阵与特征值的计算过程。")
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")

def write_cards(b, out):
    lines = [f"# {b.TITLE} 抽认卡", ""]
    ch_titles = {c[0]: c[1] for c in b.CHAPTERS}
    cur = None
    for cid, front, back, tags in b.CARDS:
        if cid != cur:
            cur = cid
            lines += [f"## {ch_titles.get(cid, cid)}", ""]
        lines.append(f"### 卡片：{front}")
        lines.append(f"- **背面**：{back}")
        lines.append(f"- **标签**：{', '.join(tags)}")
        lines.append(f"- **章节**：{cid}")
        lines.append("")
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")

def write_manifest(b, bookdir, out):
    glossary = []
    gp = os.path.join(bookdir, "glossary.md")
    if os.path.exists(gp):
        for line in open(gp, encoding="utf-8"):
            if line.startswith("|") and "术语" not in line and "---" not in line:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 4:
                    glossary.append({"term": cells[0], "def": cells[1],
                                     "chapterId": cells[3].replace(" ", "") if cells[3].startswith("ch") else cells[2]})
    quizzes = []
    for i, (cid, typ, q, opts, ans, exp) in enumerate(b.QUIZ, 1):
        quizzes.append({"id": f"q{i:02d}", "chapterId": cid, "type": typ, "question": q,
                        "options": opts, "answer": ans, "explain": exp})
    cards = []
    for i, (cid, front, back, tags) in enumerate(b.CARDS, 1):
        cards.append({"id": f"f{i:02d}", "chapterId": cid, "front": front, "back": back, "tags": tags})
    manifest = {
        "slug": b.SLUG,
        "title": b.TITLE,
        "subtitle": b.SUBTITLE,
        "book": b.BOOK,
        "audience": "零基础到本科二年级，目标是吃透理论并会做题",
        "goal": "系统掌握常微分方程的解法定课与理论基础",
        "learningPath": [{"step": s, "title": t, "chapterIds": c, "checkpoint": cp} for s, t, c, cp in b.PATH],
        "chapters": [{"id": cid, "title": t, "file": f, "difficulty": d} for cid, t, f, d in b.CHAPTERS],
        "concepts": [{"id": cid, "title": t, "file": f, "chapterIds": chs} for cid, t, f, chs in b.CONCEPTS],
        "glossary": glossary,
        "patterns": {"file": "patterns.md"},
        "cheatsheet": {"file": "cheatsheet.md"},
        "quizzes": quizzes,
        "flashcards": cards,
        "companion": b.SLUG + "学习伴侣.html",
    }
    with open(out, "w") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest

if __name__ == "__main__":
    mod = sys.argv[1]
    b = load(mod)
    bookdir = os.path.join(ROOT, b.DIR)
    assert bookdir, "找不到书目目录"
    write_quiz(b, os.path.join(bookdir, "quiz.md"))
    write_cards(b, os.path.join(bookdir, "flashcards.md"))
    m = write_manifest(b, bookdir, os.path.join(bookdir, "manifest.json"))
    print("ok", bookdir, len(m["quizzes"]), "quiz", len(m["flashcards"]), "cards", len(m["glossary"]), "terms")
