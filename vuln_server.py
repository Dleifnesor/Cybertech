#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import subprocess

class VulnerableHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Home page
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''
            <html>
            <head><title>Vulnerable Ping Service</title></head>
            <body>
                <h1>Network Ping Utility</h1>
                <p>Enter an IP address or hostname to ping:</p>
                <form action="/ping" method="GET">
                    <input type="text" name="host" placeholder="127.0.0.1">
                    <input type="submit" value="Ping">
                </form>
            </body>
            </html>
            '''
            self.wfile.write(html.encode())
        
        # Vulnerable ping endpoint
        elif parsed_path.path == '/ping':
            query = urllib.parse.parse_qs(parsed_path.query)
            host = query.get('host', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            if host:
                # VULNERABLE: Direct command injection - DO NOT USE IN PRODUCTION
                try:
                    # This is intentionally vulnerable for educational purposes
                    result = subprocess.check_output(
                        f'ping -c 4 {host}', 
                        shell=True, 
                        stderr=subprocess.STDOUT,
                        timeout=10
                    )
                    output = result.decode()
                except subprocess.TimeoutExpired:
                    output = "Ping timed out"
                except Exception as e:
                    output = f"Error: {str(e)}"
                
                html = f'''
                <html>
                <head><title>Ping Results</title></head>
                <body>
                    <h1>Ping Results</h1>
                    <pre>{output}</pre>
                    <p><a href="/">Back</a></p>
                </body>
                </html>
                '''
                self.wfile.write(html.encode())
            else:
                self.wfile.write(b'<html><body><h1>No host specified</h1><a href="/">Back</a></body></html>')
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Log requests
        print(f"{self.address_string()} - {format % args}")

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, VulnerableHandler)
    print(f'[*] Starting vulnerable web server on port {port}...')
    print(f'[*] Access it at: http://localhost:{port}')
    print('[!] WARNING: This server is intentionally vulnerable for educational purposes only!')
    print('[!] Only run this on isolated lab networks!')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
