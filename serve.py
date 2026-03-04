#!/usr/bin/env python3
"""Simple HTTP server that serves testpage.html at the root path.

Run this script from the workspace root. Browsing to http://localhost:8000/ will return
`testpage.html` instead of the default `index.html`. Other files are served normally.
"""

import http.server
import socketserver
import os

PORT = 8000

class FrontPageHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # if root requested, serve testpage.html explicitly
        if self.path == '/' or self.path == '/index.html':
            self.path = '/testpage.html'
        return super().do_GET()

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))  # serve from script directory
    with socketserver.TCPServer(('localhost', PORT), FrontPageHandler) as httpd:
        print(f"Serving on http://localhost:{PORT}/ (front page = testpage.html)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server")
            httpd.server_close()
