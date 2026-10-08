#!/usr/bin/env python3
"""
Build the handwritten-style Java OOP notebook.

    python3 build.py            -> ../Java-OOP-Notebook.html
    python3 build.py --verify   -> also compiles/runs every ```java run``` block
                                   and checks it against the ```output``` block below it
    python3 build.py --pdf      -> also renders ../Java-OOP-Notebook.pdf (headless Chromium)

Authoring syntax (chapters/*.md) — plain Markdown plus:
  @sheet [class] [| running head]          new notebook page
  @chapter NN | TITLE | subtitle | lecture  chapter header box
  @index                                    auto-generated INDEX table
  :::type [Title] ... :::                   boxes: idea rule mistake trap reality connect remember
                                            practice teach define doubt mind sticky plain ans
                                            layout: cols cols3 col aside center qa
  ```java "Tab" [run] [bad] [nocompile] [hl=2,4-5]   code (lines starting //! = red pen notes)
  ```sketch "Title" [sm|xs] [left]          pen sketch («hl» ‹red› ⟪green⟫ keep columns)
  ```output / ```err                        program output / error
  [[y:..]] [[g:..]] [[b:..]] [[r:..]] ==..== highlighters | [[o:..]] circle | [[u:..]] underline
  [[x:..]] strike | [[vs]] | @@must @@high @@good chips | Q: / A: lines for Q&A
"""
import base64, html, os, re, shlex, subprocess, sys, tempfile
import markdown
from pygments import highlight
from pygments.lexers import JavaLexer
from pygments.formatters import HtmlFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "Java-OOP-Notebook.html")

DEFAULT_TITLES = {
    "idea": "💡 CORE IDEA", "rule": "⭐ JAVA RULE", "mistake": "⚠️ COMMON MISTAKE",
    "trap": "🎯 INTERVIEW TRAP", "reality": "☕ JAVA REALITY", "connect": "🔗 CONNECT THIS WITH",
    "remember": "⭐ REMEMBER", "practice": "🧪 PRACTICE", "teach": "👨‍🏫 HOW I WOULD TEACH THIS",
    "define": "📖 DEFINITION", "doubt": "❓ STUDENT DOUBT", "mind": "🧠 MENTAL MODEL",
}
LAYOUT = {"cols", "cols3", "col", "aside", "center", "qa", "twocol"}

stash = {}          # placeholder -> final html
runnable = []       # (code, expected_output or None, kind, where)
warnings = []       # lines too wide for the page


def put(html_text):
    key = f"PHX{len(stash):05d}XHP"
    stash[key] = html_text
    return f"\n\n{key}\n\n"


def md_inline(text):
    s = markdown.markdown(inline_marks(text), extensions=["attr_list"])
    return re.sub(r"^<p>(.*)</p>$", r"\1", s.strip(), flags=re.S)


# ---------------------------------------------------------------- inline marks
INLINE_CODE = re.compile(r"(`+)(.+?)\1")

def inline_marks(text):
    codes = []
    def keep(m):
        codes.append(m.group(0)); return f"\x00{len(codes)-1}\x00"
    t = INLINE_CODE.sub(keep, text)
    cls = {"y": "hl-y", "g": "hl-g", "b": "hl-b", "r": "hl-r", "o": "circ", "u": "uline", "x": "strike"}
    for _ in range(2):  # allow one level of nesting
        t = re.sub(r"\[\[([ygbroux]):(.+?)\]\]", lambda m: f'<span class="{cls[m.group(1)]}">{m.group(2)}</span>', t)
    t = t.replace("[[vs]]", '<span class="vs">vs</span>')
    t = re.sub(r"==(?=\S)(.+?)(?<=\S)==", r'<mark>\1</mark>', t)
    t = t.replace("@@must", '<span class="chip must">🔴 MUST KNOW</span>')
    t = t.replace("@@high", '<span class="chip high">🟠 HIGHLY IMPORTANT</span>')
    t = t.replace("@@good", '<span class="chip good">🟡 GOOD TO KNOW</span>')
    t = re.sub(r"✓", '<span class="tick">✓</span>', t)
    t = re.sub(r"✗", '<span class="cross">✗</span>', t)
    t = re.sub(r"(?<![\w>])★", '<span class="star">★</span>', t)
    t = re.sub(r"≠", '<span class="neq">≠</span>', t)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], t)


