"""Monta slides.html a partir de deck/project.

Uso (na raiz do repo): uv run python docs/apresentacao/build_html.py docs/apresentacao/deck/project docs/apresentacao/slides.html
"""
import json, sys
from pathlib import Path
deck = Path(sys.argv[1]); out = Path(sys.argv[2])
meta = json.loads((deck / "deck.json").read_text(encoding="utf-8"))
css = (deck / "deck.css").read_text(encoding="utf-8")
slides = "\n".join((deck / "slides" / f"{sid}.html").read_text(encoding="utf-8") for sid in meta["order"])
html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta['title']}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&family=Inter:wght@400;600&display=swap">
<style>
{css}
/* ---- viewer (only in this standalone file) ---- */
html, body {{ margin: 0; height: 100%; background: #0E1424; overflow: hidden; }}
#stage {{ position: absolute; left: 50%; top: 50%; width: 1920px; height: 1080px; transform-origin: center center; }}
#stage > section {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
#stage > section:not(.active) {{ display: none; }}
#stage h1, #stage h2, #stage h3, #stage p {{ margin: 0; }}
#stage aside {{ display: none; }}
.tbl {{ border-collapse: collapse; }}
.tbl th, .tbl td {{ text-align: left; vertical-align: top; padding: 18px 16px; border-bottom: 1px solid #D6D3CA; }}
.tbl th {{ color: #15203B; font-weight: 600; }}
#counter {{ position: fixed; right: 16px; bottom: 10px; font: 14px Arial, sans-serif; color: #8A90A0; }}
#notes {{ position: fixed; left: 0; right: 0; bottom: 0; max-height: 40%; overflow: auto; display: none;
          background: rgba(14,20,36,.95); color: #E8EAF0; font: 20px/1.45 Arial, sans-serif; padding: 18px 28px; }}
@media print {{
  @page {{ size: 1920px 1080px; margin: 0; }}
  html, body {{ height: auto; overflow: visible; background: none; }}
  #stage {{ position: static; transform: none !important; width: 1920px; height: auto; }}
  #stage > section {{ position: relative; display: flex !important; break-after: page; }}
  #counter, #notes {{ display: none !important; }}
}}
</style>
</head>
<body>
<div id="stage">
{slides}
</div>
<div id="counter"></div>
<div id="notes"></div>
<script>
const stage = document.getElementById('stage');
const slides = [...stage.querySelectorAll(':scope > section')];
const counter = document.getElementById('counter'), notes = document.getElementById('notes');
let i = Math.max(0, Math.min(slides.length - 1, (parseInt(location.hash.slice(1)) || 1) - 1));
function fit() {{ const s = Math.min(innerWidth / 1920, innerHeight / 1080); stage.style.transform = `translate(-50%, -50%) scale(${{s}})`; }}
function show(n) {{
  i = Math.max(0, Math.min(slides.length - 1, n));
  slides.forEach((s, k) => s.classList.toggle('active', k === i));
  counter.textContent = `${{i + 1}} / ${{slides.length}}  ·  ←/→ navigate · N notes · F full screen`;
  const a = slides[i].querySelector('aside'); notes.textContent = a ? a.textContent : '';
  history.replaceState(null, '', '#' + (i + 1));
}}
addEventListener('resize', fit);
addEventListener('keydown', e => {{
  if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(e.key)) show(i + 1);
  else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) show(i - 1);
  else if (e.key === 'Home') show(0);
  else if (e.key === 'End') show(slides.length - 1);
  else if (e.key.toLowerCase() === 'n') notes.style.display = notes.style.display === 'block' ? 'none' : 'block';
  else if (e.key.toLowerCase() === 'f') (document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen());
}});
stage.addEventListener('click', () => show(i + 1));
fit(); show(i);
</script>
</body>
</html>
"""
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html, encoding="utf-8")
print("ok", out, len(meta["order"]), "slides")
