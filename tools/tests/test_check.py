import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import check

GOOD = ('<!DOCTYPE html><html><head><title>A</title><meta name="description" content="d">'
        '<link rel="canonical" href="https://x/a"></head><body>'
        '<a href="/b#sec">b</a><a href="https://ext/">e</a><img src="img/p.png"><h2 id="here">h</h2></body></html>')
B = ('<!DOCTYPE html><html><head><title>B</title><meta name="description" content="d">'
     '<link rel="canonical" href="https://x/b"></head><body><h2 id="sec">s</h2><a href="/a#here">a</a><!-- DRAFT -->new<!-- /DRAFT --></body></html>')

def write(path, text, mode='w'):
    with open(path, mode) as f: f.write(text)

def page(body, head='<link rel="canonical" href="https://x/c">'):
    return '<html><head><title>C</title><meta name="description" content="d">%s</head><body>%s</body></html>' % (head, body)

def site(d, sitemap=True):
    os.makedirs(os.path.join(d, 'img'))
    write(os.path.join(d, 'img', 'p.png'), b'x', 'wb')
    write(os.path.join(d, 'a.html'), GOOD)
    write(os.path.join(d, 'b.html'), B)
    if sitemap:
        write(os.path.join(d, 'sitemap.xml'), '<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/b</loc></url></urlset>')

class CheckTest(unittest.TestCase):
    def test_research_subpages_are_scanned_and_expected_in_sitemap(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            os.makedirs(os.path.join(d, 'research'))
            write(os.path.join(d, 'research', 'eurozone.html'), GOOD.replace('/b#sec', '/a#here').replace('https://x/a', 'https://x/research/eurozone'))
            p = '\n'.join(check.problems(d))
            self.assertIn('sitemap.xml: missing page /research/eurozone', p)
            write(os.path.join(d, 'sitemap.xml'), '<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/b</loc></url><url><loc>https://x/research/eurozone</loc></url></urlset>')
            self.assertEqual(check.problems(d), [])
            write(os.path.join(d, 'research', 'bad.html'), '<html><head></head><body><a href="/nope">x</a></body></html>')
            self.assertIn('research/bad.html: broken link /nope', '\n'.join(check.problems(d)))

    def test_clean_site_has_no_problems(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            self.assertEqual(check.problems(d), [])

    def test_strict_reports_draft_markers(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            p = check.problems(d, strict=True)
            self.assertEqual(len(p), 1); self.assertIn('b.html: DRAFT', p[0])

    def test_broken_link_image_anchor_and_meta(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            write(os.path.join(d, 'c.html'), '<html><head></head><body><a href="/nope">x</a><a href="/a#missing">y</a><img src="img/no.png"></body></html>')
            write(os.path.join(d, 'sitemap.xml'), '<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/b</loc></url><url><loc>https://x/c</loc></url></urlset>')
            p = '\n'.join(check.problems(d))
            for needle in ('c.html: missing <title>', 'c.html: missing meta description', 'c.html: missing canonical',
                           'c.html: broken link /nope', 'c.html: missing anchor /a#missing', 'c.html: missing file img/no.png'):
                self.assertIn(needle, p)

    def test_sitemap_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            write(os.path.join(d, 'sitemap.xml'), '<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/zzz</loc></url></urlset>')
            p = '\n'.join(check.problems(d))
            self.assertIn('sitemap.xml: missing page /b', p)
            self.assertIn('sitemap.xml: unknown page /zzz', p)

    def test_404_is_not_required_in_sitemap(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            write(os.path.join(d, '404.html'), GOOD.replace('/b#sec', '/a#here'))
            self.assertEqual(check.problems(d), [])

    def c_problems(self, body, head='<link rel="canonical" href="https://x/c">', sitemap=True):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            write(os.path.join(d, 'c.html'), page(body, head))
            write(os.path.join(d, 'sitemap.xml'), '<urlset>' + ''.join('<url><loc>https://x/%s</loc></url>' % n for n in 'abc') + '</urlset>')
            return check.problems(d)

    def test_multi_token_rel(self):
        self.assertEqual(self.c_problems('', '<link rel="Canonical nofollow" href="https://x/c">'), [])

    def test_preload_and_icon_missing_files(self):
        p = self.c_problems('', '<link rel="canonical" href="https://x/c"><link rel="preload" href="/fonts/nope.woff2" as="font"><link rel="icon" href="/f.ico">')
        self.assertEqual(p, ['c.html: missing file /fonts/nope.woff2', 'c.html: missing file /f.ico'])

    def test_sitemap_trailing_slash(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            write(os.path.join(d, 'sitemap.xml'), '<urlset><url><loc>https://x/a/</loc></url><url><loc>https://x/b</loc></url></urlset>')
            self.assertEqual(check.problems(d), [])

    def test_query_and_fragment_on_src_and_href(self):
        self.assertEqual(self.c_problems('<img src="img/p.png?v=2"><img src="img/p.png#x"><a href="/a?x=1#here">a</a><a href="/a?x=1">a</a>'), [])

    def test_external_resources(self):
        p = self.c_problems('<script src="https://cdn.example/x.js"></script><script src="//cdn.example/y.js"></script><img src="HTTPS://cdn.example/z.png">',
                            '<link rel="canonical" href="https://x/c"><link rel="stylesheet" href="https://fonts.example/x.css">')
        self.assertEqual(sorted(p), sorted('c.html: external resource ' + u for u in
            ('https://fonts.example/x.css', 'https://cdn.example/x.js', '//cdn.example/y.js', 'HTTPS://cdn.example/z.png')))

    def test_data_and_javascript_schemes_skipped(self):
        self.assertEqual(self.c_problems('<img src="data:image/png;base64,AAAA"><a href="javascript:void(0)">j</a><a href="data:text/plain,hi">d</a><a href="HTTPS://e/">e</a>'), [])

if __name__ == '__main__':
    unittest.main()