# ---------------------------------------------------------------- code blocks
def render_java(code, opts, title):
    lines = code.split("\n")
    ann, real = {}, []
    for ln in lines:
        if ln.startswith("//!"):
            ann.setdefault(len(real), []).append(ln[3:])
        else:
            real.append(ln)
    hl = set()
    for part in opts.get("hl", "").split(","):
        if "-" in part:
            a, b = part.split("-"); hl.update(range(int(a), int(b) + 1))
        elif part.strip():
            hl.add(int(part))
    body = highlight("\n".join(real), JavaLexer(), HtmlFormatter(nowrap=True)).rstrip("\n").split("\n")
    out = []
    for i, h in enumerate(body):
        for a in ann.get(i, []):
            out.append('<span class="ann">   ' + html.escape(a) + "</span>")
        out.append(f'<span class="hll">{h}</span>' if (i + 1) in hl else h)
    for a in ann.get(len(body), []):
        out.append('<span class="ann">   ' + html.escape(a) + "</span>")
    klass = "code bad" if "bad" in opts or "nocompile" in opts else "code"
    tab = title or ("✗ Won't compile" if "nocompile" in opts else "Java")
    return f'<div class="{klass}"><span class="tab">{md_inline(tab)}</span><pre>' + "\n".join(out) + "</pre></div>"


def render_sketch(code, opts, title):
    t = html.escape(code)
    t = re.sub(r"[\u2500-\u257F]+", lambda m: f'<span class="bx">{m.group(0)}</span>', t)
    t = re.sub(r"[\u2190-\u21FF▲▼◀▶]+", lambda m: f'<span class="ar">{m.group(0)}</span>', t)
    t = t.replace("✓", '<span class="ok">✓</span>').replace("✗", '<span class="no">✗</span>')
    t = re.sub(r"[★☆]", lambda m: f'<span class="st">{m.group(0)}</span>', t)
    t = re.sub(r"«(.+?)»", r' <span class="hl">\1</span> ', t)
    t = re.sub(r"‹(.+?)›", r' <span class="rd">\1</span> ', t)
    t = re.sub(r"⟪(.+?)⟫", r' <span class="gl">\1</span> ', t)
    size = " sm" if "sm" in opts else (" xs" if "xs" in opts else "")
    wrap = "sketch-wrap left" if "left" in opts else "sketch-wrap"
    cap = f'<div class="sketch-title">{md_inline(title)}</div>' if title else ""
    return f'<div class="{wrap}">{cap}<pre class="sketch{size}">{t}</pre></div>'


def render_output(code, kind, title):
    tab = title or ("💥 Error" if kind == "err" else "▶ Output")
    klass = "output err" if kind == "err" else "output"
    return f'<div class="{klass}"><span class="tab">{md_inline(tab)}</span><pre>{html.escape(code)}</pre></div>'


FENCE = re.compile(r"^```(\w+)?([^\n]*)\n(.*?)\n```[ \t]*$", re.S | re.M)

def process_fences(src, where):
    pending = {"java": None}
    def repl(m):
        lang, info, code = (m.group(1) or "text"), m.group(2).strip(), m.group(3)
        toks = shlex.split(info) if info else []
        title, opts = None, {}
        for tk in toks:
            if "=" in tk:
                k, v = tk.split("=", 1); opts[k] = v
            elif tk in ("run", "bad", "nocompile", "sm", "xs", "left"):
                opts[tk] = True
            else:
                title = tk if title is None else title + " " + tk
        limit = {"java": 76, "sketch": 83 if "sm" in opts else (90 if "xs" in opts else 74)}.get(lang, 400)
        for ln in code.split("\n"):
            if len(ln) > limit:
                warnings.append(f"{where}: {lang} line {len(ln)}>{limit}: {ln.strip()[:60]}")
        if lang == "java":
            clean = "\n".join(l for l in code.split("\n") if not l.startswith("//!"))
            if "run" in opts:
                runnable.append([clean, None, "run", where]); pending["java"] = len(runnable) - 1
            elif "nocompile" in opts:
                runnable.append([clean, None, "nocompile", where]); pending["java"] = None
            else:
                pending["java"] = None
            return put(render_java(code, opts, title))
        if lang in ("output", "err"):
            if pending["java"] is not None:
                runnable[pending["java"]][1] = code
            pending["java"] = None
            return put(render_output(code, lang, title))
        pending["java"] = None
        if lang == "sketch":
            return put(render_sketch(code, opts, title))
        return put(f'<div class="code"><span class="tab">{lang}</span><pre>{html.escape(code)}</pre></div>')
    return FENCE.sub(repl, src)


