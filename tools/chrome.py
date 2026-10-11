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

def pages(root=ROOT):
    """Sorted paths of *.html in root and in root/research/."""
    return sorted(glob.glob(os.path.join(root, '*.html')) + glob.glob(os.path.join(root, 'research', '*.html')))

def page_path(filename, root=ROOT):
    """index.html -> '/', about.html -> '/about', research/eurozone.html -> '/research/eurozone', 404.html -> None."""
    rel = os.path.relpath(filename, root)[:-5].replace(os.sep, '/')
    if rel == 'index':
        return '/'
    if rel == '404':
        return None
    return '/' + rel

def mark_current(nav_html, path):
    """Mark the link for path; project pages (/research/x) also mark their parent (/research)."""
    if path is None:
        return nav_html
    targets = [path]
    if path.startswith('/research/'):
        targets.append('/research')
    out = nav_html
    for t in targets:
        out = re.sub(r'href="%s"(?! aria-current)' % re.escape(t), 'href="%s" aria-current="page"' % t, out)
    return out

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
    with open(os.path.join(root, 'tools', 'chrome', 'nav.html'), encoding='utf-8') as f: nav = f.read()
    with open(os.path.join(root, 'tools', 'chrome', 'footer.html'), encoding='utf-8') as f: foot = f.read()
    changed = []
    for p in pages(root):
        with open(p, encoding='utf-8') as f: src = f.read()
        out = render(src, nav, foot, page_path(p, root))
        if out != src:
            with open(p, 'w', encoding='utf-8') as f: f.write(out)
            changed.append(os.path.relpath(p, root).replace(os.sep, '/'))
    return changed

if __name__ == '__main__':
    for f in run():
        print('updated', f)
    sys.exit(0)
