#!/usr/bin/env python3
"""Build the manuscript reader page from chapters/*.md.

Usage: python3 tools/build_reader.py
Outputs:
  reader/the-marriage-startup.html   publish this with the Artifact tool
  reader/db/cNN.json, meta.json      one doc per chapter plus a build stamp; write these into the
                                     artifact database (collections `chapters` and `meta`, doc `build`)
                                     so the reader's Update button can pull the latest text without a republish.

Chapter status labels live in STATUS below; update them as chapters are approved.
"""
import hashlib
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = sorted((ROOT / "chapters").glob("[0-9][0-9]-*.md"))
OUT = ROOT / "reader" / "the-marriage-startup.html"
DB_OUT = ROOT / "reader" / "db"

STATUS = {1: "Approved"}  # anything else shows as "Draft"


def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", t)
    return t.replace("\n", "<br>")


def block_html(kind, pid, md):
    if kind == "hr":
        return '<hr class="scene">'
    cls = {"in": ' class="msg in"', "out": ' class="msg out"', "sign": ' class="sign"', "principle": ' class="principle"'}.get(kind, "")
    return f'<p{cls} data-p="{pid}">{inline(md)}</p>'


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
    idx = 0

    def pid():
        nonlocal idx
        idx += 1
        return f"c{num}-p{idx}"

    story_blocks = []  # [kind, id, markdown]
    for b in story:
        if b == "---":
            story_blocks.append(["hr", "", ""])
            continue
        m_bold = re.fullmatch(r"\*\*(.+)\*\*", b, flags=re.S)
        m_ital = re.fullmatch(r"\*([^*].*)\*", b, flags=re.S)
        if m_bold and "**" not in m_bold.group(1):
            txt = m_bold.group(1)
            letters = re.sub(r"[^A-Za-z]", "", txt)
            kind = "sign" if letters and letters.upper() == letters and len(letters) > 6 else "in"
            story_blocks.append([kind, pid(), txt])
        elif m_ital and "*" not in m_ital.group(1):
            story_blocks.append(["out", pid(), m_ital.group(1)])
        else:
            story_blocks.append(["p", pid(), b])

    note_blocks = []
    if note:
        rest = note[1:]
        if rest and re.fullmatch(r"\*[^*].*\*", rest[0], flags=re.S):
            note_blocks.append(["principle", pid(), rest[0].strip("*")])
            rest = rest[1:]
        for p in rest:
            note_blocks.append(["p", pid(), p])

    status = STATUS.get(num, "Draft")
    digest = hashlib.sha1(json.dumps([title, status, story_blocks, note_blocks], sort_keys=True).encode()).hexdigest()[:12]
    return {
        "n": num, "title": title, "words": words, "status": status, "hash": digest,
        "blocks": story_blocks, "note": note_blocks,
    }


def section_html(c):
    note_html = ""
    if c["note"]:
        paras = "".join(block_html(*b) for b in c["note"])
        note_html = (
            '<aside class="note" aria-label="Founder\'s Note">'
            '<div class="note-label">Founder\'s Note</div>'
            f"{paras}</aside>"
        )
    prose = "".join(block_html(*b) for b in c["blocks"])
    return (
        f'<section class="chapter" id="ch{c["n"]}" data-n="{c["n"]}" data-words="{c["words"]}" '
        f'data-hash="{c["hash"]}" data-title="{html.escape(c["title"], quote=True)}">'
        f'<header class="chap-head"><div class="eyebrow">Chapter {c["n"]}</div>'
        f'<h2>{html.escape(c["title"])}</h2>'
        f'<div class="chap-meta"><span>{c["words"]:,} words</span>'
        f'<span class="pill {c["status"].lower()}">{c["status"]}</span></div></header>'
        f'<div class="prose">{prose}</div>{note_html}</section>'
    )


def main():
    chapters = [parse(p) for p in CHAPTERS]
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    nav = "".join(
        f'<a class="ch" href="#ch{c["n"]}" data-n="{c["n"]}"><span class="n">{c["n"]}</span>'
        f'<span class="t">{html.escape(c["title"])}</span>'
        f'<span class="m">{c["words"]:,} words · {c["status"]}</span></a>'
        for c in chapters
    )
    total = sum(c["words"] for c in chapters)
    page = TEMPLATE
    page = page.replace("__NAV__", nav)
    page = page.replace("__CHAPTERS__", "\n".join(section_html(c) for c in chapters))
    page = page.replace("__TOTAL__", f"{total:,}")
    page = page.replace("__COUNT__", str(len(chapters)))
    page = page.replace("__BUILD__", stamp)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page)

    DB_OUT.mkdir(exist_ok=True)
    for old in DB_OUT.glob("*.json"):
        old.unlink()
    for c in chapters:
        doc = dict(c)
        doc["stamp"] = stamp
        (DB_OUT / f"c{c['n']:02d}.json").write_text(json.dumps(doc, ensure_ascii=False))
    (DB_OUT / "meta.json").write_text(json.dumps({"stamp": stamp, "count": len(chapters), "total": total}))
    print(f"Built {OUT} ({len(chapters)} chapters, {total:,} words, {len(page) // 1024} KB, stamp {stamp})")


TEMPLATE = (Path(__file__).with_name("reader_template.html")).read_text()

if __name__ == "__main__":
    main()