# ---------------------------------------------------------------- directives / containers
def process_blocks(src):
    out, stack, page = [], [], 0
    for line in src.split("\n"):
        s = line.rstrip()
        if s.startswith("@sheet"):
            if stack:
                warnings.append(f"page {page + 1} started with open box(es): {stack}")
            while stack:
                out.append(put("</div>" if stack.pop() != "ans" else "</details>"))
            if page:
                out.append(put("</section>"))
            page += 1
            rest = s[6:].strip()
            klass, head = (rest.split("|", 1) + [""])[:2] if "|" in rest else (rest, "")
            runhead = f'<div class="runhead">{md_inline(head.strip())}</div>' if head.strip() else ""
            out.append(put(
                f'<section class="sheet {klass.strip()}" id="page-{page}" data-page="{page}">'
                f'<div class="pg"><span>Page No.</span><b>{page}</b><span>Date</span><b>__/__/__</b></div>{runhead}'))
            continue
        if s.startswith("@chapter"):
            parts = [p.strip() for p in s[8:].split("|")] + ["", "", "", ""]
            num, title, sub, lec = parts[:4]
            out.append(put(
                f'<div class="chapter" data-num="{num}" data-title="{html.escape(title)}">'
                f'<span class="num">{num}</span><div class="title">{md_inline(title)}</div>'
                + (f'<div class="sub">{md_inline(sub)}</div>' if sub else "")
                + (f'<span class="lec">{md_inline(lec)}</span>' if lec else "") + "</div>"))
            continue
        if s == "@index":
            out.append(put("<!--INDEX-->"))
            continue
        m = re.match(r"^:::(\w+)\s*(.*)$", s)
        if m:
            kind, title = m.group(1), m.group(2).strip()
            stack.append(kind)
            if kind == "ans":
                out.append(put(f'<details class="ans"><summary>{md_inline(title or "☑ Answer")}</summary>'))
            elif kind in LAYOUT:
                out.append(put(f'<div class="{kind}">'))
            else:
                title = title or DEFAULT_TITLES.get(kind, "")
                tdiv = f'<div class="box-title">{md_inline(title)}</div>' if title else ""
                out.append(put(f'<div class="box {kind}">{tdiv}'))
            continue
        if s == ":::":
            if not stack:
                warnings.append(f"stray ':::' closer near: {out[-1][:40] if out else ''}")
                continue
            kind = stack.pop()
            out.append(put("</details>" if kind == "ans" else "</div>"))
            continue
        q = re.match(r"^(Q|A):\s+(.*)$", s)
        if q:
            out.append("\n" + inline_marks(q.group(2)) + "\n{: ." + q.group(1).lower() + "}\n")
            continue
        out.append(inline_marks(line))
    while stack:
        out.append(put("</div>"))
    if page:
        out.append(put("</section>"))
    return "\n".join(out)


# ---------------------------------------------------------------- index + headings
def finish(body):
    def unstash(text):
        for _ in range(3):
            text = re.sub(r"<p>(PHX\d{5}XHP)</p>", lambda m: stash[m.group(1)], text)
            text = re.sub(r"PHX\d{5}XHP", lambda m: stash[m.group(0)], text)
        return text
    body = unstash(body)
    rows, page, k = [], 0, 0
    def walker(m):
        nonlocal page, k
        tok = m.group(0)
        if tok.startswith("<section"):
            page = int(re.search(r'data-page="(\d+)"', tok).group(1)); return tok
        if tok.startswith('<div class="chapter"'):
            num = re.search(r'data-num="([^"]*)"', tok).group(1)
            title = html.unescape(re.search(r'data-title="([^"]*)"', tok).group(1))
            rows.append(("chap", num, title, page, f"page-{page}")); return tok
        k += 1
        inner = m.group(2)
        plain = html.unescape(re.sub(r"<[^>]+>", "", inner)).replace("✦", "").strip()
        if plain != "INDEX":
            rows.append(("h1", "", plain, page, f"t{k}"))
        return f'<h1 id="t{k}"><span class="u">{inner}</span></h1>'
    body = re.sub(r'<section[^>]*>|<div class="chapter"[^>]*>|<h1( [^>]*)?>(.*?)</h1>', walker, body, flags=re.S)
    body = re.sub(r"<h2>(.*?)</h2>", r'<h2><span class="u">\1</span></h2>', body, flags=re.S)
    trs, n = [], 0
    for kind, num, title, pg, anchor in rows:
        if kind == "chap":
            trs.append(f'<tr class="chap"><td>{num}</td><td><a href="#{anchor}">{html.escape(title)}</a></td><td>{pg}</td></tr>')
        else:
            n += 1
            trs.append(f'<tr><td>{n}</td><td><a href="#{anchor}">{html.escape(title)}</a></td><td>{pg}</td></tr>')
    idx = ('<table class="idx plainfirst"><thead><tr><th>S.No.</th><th>Name of the Topic</th><th>Page No.</th></tr></thead><tbody>'
           + "".join(trs) + "</tbody></table>")
    return body.replace("<!--INDEX-->", idx)


