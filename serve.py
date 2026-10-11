#!/usr/bin/env python3
"""Local dev server. Stdlib only, no dependencies.

Mimics the Vercel config: clean URLs (/privacy -> privacy.html) and the
same security headers, so a strict CSP failure shows up locally.

    python3 serve.py            # http://localhost:8765
    python3 serve.py 3000
"""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT, "vercel.json"), encoding="utf-8") as f:
    VERCEL = json.load(f)
HEADERS = [(h["key"], h["value"]) for rule in VERCEL.get("headers", [])
           if rule["source"] == "/(.*)" for h in rule["headers"]]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def translate_path(self, path):
        full = super().translate_path(path)
        clean = path.split("?", 1)[0].split("#", 1)[0]
        if not os.path.exists(full) and not clean.endswith("/"):
            candidate = full + ".html"
            if os.path.isfile(candidate):
                return candidate
        return full

    def end_headers(self):
        for key, value in HEADERS:
            self.send_header(key, value)
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        """Serve 404.html for missing paths, as Vercel does."""
        page = os.path.join(ROOT, "404.html")
        if code == 404 and os.path.isfile(page):
            body = open(page, "rb").read()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.log_date_time_string(), fmt % args))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"Serving {ROOT} at http://localhost:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
