#!/usr/bin/env python3
"""Build the manuscript reader page from chapters/*.md.

Usage: python3 tools/build_reader.py
Output: reader/the-marriage-startup.html  (publish this with the Artifact tool)

Chapter status labels live in STATUS below; update them as chapters are approved.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = sorted((ROOT / "chapters").glob("[0-9][0-9]-*.md"))
OUT = ROOT / "reader" / "the-marriage-startup.html"

STATUS = {1: "Approved"}  # anything else shows as "Draft"


def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", t)
    return t.replace("\n", "<br>")


def parse(path):
    raw = path.read_text().strip()
    lines = raw.split("\n")
    num = int(re.match(r"#\s*Chapter\s+(\d+)", lines[0]).group(1))
    title = lines[1].lstrip("# ").strip()
    body = "\n".join(lines[2:]).strip()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", body) if b.strip()]

    note_at = next((i for i, b in enumerate(blocks) if b.startswith("**FOUNDER'S NOTE**")), None)
    story, note = (blocks, []) if note_at is None else (blocks[:note_at], blocks[note_at:])
    while story and story[-1] == "---":
        story.pop()

    words = len(re.findall(r"\S+", body))
    out, idx = [], 0

    def pid():
        nonlocal idx
        idx += 1
        return f"c{num}-p{idx}"

    for b in story:
        if b == "---":
            out.append('<hr class="scene">')
            continue
        m_bold = re.fullmatch(r"\*\*(.+)\*\*", b, flags=re.S)
        m_ital = re.fullmatch(r"\*([^*].*)\*", b, flags=re.S)
        if m_bold and "**" not in m_bold.group(1):
            txt = m_bold.group(1)
            letters = re.sub(r"[^A-Za-z]", "", txt)
            cls = "sign" if letters and letters.upper() == letters and len(letters) > 6 else "msg in"
            out.append(f'<p class="{cls}" data-p="{pid()}">{inline(txt)}</p>')
        elif m_ital and "*" not in m_ital.group(1):
            out.append(f'<p class="msg out" data-p="{pid()}">{inline(m_ital.group(1))}</p>')
        else:
            out.append(f'<p data-p="{pid()}">{inline(b)}</p>')

    note_html = ""
    if note:
        rest = note[1:]
        principle = ""
        if rest and re.fullmatch(r"\*[^*].*\*", rest[0], flags=re.S):
            principle = f'<p class="principle" data-p="{pid()}">{inline(rest[0].strip("*"))}</p>'
            rest = rest[1:]
        paras = "".join(f'<p data-p="{pid()}">{inline(p)}</p>' for p in rest)
        note_html = (
            '<aside class="note" aria-label="Founder\'s Note">'
            '<div class="note-label">Founder\'s Note</div>'
            f"{principle}{paras}</aside>"
        )

    status = STATUS.get(num, "Draft")
    section = (
        f'<section class="chapter" id="ch{num}" data-n="{num}" data-title="{html.escape(title, quote=True)}">'
        f'<header class="chap-head"><div class="eyebrow">Chapter {num}</div>'
        f'<h2>{html.escape(title)}</h2>'
        f'<div class="chap-meta"><span>{words:,} words</span>'
        f'<span class="pill {status.lower()}">{status}</span></div></header>'
        f'<div class="prose">{"".join(out)}</div>{note_html}</section>'
    )
    return {"n": num, "title": title, "words": words, "status": status, "html": section}


def main():
    chapters = [parse(p) for p in CHAPTERS]
    nav = "".join(
        f'<a href="#ch{c["n"]}" data-n="{c["n"]}"><span class="n">{c["n"]}</span>'
        f'<span class="t">{html.escape(c["title"])}</span>'
        f'<span class="m">{c["words"]:,} words · {c["status"]}</span></a>'
        for c in chapters
    )
    total = sum(c["words"] for c in chapters)
    page = TEMPLATE
    page = page.replace("__NAV__", nav)
    page = page.replace("__CHAPTERS__", "\n".join(c["html"] for c in chapters))
    page = page.replace("__TOTAL__", f"{total:,}")
    page = page.replace("__COUNT__", str(len(chapters)))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page)
    print(f"Built {OUT} ({len(chapters)} chapters, {total:,} words, {len(page) // 1024} KB)")


TEMPLATE = (Path(__file__).with_name("reader_template.html")).read_text()

if __name__ == "__main__":
    main()