def font_face():
    faces = [("Caveat", "Caveat.woff2", "400 700"), ("Kalam", "Kalam-300.woff2", "300"),
             ("Kalam", "Kalam-400.woff2", "400"), ("Kalam", "Kalam-700.woff2", "700"),
             ("JetBrains Mono", "JetBrainsMono.woff2", "100 800"),
             ("Radon", "Radon-Regular.woff2", "400"), ("Radon", "Radon-Bold.woff2", "700")]
    css = []
    for fam, f, w in faces:
        data = base64.b64encode(open(os.path.join(HERE, "fonts", f), "rb").read()).decode()
        css.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;"
                   f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return "\n".join(css)


def verify():
    ok = bad = 0
    for i, (code, expected, kind, where) in enumerate(runnable):
        m = re.search(r"public\s+(?:final\s+)?class\s+(\w+)", code)
        name = m.group(1) if m else None
        if not name:
            mains = [c.group(1) for c in re.finditer(r"class\s+(\w+)[^{]*\{", code)
                     if "static void main" in code[c.end():].split("\nclass ")[0]]
            name = mains[-1] if mains else "Main"
        d = tempfile.mkdtemp()
        open(os.path.join(d, name + ".java"), "w").write(code)
        c = subprocess.run(["javac", "-nowarn", "-Xlint:none", "-d", d, os.path.join(d, name + ".java")],
                           capture_output=True, text=True)
        if kind == "nocompile":
            if c.returncode == 0:
                bad += 1; print(f"✗ [{where}] #{i} expected a compile error but it compiled:\n{code[:300]}\n")
            else:
                ok += 1
            continue
        if c.returncode != 0:
            bad += 1; print(f"✗ [{where}] #{i} does not compile:\n{c.stderr[:900]}\n{code[:400]}\n"); continue
        r = subprocess.run(["java", "-cp", d, name], capture_output=True, text=True, timeout=30)
        got = r.stdout.rstrip()
        if expected is not None and got != expected.rstrip():
            exp_first = expected.strip().split("\n")
            if not (r.stderr and "Exception" in expected):
                bad += 1
                print(f"✗ [{where}] #{i} output mismatch in {name}\n--- expected\n{expected}\n--- got\n{got}\n--- stderr\n{r.stderr[:400]}\n")
                continue
        ok += 1
    print(f"verify: {ok} passed, {bad} failed, {len(runnable)} total")
    return bad == 0


def main():
    parts = []
    chapters = sorted(f for f in os.listdir(os.path.join(HERE, "chapters")) if f.endswith(".md"))
    for f in chapters:
        src = open(os.path.join(HERE, "chapters", f), encoding="utf-8").read()
        parts.append(process_fences(src, f))
    blocks = process_blocks("\n\n".join(parts))
    body = markdown.markdown(blocks, extensions=["tables", "attr_list", "sane_lists"])
    body = finish(body)
    css = open(os.path.join(HERE, "notebook.css"), encoding="utf-8").read()
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>✦ JAVA OOP ✦ — Handwritten Notebook</title>
<style>
{font_face()}
{css}
</style></head>
<body>
{body}
<a class="fab" href="#page-2">☰ Index</a>
</body></html>"""
    open(OUT, "w", encoding="utf-8").write(page)
    for w in warnings:
        print("⚠ wide:", w)
    print(f"wrote {os.path.relpath(OUT)} ({len(page)//1024} KB, {len(chapters)} chapter files, {len(runnable)} checked code blocks)")
    ok = verify() if "--verify" in sys.argv else True
    if "--pdf" in sys.argv:
        subprocess.run(["node", os.path.join(HERE, "render.js"), "pdf"], check=True)
        pdf = os.path.join(HERE, "..", "Java-OOP-Notebook.pdf")
        try:
            from pypdf import PdfReader, PdfWriter
            w = PdfWriter(clone_from=PdfReader(pdf))
            for pg in w.pages:
                pg.compress_content_streams(level=9)
            w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
            w.write(pdf)
            print(f"compacted PDF → {os.path.getsize(pdf) / 1048576:.1f} MB, {len(w.pages)} pages")
        except ImportError:
            print("(pip install pypdf to shrink the PDF)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
