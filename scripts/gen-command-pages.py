#!/usr/bin/env python3
"""
gen-command-pages.py — generate a static detail page per /qa:* command.

Reads scripts/commands-data.json (one object per command) and writes:
  docs/commands/command.css        shared stylesheet
  docs/commands/<name>.html         one detail page per command (64)
  docs/commands/index.html          the command catalog (grouped, filterable)

Run from the repo root:  python3 scripts/gen-command-pages.py
Static output only — no build step at serve time. Re-run after editing the data.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "scripts", "commands-data.json")
OUTDIR = os.path.join(ROOT, "docs", "commands")

VERSION = "v3.10.0"

# group order + a distinct accent per group (on the dark terminal palette)
GROUP_ORDER = [
    "Test planning & management",
    "Static testing, analysis & design",
    "Test levels & change-related testing",
    "Test implementation",
    "Test automation by surface",
    "Test execution — functional & non-functional",
    "Monitoring, control & completion",
    "Version control & PR quality",
    "AI-assisted & reference",
]
GROUP_COLOR = {
    "Test planning & management": "#5da9f2",
    "Static testing, analysis & design": "#ab8df8",
    "Test levels & change-related testing": "#4fd1c5",
    "Test implementation": "#45d483",
    "Test automation by surface": "#38bdf8",
    "Test execution — functional & non-functional": "#f0b03c",
    "Monitoring, control & completion": "#f59e6b",
    "Version control & PR quality": "#f4654f",
    "AI-assisted & reference": "#e879c7",
}
ROLE_LABEL = {"manual": "Manual", "automation": "Automation",
              "performance": "Performance", "leader": "Test Leader", "manager": "Test Manager"}
ROLE_FILE = {"manual": "manual-tester.html", "automation": "automation-tester.html",
             "performance": "performance-tester.html", "leader": "test-leader.html",
             "manager": "test-manager.html"}

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'"
           "%3E%3Crect width='32' height='32' rx='7' fill='%230d0f13'/%3E%3Cpath d='M9 11l6 5-6 5'"
           " stroke='%235ee2a0' stroke-width='2.6' fill='none' stroke-linecap='round'"
           " stroke-linejoin='round'/%3E%3Cpath d='M17 21h7' stroke='%23e9e4d8' stroke-width='2.6'"
           " stroke-linecap='round'/%3E%3C/svg%3E")
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;'
         '9..144,400;9..144,500;9..144,600&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400'
         '&family=JetBrains+Mono:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">')

def e(s):  # escape text
    return html.escape(str(s), quote=False)
def ea(s):  # escape attribute
    return html.escape(str(s), quote=True)
def gslug(g):
    return re.sub(r'[^a-z0-9]+', '-', g.lower()).strip('-')

REVEAL_JS = """<script>
document.documentElement.classList.add('js');
(function(){
  if(!('IntersectionObserver' in window)){document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in');});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{rootMargin:'0px 0px -8% 0px',threshold:0.05});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
})();
</script>"""

FILTER_JS = """<script>
document.documentElement.classList.add('js');
(function(){
  var box=document.getElementById('filter'); if(!box) return;
  var cards=[].slice.call(document.querySelectorAll('.ccard'));
  var groups=[].slice.call(document.querySelectorAll('.cat-group'));
  var count=document.getElementById('count');
  box.addEventListener('input',function(){
    var q=box.value.trim().toLowerCase(); var n=0;
    cards.forEach(function(c){var hit=c.getAttribute('data-text').indexOf(q)>-1;c.style.display=hit?'':'none';if(hit)n++;});
    groups.forEach(function(g){var any=g.querySelector('.ccard:not([style*="none"])');g.style.display=any?'':'none';});
    if(count) count.textContent=n+' / '+cards.length;
  });
})();
</script>"""

NAV = """<nav class="topnav" aria-label="Navigation">
  <div class="wrap">
    <a class="wordmark" href="../index.html">QA Toolkit<span class="v">{ver}</span></a>
    <ul class="navlinks">
      <li><a href="../index.html">Home</a></li>
      <li><a href="index.html">All commands</a></li>
      <li><a href="../COMMAND-GUIDE.md">Guide</a></li>
      <li><a href="../COMMAND-THEORY.md">Theory</a></li>
      <li><a href="../command-reference.html">Reference</a></li>
    </ul>
  </div>
</nav>""".replace("{ver}", VERSION)

FOOTER = """<footer>
  <div class="wrap">
    <div class="foot-line">
      <span>QA Toolkit <strong>{ver}</strong></span><span>64 commands</span>
      <span>MIT license</span><span><a href="../index.html">Home</a></span>
    </div>
    <p class="foot-legal">ISTQB&reg; is a registered trademark of the International Software Testing
    Qualifications Board. ISTQB syllabi and the Glossary are copyrighted by ISTQB — this toolkit
    implements their concepts and terminology; it does not reproduce the syllabi.</p>
  </div>
</footer>""".replace("{ver}", VERSION)


def head(title, desc, css="command.css"):
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
            "<meta charset=\"UTF-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            f"<title>{e(title)}</title>\n<meta name=\"description\" content=\"{ea(desc)}\">\n"
            f"<link rel=\"icon\" href=\"{FAVICON}\">\n{FONTS}\n"
            f"<link rel=\"stylesheet\" href=\"{css}\">\n</head>\n")


def command_page(cmd, names, group_members):
    name = cmd["name"]; group = cmd["group"]; color = GROUP_COLOR.get(group, "#5ee2a0")
    roles = [r for r in cmd.get("roles", []) if r in ROLE_FILE]
    related = [r for r in cmd.get("related", []) if r in names]
    steps = "".join(f"<li>{e(s)}</li>" for s in cmd.get("howItWorks", []))
    relchips = "".join(f'<a class="chip" href="{ea(r)}.html">/qa:{e(r)}</a>' for r in related) or '<span class="muted">—</span>'
    rolechips = "".join(f'<a class="chip role-{r}" href="../{ROLE_FILE[r]}">{e(ROLE_LABEL[r])}</a>' for r in roles) or '<span class="muted">any role</span>'
    roles_meta = " · ".join(ROLE_LABEL[r] for r in roles) if roles else "all roles"

    # prev / next within the same group (data order)
    idx = group_members.index(name)
    prev_n = group_members[idx - 1] if idx > 0 else None
    next_n = group_members[idx + 1] if idx < len(group_members) - 1 else None
    pv = (f'<a class="pn prev" href="{ea(prev_n)}.html"><span>&larr; Prev</span><b>/qa:{e(prev_n)}</b></a>'
          if prev_n else '<span></span>')
    nx = (f'<a class="pn next" href="{ea(next_n)}.html"><span>Next &rarr;</span><b>/qa:{e(next_n)}</b></a>'
          if next_n else '<span></span>')

    body = []
    body.append(f'<body style="--rc:{color}">')
    body.append(NAV)
    # hero
    body.append('<header class="chero" id="top"><div class="wrap">')
    body.append(f'<p class="kicker reveal"><a href="index.html#{gslug(group)}">{e(group)}</a></p>')
    body.append(f'<h1 class="reveal"><span class="slash">/qa:</span>{e(name)}</h1>')
    body.append(f'<p class="ctitle reveal">{e(cmd["title"])}</p>')
    body.append(f'<p class="standfirst reveal">{e(cmd["tagline"])}</p>')
    body.append(f'<div class="usage reveal"><span class="ul">USAGE</span><code>{e(cmd["usage"])}</code></div>')
    body.append(f'<div class="meta-row reveal"><span>{e(group)}</span><span>{e(cmd["istqb"])}</span><span>{e(roles_meta)}</span></div>')
    body.append('</div></header>')
    body.append('<main>')
    # overview grid
    body.append('<section class="reveal"><div class="wrap"><div class="ov-grid">')
    body.append(f'<div class="ov-card"><h3>What it does</h3><p>{e(cmd["whatItDoes"])}</p></div>')
    body.append(f'<div class="ov-card"><h3>When to use it</h3><p>{e(cmd["when"])}</p></div>')
    body.append(f'<div class="ov-card"><h3>Prerequisites</h3><p>{e(cmd["needs"])}</p></div>')
    body.append(f'<div class="ov-card"><h3>Output</h3><p>{e(cmd["output"])}</p></div>')
    body.append('</div></div></section>')
    # how it works
    body.append('<section class="reveal"><div class="wrap"><p class="kicker">Mechanics</p>'
                '<h2 class="sec-title">How it works</h2>'
                f'<ol class="steps">{steps}</ol></div></section>')
    # theory
    body.append('<section class="reveal"><div class="wrap"><p class="kicker">Why it works</p>'
                '<h2 class="sec-title">The theory behind it</h2>'
                f'<div class="theory"><p>{e(cmd["theory"])}</p>'
                f'<p class="istqb-tag">{e(cmd["istqb"])}</p></div></div></section>')
    # example
    ex = cmd.get("example", {})
    body.append('<section class="reveal"><div class="wrap"><p class="kicker">Example</p>'
                '<h2 class="sec-title">See it in use</h2>'
                f'<div class="term"><div class="term-bar"><i></i><i></i><i></i><span>{e(name)}</span></div>'
                f'<pre><span class="p">&gt; {e(ex.get("cmd",""))}</span></pre></div>'
                f'<p class="correct"><span class="ok">&#10003; Correct when</span> {e(ex.get("correctWhen",""))}</p>'
                '</div></section>')
    # related & roles
    body.append('<section class="reveal"><div class="wrap"><div class="rel-grid">'
                f'<div><p class="kicker">Related commands</p><div class="chips">{relchips}</div></div>'
                f'<div><p class="kicker">Used by</p><div class="chips">{rolechips}</div></div>'
                '</div>'
                f'<nav class="prevnext">{pv}<a class="pn allc" href="index.html">All commands</a>{nx}</nav>'
                '</div></section>')
    body.append('</main>')
    body.append(FOOTER)
    body.append(REVEAL_JS)
    body.append('</body>\n</html>\n')
    title = f"/qa:{name} — {cmd['title']} · QA Toolkit"
    return head(title, cmd["tagline"]) + "\n".join(body)


def catalog_page(data):
    by_group = {g: [] for g in GROUP_ORDER}
    for c in data:
        by_group.setdefault(c["group"], []).append(c)
    body = []
    body.append('<body>')
    body.append(NAV)
    body.append('<header class="chero cat" id="top"><div class="wrap">')
    body.append('<p class="kicker reveal">The catalog</p>')
    body.append('<h1 class="reveal">All <em>64</em> commands</h1>')
    body.append('<p class="standfirst reveal">Every <code>/qa:*</code> command, grouped by ISTQB activity. '
                'Click any command for its dedicated page — what it does, how it works, the theory behind it, '
                'and a worked example.</p>')
    body.append('<div class="filterbar reveal"><input id="filter" type="search" '
                'placeholder="Filter commands…" autocomplete="off" aria-label="Filter commands">'
                '<span id="count" class="count">64 / 64</span></div>')
    body.append('</div></header><main>')
    for g in GROUP_ORDER:
        cmds = by_group.get(g, [])
        if not cmds:
            continue
        color = GROUP_COLOR.get(g, "#5ee2a0")
        body.append(f'<section class="cat-group" id="{gslug(g)}" style="--rc:{color}"><div class="wrap">')
        body.append(f'<h2 class="grp-title reveal"><span class="dot"></span>{e(g)} '
                    f'<span class="grp-n">{len(cmds)}</span></h2>')
        body.append('<div class="ccards">')
        for c in cmds:
            dt = ea((c["name"] + " " + c["title"] + " " + c["tagline"] + " " + c["istqb"]).lower())
            body.append(f'<a class="ccard reveal" href="{ea(c["name"])}.html" data-text="{dt}">'
                        f'<span class="cc-name">/qa:{e(c["name"])}</span>'
                        f'<span class="cc-tag">{e(c["tagline"])}</span>'
                        f'<span class="cc-go">open &rarr;</span></a>')
        body.append('</div></div></section>')
    body.append('</main>')
    body.append(FOOTER)
    body.append(FILTER_JS)
    body.append(REVEAL_JS.replace('document.documentElement.classList.add(\'js\');\n', ''))
    body.append('</body>\n</html>\n')
    return head("All commands — QA Toolkit", "All 64 /qa:* commands, grouped by ISTQB activity, each linking to its dedicated detail page.") + "\n".join(body)


CSS = r""":root{
  --bg:#0d0f13;--bg-deep:#0a0c10;--surface:#12151c;--surface-2:#161a22;
  --hairline:rgba(232,228,217,.10);--hairline-2:rgba(232,228,217,.06);
  --text:#e9e4d8;--text-soft:#c8c4ba;--dim:#9aa1ab;--faint:#788089;
  --accent:#5ee2a0;--accent-dim:#3da874;
  --c-manual:#f0b03c;--c-auto:#45d483;--c-perf:#f4654f;--c-leader:#5da9f2;--c-manager:#ab8df8;
  --serif:"Fraunces",Georgia,serif;--sans:"Public Sans",-apple-system,"Segoe UI",sans-serif;
  --mono:"JetBrains Mono","SFMono-Regular",Menlo,Consolas,monospace;
  --wrap:1120px;--prose:760px;--rc:var(--accent);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto;}*,*::before,*::after{animation:none!important;transition:none!important;}}
