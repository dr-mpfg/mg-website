import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import chrome

NAV = '<nav><a class="nav__link" href="/research">Research</a><a class="btn nav__cta" href="/advisory">Advisory</a></nav>'
FOOT = '<footer>f</footer>'
PAGE = ('<html><body>\n<!-- CHROME:nav -->\nOLD NAV\n<!-- /CHROME:nav -->\n<main>x</main>\n'
        '<!-- CHROME:footer -->OLD FOOT<!-- /CHROME:footer -->\n</body></html>')

class ChromeTest(unittest.TestCase):
    def test_page_path(self):
        self.assertEqual(chrome.page_path('index.html'), '/')
        self.assertEqual(chrome.page_path('about.html'), '/about')
        self.assertIsNone(chrome.page_path('404.html'))

    def test_mark_current_sets_aria_current_on_matching_link_only(self):
        out = chrome.mark_current(NAV, '/research')
        self.assertIn('href="/research" aria-current="page"', out)
        self.assertNotIn('href="/advisory" aria-current', out)

    def test_mark_current_handles_cta_and_none(self):
        self.assertIn('href="/advisory" aria-current="page"', chrome.mark_current(NAV, '/advisory'))
        self.assertEqual(chrome.mark_current(NAV, None), NAV)

    def test_render_replaces_both_blocks(self):
        out = chrome.render(PAGE, NAV, FOOT, '/research')
        self.assertNotIn('OLD NAV', out); self.assertNotIn('OLD FOOT', out)
        self.assertIn('<!-- CHROME:nav -->\n<nav>', out)
        self.assertIn('<footer>f</footer>\n<!-- /CHROME:footer -->', out)
        self.assertIn('aria-current="page"', out)

    def test_render_raises_when_markers_missing(self):
        with self.assertRaises(chrome.MissingMarker):
            chrome.render('<html></html>', NAV, FOOT, '/')

    def test_run_rewrites_files_in_root(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, 'tools', 'chrome'))
            open(os.path.join(d, 'tools', 'chrome', 'nav.html'), 'w').write(NAV)
            open(os.path.join(d, 'tools', 'chrome', 'footer.html'), 'w').write(FOOT)
            open(os.path.join(d, 'research.html'), 'w').write(PAGE)
            changed = chrome.run(d)
            self.assertEqual(changed, ['research.html'])
            self.assertIn('aria-current="page"', open(os.path.join(d, 'research.html')).read())
            self.assertEqual(chrome.run(d), [])  # idempotent

if __name__ == '__main__':
    unittest.main()
