import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import check

GOOD = ('<!DOCTYPE html><html><head><title>A</title><meta name="description" content="d">'
        '<link rel="canonical" href="https://x/a"></head><body>'
        '<a href="/b#sec">b</a><a href="https://ext/">e</a><img src="img/p.png"><h2 id="here">h</h2></body></html>')
B = ('<!DOCTYPE html><html><head><title>B</title><meta name="description" content="d">'
     '<link rel="canonical" href="https://x/b"></head><body><h2 id="sec">s</h2><a href="/a#here">a</a><!-- DRAFT -->new<!-- /DRAFT --></body></html>')

def site(d, sitemap=True):
    os.makedirs(os.path.join(d, 'img'))
    open(os.path.join(d, 'img', 'p.png'), 'wb').write(b'x')
    open(os.path.join(d, 'a.html'), 'w').write(GOOD)
    open(os.path.join(d, 'b.html'), 'w').write(B)
    if sitemap:
        open(os.path.join(d, 'sitemap.xml'), 'w').write('<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/b</loc></url></urlset>')

class CheckTest(unittest.TestCase):
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
            open(os.path.join(d, 'c.html'), 'w').write('<html><head></head><body><a href="/nope">x</a><a href="/a#missing">y</a><img src="img/no.png"></body></html>')
            open(os.path.join(d, 'sitemap.xml'), 'w').write('<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/b</loc></url><url><loc>https://x/c</loc></url></urlset>')
            p = '\n'.join(check.problems(d))
            for needle in ('c.html: missing <title>', 'c.html: missing meta description', 'c.html: missing canonical',
                           'c.html: broken link /nope', 'c.html: missing anchor /a#missing', 'c.html: missing file img/no.png'):
                self.assertIn(needle, p)

    def test_sitemap_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            open(os.path.join(d, 'sitemap.xml'), 'w').write('<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/zzz</loc></url></urlset>')
            p = '\n'.join(check.problems(d))
            self.assertIn('sitemap.xml: missing page /b', p)
            self.assertIn('sitemap.xml: unknown page /zzz', p)

    def test_404_is_not_required_in_sitemap(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            open(os.path.join(d, '404.html'), 'w').write(GOOD.replace('/b#sec', '/a#here'))
            self.assertEqual(check.problems(d), [])

if __name__ == '__main__':
    unittest.main()