body{background:var(--bg);color:var(--text);font-family:var(--sans);font-size:1.0625rem;line-height:1.7;-webkit-font-smoothing:antialiased;
  background-image:radial-gradient(1200px 600px at 50% -10%,color-mix(in srgb,var(--rc) 7%,transparent),transparent 60%),
  linear-gradient(rgba(232,228,217,.022) 1px,transparent 1px),linear-gradient(90deg,rgba(232,228,217,.022) 1px,transparent 1px);
  background-size:auto,56px 56px,56px 56px;}
::selection{background:color-mix(in srgb,var(--rc) 28%,transparent);color:#fff;}
a{color:var(--rc);text-decoration:none;}a:hover{text-decoration:underline;text-underline-offset:3px;}
a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--rc);outline-offset:3px;border-radius:2px;}
code,kbd{font-family:var(--mono);}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 28px;}
.muted{color:var(--faint);}
.kicker{font-family:var(--mono);font-size:.72rem;font-weight:500;letter-spacing:.28em;text-transform:uppercase;color:var(--rc);}
.kicker::before{content:"// ";color:var(--faint);letter-spacing:0;}
.kicker a{color:var(--rc);}
h2.sec-title{font-family:var(--serif);font-weight:400;font-size:clamp(1.7rem,3.4vw,2.4rem);line-height:1.14;letter-spacing:-.01em;margin:.5em 0 .4em;}
section{padding:60px 0 54px;border-top:1px solid var(--hairline-2);}
/* nav */
.topnav{position:sticky;top:0;z-index:50;background:rgba(13,15,19,.94);border-bottom:1px solid var(--hairline);}
@supports (backdrop-filter:blur(6px)){.topnav{background:rgba(13,15,19,.82);backdrop-filter:blur(8px);}}
.topnav .wrap{display:flex;align-items:center;justify-content:space-between;gap:18px;height:56px;}
.wordmark{font-family:var(--serif);font-weight:500;font-style:italic;font-size:1.08rem;color:var(--text);white-space:nowrap;}
.wordmark:hover{text-decoration:none;color:var(--rc);}
.wordmark .v{font-family:var(--mono);font-style:normal;font-size:.66rem;color:var(--faint);letter-spacing:.08em;margin-left:.5em;vertical-align:2px;}
.navlinks{display:flex;gap:4px;list-style:none;}
.navlinks a{font-family:var(--mono);font-size:.74rem;letter-spacing:.06em;color:var(--dim);padding:6px 10px;border-radius:4px;white-space:nowrap;}
.navlinks a:hover{color:var(--text);text-decoration:none;background:rgba(232,228,217,.05);}
@media (max-width:920px){.topnav .wrap{height:auto;flex-wrap:wrap;padding:10px 28px;}.navlinks{flex-wrap:wrap;}}
/* hero */
.chero{padding:64px 0 44px;}
.chero h1{font-family:var(--mono);font-weight:500;font-size:clamp(2rem,5vw,3.2rem);line-height:1.05;letter-spacing:-.02em;margin:.2em 0 .1em;color:var(--text);}
.chero h1 .slash{color:var(--rc);}
.chero h1 em{font-family:var(--serif);font-style:italic;font-weight:400;color:var(--rc);}
.ctitle{font-family:var(--serif);font-size:clamp(1.2rem,2.4vw,1.6rem);color:var(--text-soft);margin-bottom:.5em;}
.standfirst{max-width:var(--prose);font-size:clamp(1.02rem,1.7vw,1.18rem);color:var(--text-soft);}
.standfirst code{font-size:.85em;color:var(--rc);}
.usage{margin-top:22px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
.usage .ul{font-family:var(--mono);font-size:.6rem;letter-spacing:.2em;color:var(--faint);border:1px solid var(--hairline);border-radius:4px;padding:3px 7px;}
.usage code{font-family:var(--mono);font-size:.86rem;color:var(--text);background:var(--bg-deep);border:1px solid var(--hairline);border-radius:7px;padding:9px 14px;display:inline-block;}
.meta-row{display:flex;flex-wrap:wrap;gap:.4em 0;align-items:center;margin-top:22px;font-family:var(--mono);font-size:.74rem;letter-spacing:.04em;color:var(--dim);}
.meta-row>span+span::before{content:"·";margin:0 .9em;color:var(--faint);}
/* overview grid */
.ov-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--hairline-2);border:1px solid var(--hairline-2);border-radius:12px;overflow:hidden;}
.ov-card{background:var(--surface);padding:22px 24px;}
.ov-card h3{font-family:var(--mono);font-size:.66rem;font-weight:500;letter-spacing:.2em;text-transform:uppercase;color:var(--rc);margin-bottom:9px;}
.ov-card p{font-size:.98rem;color:var(--text-soft);}
@media (max-width:680px){.ov-grid{grid-template-columns:1fr;}}
/* steps */
.steps{counter-reset:s;list-style:none;display:grid;gap:14px;max-width:860px;margin-top:6px;}
.steps li{counter-increment:s;position:relative;padding:14px 18px 14px 56px;background:var(--surface);border:1px solid var(--hairline-2);border-radius:9px;color:var(--text-soft);font-size:.98rem;}
.steps li::before{content:counter(s);position:absolute;left:16px;top:13px;width:26px;height:26px;display:grid;place-items:center;border-radius:50%;background:color-mix(in srgb,var(--rc) 16%,transparent);color:var(--rc);font-family:var(--mono);font-size:.78rem;font-weight:700;}
/* theory */
.theory{max-width:var(--prose);border-left:3px solid var(--rc);padding:4px 0 4px 22px;}
.theory p{font-family:var(--serif);font-size:clamp(1.1rem,2vw,1.3rem);line-height:1.55;color:var(--text);}
.istqb-tag{margin-top:14px!important;font-family:var(--mono)!important;font-style:normal;font-size:.72rem!important;letter-spacing:.06em;color:var(--faint)!important;}
/* terminal */
.term{background:var(--bg-deep);border:1px solid var(--hairline);border-radius:10px;box-shadow:0 14px 44px rgba(0,0,0,.42);overflow:hidden;max-width:860px;}
.term-bar{display:flex;align-items:center;gap:7px;padding:11px 14px;border-bottom:1px solid var(--hairline-2);}
.term-bar i{width:11px;height:11px;border-radius:50%;}
.term-bar i:nth-child(1){background:#e5634f;}.term-bar i:nth-child(2){background:#e0a93e;}.term-bar i:nth-child(3){background:#46c06c;}
.term-bar span{margin-left:auto;font-family:var(--mono);font-size:.68rem;letter-spacing:.08em;color:var(--faint);}
.term pre{padding:16px 20px;font-family:var(--mono);font-size:.86rem;line-height:1.7;overflow-x:auto;color:var(--text-soft);white-space:pre-wrap;}
.term .p{color:var(--accent);}
.correct{margin-top:16px;font-size:.96rem;color:var(--text-soft);max-width:860px;}
.correct .ok{font-family:var(--mono);font-size:.74rem;letter-spacing:.04em;color:var(--accent);margin-right:.5em;}
/* related + roles */
.rel-grid{display:grid;grid-template-columns:1fr 1fr;gap:30px;}
@media (max-width:680px){.rel-grid{grid-template-columns:1fr;}}
.chips{display:flex;flex-wrap:wrap;gap:9px;margin-top:12px;}
.chip{font-family:var(--mono);font-size:.76rem;color:var(--text-soft);border:1px solid var(--hairline);border-radius:6px;padding:6px 11px;background:var(--surface);}
.chip:hover{text-decoration:none;border-color:var(--rc);color:var(--text);}
.chip.role-manual{border-left:3px solid var(--c-manual);}
.chip.role-automation{border-left:3px solid var(--c-auto);}
.chip.role-performance{border-left:3px solid var(--c-perf);}
.chip.role-leader{border-left:3px solid var(--c-leader);}
.chip.role-manager{border-left:3px solid var(--c-manager);}
.prevnext{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-top:40px;padding-top:24px;border-top:1px solid var(--hairline-2);}
.pn{display:flex;flex-direction:column;gap:3px;font-family:var(--mono);font-size:.74rem;color:var(--dim);}
.pn span{font-size:.64rem;letter-spacing:.1em;color:var(--faint);}
.pn b{color:var(--text);font-weight:500;}
.pn.next{text-align:right;}
.pn.allc{align-self:center;color:var(--rc);}
/* catalog */
.chero.cat h1 em{font-family:var(--serif);font-style:italic;color:var(--accent);}
.filterbar{margin-top:26px;display:flex;align-items:center;gap:14px;}
#filter{flex:1;max-width:420px;background:var(--bg-deep);border:1px solid var(--hairline);border-radius:8px;color:var(--text);font-family:var(--mono);font-size:.84rem;padding:11px 14px;}
#filter::placeholder{color:var(--faint);}
.count{font-family:var(--mono);font-size:.74rem;color:var(--faint);}
.cat-group{padding:44px 0 30px;}
.grp-title{font-family:var(--serif);font-weight:500;font-size:1.5rem;display:flex;align-items:center;gap:12px;margin-bottom:6px;}
.grp-title .dot{width:11px;height:11px;border-radius:50%;background:var(--rc);flex:none;}
.grp-title .grp-n{font-family:var(--mono);font-size:.7rem;color:var(--faint);font-weight:400;}
.ccards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;margin-top:18px;}
.ccard{display:flex;flex-direction:column;gap:7px;background:var(--surface);border:1px solid var(--hairline);border-left:3px solid var(--rc);border-radius:10px;padding:16px 18px;transition:transform .15s ease,border-color .15s ease;}
.ccard:hover{text-decoration:none;transform:translateY(-2px);}
.cc-name{font-family:var(--mono);font-size:.92rem;color:var(--text);font-weight:500;}
.cc-tag{font-size:.86rem;color:var(--dim);line-height:1.5;}
.cc-go{font-family:var(--mono);font-size:.68rem;letter-spacing:.08em;color:var(--rc);}
/* footer */
footer{border-top:1px solid var(--hairline);padding:46px 0 60px;margin-top:24px;}
footer .wrap{display:grid;gap:16px;}
.foot-line{font-family:var(--mono);font-size:.74rem;letter-spacing:.06em;color:var(--dim);display:flex;flex-wrap:wrap;gap:.3em 0;}
.foot-line span+span::before{content:"·";margin:0 .8em;color:var(--faint);}
.foot-line a{color:var(--dim);}
.foot-legal{font-size:.82rem;color:var(--faint);max-width:var(--prose);}
.foot-legal a{color:var(--dim);}
html.js .reveal{opacity:0;transform:translateY(16px);transition:opacity .6s ease,transform .6s ease;}
html.js .reveal.in{opacity:1;transform:none;}
@media print{html.js .reveal{opacity:1!important;transform:none!important;}}
"""


def main():
    data = json.load(open(DATA))
    names = {c["name"] for c in data}
    os.makedirs(OUTDIR, exist_ok=True)
    open(os.path.join(OUTDIR, "command.css"), "w").write(CSS)
    # group members in data order, for prev/next
    members = {}
    for c in data:
        members.setdefault(c["group"], []).append(c["name"])
    n = 0
    for c in data:
        page = command_page(c, names, members[c["group"]])
        open(os.path.join(OUTDIR, f"{c['name']}.html"), "w").write(page)
        n += 1
    open(os.path.join(OUTDIR, "index.html"), "w").write(catalog_page(data))
    print(f"wrote {n} command pages + index.html + command.css to docs/commands/")


if __name__ == "__main__":
    main()
