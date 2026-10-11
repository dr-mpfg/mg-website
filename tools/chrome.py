#!/usr/bin/env python3
"""Write the shared nav and footer into every page. Stdlib only.

    python3 tools/chrome.py          # rewrites *.html in the repo root, prints the files changed

Pages carry two marker pairs:  <!-- CHROME:nav --> ... <!-- /CHROME:nav -->
and                            <!-- CHROME:footer --> ... <!-- /CHROME:footer -->
Sources: tools/chrome/nav.html and tools/chrome/footer.html. The nav link whose
href equals the page's clean URL gets aria-current="page".
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MissingMarker(Exception):
    pass

def page_path(filename):
    """index.html -> '/', about.html -> '/about', 404.html -> None."""
    name = os.path.basename(filename)[:-5]
    if name == 'index':
        return '/'
    if name == '404':
        return None
    return '/' + name

def mark_current(nav_html, path):
    if path is None:
        return nav_html
    return re.sub(r'href="%s"(?! aria-current)' % re.escape(path), 'href="%s" aria-current="page"' % path, nav_html)

def _block(name):
    return re.compile(r'(<!-- CHROME:%s -->)(.*?)(<!-- /CHROME:%s -->)' % (name, name), re.S)

def render(page_html, nav_html, footer_html, path):
    out = page_html
    for name, body in (('nav', mark_current(nav_html, path)), ('footer', footer_html)):
        pat = _block(name)
        if not pat.search(out):
            raise MissingMarker('missing CHROME:%s markers' % name)
        out = pat.sub(lambda m, b=body: m.group(1) + '\n' + b.strip() + '\n' + m.group(3), out, count=1)
    return out

def run(root=ROOT):
    nav = open(os.path.join(root, 'tools', 'chrome', 'nav.html'), encoding='utf-8').read()
    foot = open(os.path.join(root, 'tools', 'chrome', 'footer.html'), encoding='utf-8').read()
    changed = []
    for p in sorted(glob.glob(os.path.join(root, '*.html'))):
        src = open(p, encoding='utf-8').read()
        out = render(src, nav, foot, page_path(p))
        if out != src:
            open(p, 'w', encoding='utf-8').write(out)
            changed.append(os.path.basename(p))
    return changed

if __name__ == '__main__':
    for f in run():
        print('updated', f)
    sys.exit(0)
