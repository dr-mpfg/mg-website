#!/usr/bin/env python3
"""Flip search-engine indexing for the whole site in one go. Stdlib only.

    python3 tools/indexing.py on      # launch: remove noindex, robots.txt Allow: /
    python3 tools/indexing.py off     # back to noindex + Disallow: /
    python3 tools/indexing.py         # show current state
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFF = '<!-- ROBOTS:off --><meta name="robots" content="noindex, nofollow"><!-- /ROBOTS -->'
ON = '<!-- ROBOTS:on --><!-- /ROBOTS -->'
BLOCK = re.compile(r'<!-- ROBOTS:(on|off) -->.*?<!-- /ROBOTS -->', re.S)

def pages():
    return sorted(glob.glob(os.path.join(ROOT, '*.html')))

def state():
    out = {}
    for p in pages():
        m = BLOCK.search(open(p, encoding='utf-8').read())
        out[os.path.basename(p)] = m.group(1) if m else 'MISSING'
    r = open(os.path.join(ROOT, 'robots.txt'), encoding='utf-8').read()
    out['robots.txt'] = 'on' if re.search(r'^Allow: /\s*$', r, re.M) else 'off'
    c = open(os.path.join(ROOT, 'js/config.js'), encoding='utf-8').read()
    out['config.js'] = 'on' if re.search(r'INDEXING:\s*true', c) else 'off'
    return out

def set_state(on):
    for p in pages():
        s = open(p, encoding='utf-8').read()
        s2 = BLOCK.sub(ON if on else OFF, s)
        if s2 != s:
            open(p, 'w', encoding='utf-8').write(s2)
    rp = os.path.join(ROOT, 'robots.txt')
    open(rp, 'w', encoding='utf-8').write(
        '# Managed by tools/indexing.py\nUser-agent: *\n' + ('Allow: /\n' if on else 'Disallow: /\n')
        + 'Sitemap: https://mg-macro.vercel.app/sitemap.xml\n')
    cp = os.path.join(ROOT, 'js/config.js')
    c = open(cp, encoding='utf-8').read()
    open(cp, 'w', encoding='utf-8').write(re.sub(r'INDEXING:\s*(true|false)', 'INDEXING: ' + ('true' if on else 'false'), c))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('on', 'off'):
        set_state(sys.argv[1] == 'on')
    for k, v in state().items():
        print(f'{k:14s} {v}')
