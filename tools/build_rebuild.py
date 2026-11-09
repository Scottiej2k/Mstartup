#!/usr/bin/env python3
"""Build the rebuild-proposal page: the plan, the rewritten Chapter 1, and the current Chapter 1.

Usage: python3 tools/build_rebuild.py
Output: rebuild/rebuild-proposal.html (publish with the Artifact tool; separate from the reader).
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "rebuild" / "rebuild-proposal.html"


def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", t)
    return t.replace("\n", "<br>")


def render(md, prose=False):
    """Small Markdown subset: headings, paragraphs, lists, blockquotes, rules, code lines."""
    out = []
    blocks = [b.strip("\n") for b in re.split(r"\n\s*\n", md.strip()) if b.strip()]
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if b.strip() == "---":
            out.append('<hr class="scene">')
        elif b.startswith(">"):
            parts = []
            while i < len(blocks) and blocks[i].startswith(">"):
                parts.append("\n".join(re.sub(r"^>\s?", "", ln) for ln in blocks[i].split("\n")))
                i += 1
            i -= 1
            out.append('<aside class="note">' + "".join(f"<p>{inline(p)}</p>" for p in parts) + "</aside>")
        elif re.match(r"#{1,3} ", b):
            for ln in b.split("\n"):
                m = re.match(r"(#{1,3}) (.*)", ln)
                if m:
                    lvl = len(m.group(1))
                    out.append(f"<h{lvl + 1}>{inline(m.group(2))}</h{lvl + 1}>")
                else:
                    out.append(f"<p>{inline(ln)}</p>")
        elif re.fullmatch(r"`[^`]+`", b):
            out.append(f'<p class="dash">{html.escape(b.strip("`"), quote=False)}</p>')
        elif all(re.match(r"- ", ln) for ln in b.split("\n")):
            out.append("<ul>" + "".join(f"<li>{inline(ln[2:])}</li>" for ln in b.split("\n")) + "</ul>")
        elif all(re.match(r"\d+\. ", ln) for ln in b.split("\n")):
            items = [re.sub(r"^\d+\. ", "", ln) for ln in b.split("\n")]
            out.append("<ol>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ol>")
        else:
            cls = ""
            if prose:
                if re.fullmatch(r"\*\*[^*]+\*\*", b):
                    cls = ' class="msg in"'
                elif re.fullmatch(r"\*[^*]+\*", b):
                    cls = ' class="msg out"'
            out.append(f"<p{cls}>{inline(b)}</p>")
        i += 1
    return "\n".join(out)


def words(md):
    return len(re.findall(r"\S+", md))


plan = (ROOT / "rebuild" / "00-plan.md").read_text()
new1 = (ROOT / "rebuild" / "01-talk-to-users.md").read_text()
old1 = (ROOT / "chapters" / "01-the-room-nobody-wanted-to-be-in.md").read_text()

# The old chapter uses "# Chapter 1 / ## Title" and a bold FOUNDER'S NOTE label.
old1 = old1.replace("**FOUNDER'S NOTE**\n", "### Founder's Note\n\n")

PAGE = f"""<title>Marriage Startup Rebuild</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=JetBrains+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..600&display=swap">
<style>
/* Layout: one reading column, three views switched from a sticky bar. Same tokens as the manuscript reader. */
:root {{
  --bg: #edf0f1; --paper: #fafbfb; --ink: #161b20; --muted: #5a6670; --rule: #d3dadf;
  --accent: #1b5b72; --accent-ink: #ffffff; --slide: #15222c; --slide-ink: #e8eef1; --slide-mute: #9db0bb;
  --msg-in: #e2e8eb; --msg-out: #d6e7ec;
  --f-display: 'Bricolage Grotesque', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --f-body: 'Newsreader', Georgia, 'Times New Roman', serif;
  --f-mono: 'JetBrains Mono', ui-monospace, Menlo, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --bg: #0e1316; --paper: #141b20; --ink: #e3e8eb; --muted: #93a0a9; --rule: #27323a;
    --accent: #74b9d3; --accent-ink: #0b1216; --slide: #1c2b36; --slide-ink: #eaf0f3; --slide-mute: #9fb2bd;
    --msg-in: #1e282f; --msg-out: #1b3440; color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
  --bg: #0e1316; --paper: #141b20; --ink: #e3e8eb; --muted: #93a0a9; --rule: #27323a;
  --accent: #74b9d3; --accent-ink: #0b1216; --slide: #1c2b36; --slide-ink: #eaf0f3; --slide-mute: #9fb2bd;
  --msg-in: #1e282f; --msg-out: #1b3440; color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--f-body); font-size: 19px; line-height: 1.62; }}
body::before {{ content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 30; background: var(--bg); }}
:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}

.top {{ position: sticky; top: env(safe-area-inset-top, 0px); z-index: 20; background: var(--bg); border-bottom: 1px solid var(--rule); }}
.top-in {{ max-width: 760px; margin-inline: auto; padding-block: 10px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; }}
.brand {{ font-family: var(--f-display); font-weight: 700; font-size: 1.02rem; margin-right: auto; }}
.tabs {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.tabs a {{ font-family: var(--f-mono); font-size: 0.74rem; letter-spacing: 0.02em; text-decoration: none; color: var(--ink);
  border: 1px solid var(--rule); border-radius: 6px; padding: 7px 10px; }}
.tabs a:hover {{ border-color: var(--accent); }}
.tabs a[aria-current="page"] {{ background: var(--accent); border-color: var(--accent); color: var(--accent-ink); }}

main {{ max-width: 760px; margin-inline: auto; padding-block: 28px 80px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
.sheet {{ background: var(--paper); border: 1px solid var(--rule); border-radius: 4px; padding: clamp(20px, 5vw, 52px); min-width: 0; }}
.meta {{ font-family: var(--f-mono); font-size: 0.72rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin: 0 0 18px; }}

h2, h3, h4 {{ font-family: var(--f-display); line-height: 1.15; text-wrap: balance; letter-spacing: -0.01em; }}
h2 {{ font-size: clamp(1.7rem, 5vw, 2.3rem); font-weight: 750; margin: 0 0 0.6em; }}
h3 {{ font-size: 1.32rem; font-weight: 700; margin: 2em 0 0.5em; padding-top: 1.1em; border-top: 1px solid var(--rule); }}
h4 {{ font-size: 0.8rem; font-family: var(--f-mono); font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent); margin: 2.2em 0 0.4em; }}
p {{ margin: 0 0 0.95em; overflow-wrap: break-word; }}
ul, ol {{ margin: 0 0 1em; padding-left: 1.3em; }}
li {{ margin-bottom: 0.35em; }}
code {{ font-family: var(--f-mono); font-size: 0.8em; background: var(--msg-in); padding: 1px 5px; border-radius: 3px; overflow-wrap: anywhere; }}
hr.scene {{ border: 0; height: 1px; background: var(--rule); margin: 2em auto; width: 40%; }}

/* manuscript views */
.prose h2 {{ font-family: var(--f-mono); font-size: 0.8rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); margin: 0 0 6px; }}
.prose h3 {{ font-size: clamp(1.7rem, 5vw, 2.3rem); font-weight: 750; border: 0; padding: 0; margin: 0 0 0.7em; }}
.prose h4 {{ margin-top: 2.4em; }}
.dash {{ font-family: var(--f-mono); font-size: 0.72rem; line-height: 1.7; background: var(--slide); color: var(--slide-ink);
  border-radius: 4px; padding: 10px 12px; margin: 0 0 1.6em; overflow-wrap: anywhere; }}
.msg {{ font-family: var(--f-display); font-size: 0.92rem; line-height: 1.4; max-width: 78%; width: fit-content; padding: 8px 13px; border-radius: 14px; margin: 0 0 6px; }}
.msg.in {{ background: var(--msg-in); border-bottom-left-radius: 4px; }}
.msg.out {{ background: var(--msg-out); margin-left: auto; border-bottom-right-radius: 4px; }}
.msg strong, .msg em {{ font-weight: 500; font-style: normal; }}
.msg + p:not(.msg) {{ margin-top: 1.1em; }}
.note {{ background: var(--slide); color: var(--slide-ink); border-radius: 4px; padding: 18px 20px; margin: 1.6em 0; font-family: var(--f-mono); font-size: 0.8rem; line-height: 1.65; }}
.note p {{ margin: 0 0 0.8em; }}
.note p:last-child {{ margin-bottom: 0; }}
.note code {{ background: transparent; padding: 0; color: var(--slide-mute); font-size: 1em; }}
.front p {{ font-size: 0.98rem; }}
</style>

<div class="top"><div class="top-in">
  <div class="brand">The Marriage Startup · rebuild</div>
  <nav class="tabs" aria-label="Views">
    <a href="#plan">Plan</a>
    <a href="#new-chapter">New Chapter 1</a>
    <a href="#current-chapter">Current Chapter 1</a>
  </nav>
</div></div>

<main>
  <section id="view-plan" class="sheet">
    <p class="meta">Proposal · {words(plan):,} words</p>
    {render(plan)}
  </section>
  <section id="view-new-chapter" class="sheet prose" hidden>
    <p class="meta">Rewritten sample · {words(new1):,} words including the opening page</p>
    {render(new1, prose=True)}
  </section>
  <section id="view-current-chapter" class="sheet prose" hidden>
    <p class="meta">Current manuscript · {words(old1):,} words</p>
    {render(old1, prose=True)}
  </section>
</main>

<script>
(function () {{
  var names = ['plan', 'new-chapter', 'current-chapter'];
  function show() {{
    var h = (location.hash || '').slice(1);
    if (names.indexOf(h) < 0) h = 'plan';
    names.forEach(function (n) {{
      document.getElementById('view-' + n).hidden = n !== h;
    }});
    document.querySelectorAll('.tabs a').forEach(function (a) {{
      if (a.getAttribute('href') === '#' + h) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    }});
    window.scrollTo(0, 0);
  }}
  window.addEventListener('hashchange', show);
  show();
}})();
</script>
"""

OUT.write_text(PAGE)
print(f"wrote {OUT.relative_to(ROOT)} ({len(PAGE):,} bytes)")
