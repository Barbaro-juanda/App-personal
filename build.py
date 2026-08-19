#!/usr/bin/env python3
"""Genera index.html autocontenido a partir de 'App Habitos y Finanzas.dc.html'.

Embebe React, React-DOM, el runtime (src/support.js) y las fuentes IBM Plex Sans
como data: URIs, para que el archivo abra sin servidor ni red.
Los scripts van como src="data:..." a proposito: React-DOM minificado contiene
un '</script>' literal que romperia el parseo si se inyectara en linea.
"""
import base64, pathlib, re, urllib.request

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "App Habitos y Finanzas.dc.html"
CDN = {
    "https://unpkg.com/react@18.3.1/umd/react.production.min.js": None,
    "https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js": None,
}
CACHE = ROOT / ".build-cache"


def fetch(url):
    CACHE.mkdir(exist_ok=True)
    f = CACHE / re.sub(r"\W+", "_", url)
    if not f.exists():
        f.write_bytes(urllib.request.urlopen(url).read())
    return f.read_bytes()


def durl(mime, raw):
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode())


html = SRC.read_text(encoding="utf-8")

# runtime + react/react-dom embebidos
tags = "".join(
    '<script src="%s"></script>\n' % durl("text/javascript", fetch(u)) for u in CDN
)
tags += '<script src="%s"></script>' % durl(
    "text/javascript", (ROOT / "src" / "support.js").read_bytes()
)
html = re.sub(
    r'<script src="https://unpkg\.com/react[^>]*></script>\s*'
    r'<script src="https://unpkg\.com/react-dom[^>]*></script>\s*'
    r'<script src="src/support\.js"></script>',
    lambda _: tags,
    html,
)

# fuentes: descarga el CSS de Google y embebe cada woff2
css_url = re.search(r'href="(https://fonts\.googleapis\.com/css2[^"]*)"', html).group(1)
req = urllib.request.Request(css_url, headers={"User-Agent": "Mozilla/5.0"})
CACHE.mkdir(exist_ok=True)
cf = CACHE / "fonts.css"
if not cf.exists():
    cf.write_bytes(urllib.request.urlopen(req).read())
css = cf.read_text()
for fu in sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css))):
    css = css.replace(fu, durl("font/woff2", fetch(fu)))
html = re.sub(
    r'<link rel="preconnect"[^>]*>\s*<link rel="preconnect"[^>]*>\s*'
    r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2[^"]*">',
    lambda _: "<style>%s</style>" % css,
    html,
)

assert "unpkg.com" not in html and "fonts.gstatic.com" not in html, "quedaron refs externas"
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("index.html generado:", len(html), "bytes")
