#!/usr/bin/env python3
"""Static checks for the site. Stdlib only.

    python3 tools/check.py            # links, images, anchors, metadata, sitemap
    python3 tools/check.py --strict   # also fail on any <!-- DRAFT --> marker
Exit 1 and one line per problem when anything is wrong.
"""
import glob, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs, self.srcs, self.ids = [], [], set()
        self.title = self.description = self.canonical = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag == 'a' and a.get('href'): self.hrefs.append(a['href'])
        if tag in ('img', 'script', 'source') and a.get('src'): self.srcs.append(a['src'])
        if tag == 'link':
            rel = (a.get('rel') or '').lower().split()
            if a.get('href'):
                if 'canonical' in rel: self.canonical = True
                if {'stylesheet', 'icon', 'apple-touch-icon', 'preload'} & set(rel): self.srcs.append(a['href'])
        if tag == 'meta' and a.get('name') == 'description' and a.get('content'): self.description = True
        if tag == 'title': self.title = True

def read(path):
    with open(path, encoding='utf-8') as f: return f.read()

def scan(path):
    s = Scan(); s.feed(read(path)); return s

def page_for(root, url_path):
    """'/about' -> about.html, '/' -> index.html, '/x/' -> x/index.html; None if absent."""
    p = url_path.strip('/')
    cands = [os.path.join(root, 'index.html')] if p == '' else [os.path.join(root, p + '.html'), os.path.join(root, p, 'index.html'), os.path.join(root, p)]
    for c in cands:
        if os.path.isfile(c): return c
    return None

def problems(root=ROOT, strict=False):
    out = []
    pages = sorted(glob.glob(os.path.join(root, '*.html')) + glob.glob(os.path.join(root, 'research', '*.html')))
    scans = {p: scan(p) for p in pages}
    for p in pages:
        name = os.path.relpath(p, root).replace(os.sep, '/'); s = scans[p]
        if not s.title: out.append('%s: missing <title>' % name)
        if not s.description: out.append('%s: missing meta description' % name)
        if not s.canonical: out.append('%s: missing canonical' % name)
        if strict and '<!-- DRAFT -->' in read(p): out.append('%s: DRAFT marker present' % name)
        for h in s.hrefs:
            if re.match(r'^(https?:|mailto:|tel:|data:|javascript:)', h, re.I): continue
            if h.startswith('#'):
                if h[1:] and h[1:] not in s.ids: out.append('%s: missing anchor %s' % (name, h))
                continue
            if h.startswith('/'):
                path, _, frag = h.partition('#')
                path = path.partition('?')[0]
                target = page_for(root, path)
                if not target: out.append('%s: broken link %s' % (name, h)); continue
                if frag and target.endswith('.html') and frag not in (scans.get(target) or scan(target)).ids:
                    out.append('%s: missing anchor %s' % (name, h))
                continue
            if not os.path.isfile(os.path.join(root, re.split(r'[?#]', h)[0])): out.append('%s: missing file %s' % (name, h))
        for src in s.srcs:
            if re.match(r'^(https?:|//)', src, re.I): out.append('%s: external resource %s' % (name, src)); continue
            if re.match(r'^data:', src, re.I): continue
            rel = re.split(r'[?#]', src)[0].lstrip('/')
            if not os.path.isfile(os.path.join(root, rel)): out.append('%s: missing file %s' % (name, src))
    sm = os.path.join(root, 'sitemap.xml')
    if os.path.isfile(sm):
        locs = re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', read(sm))
        listed = set(re.sub(r'^https?://[^/]+', '', l).rstrip('/') or '/' for l in locs)
        def clean(p):
            rel = os.path.relpath(p, root)[:-5].replace(os.sep, '/')
            return '/' if rel == 'index' else '/' + rel
        expected = set(clean(p) for p in pages if os.path.basename(p) != '404.html')
        for miss in sorted(expected - listed): out.append('sitemap.xml: missing page %s' % miss)
        for extra in sorted(listed - expected): out.append('sitemap.xml: unknown page %s' % extra)
    return out

if __name__ == '__main__':
    probs = problems(strict='--strict' in sys.argv)
    for line in probs: print(line)
    print('check: %d problem(s)' % len(probs))
    sys.exit(1 if probs else 0)
