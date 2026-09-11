import os
import sys
import http.server
import socketserver
import json

PORT = 8000
PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

class CreditLensHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_GET(self):
        # REST API endpoint for system health & portfolio summary
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response_data = {
                "status": "ONLINE",
                "warehouse": "PostgreSQL 14.2",
                "records_loaded": 5800000,
                "par30": "2.40%",
                "npl": "1.10%",
                "portfolio_value": "$145.2M"
            }
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return
            
        return super().do_GET()

def run_server():
    os.chdir(PUBLIC_DIR)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CreditLensHandler) as httpd:
        print(f"CreditLens Terminal Server running on http://localhost:{PORT}")
        sys.stdout.flush()
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
