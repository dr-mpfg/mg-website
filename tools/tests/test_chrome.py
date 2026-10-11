import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import chrome

NAV = '<nav><a class="nav__link" href="/research">Research</a><a class="btn nav__cta" href="/advisory">Advisory</a></nav>'
FOOT = '<footer>f</footer>'
def put(path, text):
    with open(path, 'w', encoding='utf-8') as f: f.write(text)

PAGE = ('<html><body>\n<!-- CHROME:nav -->\nOLD NAV\n<!-- /CHROME:nav -->\n<main>x</main>\n'
        '<!-- CHROME:footer -->OLD FOOT<!-- /CHROME:footer -->\n</body></html>')

class ChromeTest(unittest.TestCase):
    def test_page_path(self):
        self.assertEqual(chrome.page_path('/r/index.html', '/r'), '/')
        self.assertEqual(chrome.page_path('/r/about.html', '/r'), '/about')
        self.assertIsNone(chrome.page_path('/r/404.html', '/r'))

    def test_page_path_subdirectory(self):
        self.assertEqual(chrome.page_path('/x/research/eurozone.html', '/x'), '/research/eurozone')
        self.assertEqual(chrome.page_path('/x/about.html', '/x'), '/about')

    def test_mark_current_marks_parent_for_project_pages(self):
        nav = '<a class="nav__link" href="/research">Research</a><a href="/research/eurozone">Eurozone</a><a href="/research/gegi-study">GEGI</a>'
        out = chrome.mark_current(nav, '/research/eurozone')
        self.assertIn('href="/research" aria-current="page"', out)
        self.assertIn('href="/research/eurozone" aria-current="page"', out)
        self.assertNotIn('href="/research/gegi-study" aria-current', out)

    def test_pages_includes_root_and_research(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, 'research'))
            put(os.path.join(d, 'index.html'), '')
            put(os.path.join(d, 'research', 'eurozone.html'), '')
            self.assertEqual(chrome.pages(d), [os.path.join(d, 'index.html'), os.path.join(d, 'research', 'eurozone.html')])

    def test_run_includes_research_directory(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, 'tools', 'chrome')); os.makedirs(os.path.join(d, 'research'))
            put(os.path.join(d, 'tools', 'chrome', 'nav.html'), '<a class="nav__link" href="/research">R</a>')
            put(os.path.join(d, 'tools', 'chrome', 'footer.html'), FOOT)
            put(os.path.join(d, 'research', 'eurozone.html'), PAGE)
            self.assertEqual(chrome.run(d), ['research/eurozone.html'])
            with open(os.path.join(d, 'research', 'eurozone.html'), encoding='utf-8') as f:
                self.assertIn('href="/research" aria-current="page"', f.read())

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
            put(os.path.join(d, 'tools', 'chrome', 'nav.html'), NAV)
            put(os.path.join(d, 'tools', 'chrome', 'footer.html'), FOOT)
            put(os.path.join(d, 'research.html'), PAGE)
            changed = chrome.run(d)
            self.assertEqual(changed, ['research.html'])
            with open(os.path.join(d, 'research.html'), encoding='utf-8') as f:
                self.assertIn('aria-current="page"', f.read())
            self.assertEqual(chrome.run(d), [])  # idempotent

if __name__ == '__main__':
    unittest.main()
