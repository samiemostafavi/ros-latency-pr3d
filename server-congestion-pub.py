# pip3 install HTTPServer
# pip3 install python-daemon

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import subprocess
import json
import daemon

class MyHttpRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        # create and send headers                                                                                                                                                                                                      
        self.send_response(200)                                                                                                                                                                                                        
        self.send_header('Content-type', 'application/json')                                                                                                                                                                           
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
	    # get resuls
        command = "ifstat -i net1 1 1 | awk 'NR==3 {print $1, $2}'"
        try:
            res = subprocess.check_output(command, shell=True, text=True).strip()
        except subprocess.CalledProcessError as e:
            res = f"ERROR_{e}"
        
        # Create a JSON response
        response = json.dumps({"result": res})
        
        # Write the response
        self.wfile.write(response.encode('utf-8'))

if __name__ == "__main__":
    from sys import argv

    port = 50123

    server_address = ('', port)                        
    server = HTTPServer(server_address, MyHttpRequestHandler)

    # Make the context manager for becoming a daemon process.
    daemon_context = daemon.DaemonContext()
    daemon_context.files_preserve = [server.fileno()]

    # Become a daemon process.
    with daemon_context:
        server.serve_forever()
