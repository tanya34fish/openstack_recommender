from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess
import cgi

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path=='/favicon.ico':
            return
        p = self.path.split("?")
        params = {}
        if len(p) > 1:
            params = cgi.parse_qs(p[1], True, True)
        commands = ['python', 'train.py']
        commands.append(params['data'])
        commands.append(params['model'])
        print commands
        # Train here
        subprocess.call(commands)

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()
