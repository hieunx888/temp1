import http.server
import socketserver

PORT = 8080

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        html_path = "web/index.html"
        try:
            with open(html_path, "rb") as file:
                content = file.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)

        except IOError:
            self.send_error(404, "File not found")
    
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Server started on port {PORT}. Press Ctrl+C to stop.")
    httpd.serve_forever()
