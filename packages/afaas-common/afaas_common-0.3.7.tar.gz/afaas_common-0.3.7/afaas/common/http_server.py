""" Simple http server to expose healthz and some basic introspection for the MSA/Fold servers """
import http.server
import socketserver
import threading

from google.cloud import firestore
from google import auth


class Handler(http.server.BaseHTTPRequestHandler):
    """ Handles incoming HTTP GET requests. """

    def __init__(self, *args, **kwargs):
        creds, project_id = auth.default()
        self.db_client = firestore.Client(credentials=creds, project=project_id)
        super().__init__(*args, **kwargs)

    def do_HEAD(self):
        self.send_response(200)

    def do_GET(self):
        if self.path == '/healthz':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('OK'.encode('UTF-8'))
        elif self.path == '/cache':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('No cache.'.encode('UTF-8'))
        elif self.path == '/localcache':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('No local cache.'.encode('UTF-8'))
            return


def _run_http_server(port: int):
    httpd = socketserver.TCPServer(('', port), Handler)
    httpd.serve_forever()


def start_daemon(port: int):
    http_thread = threading.Thread(name='http_server', target=_run_http_server, args=(port,))
    http_thread.setDaemon(True)
    http_thread.start()
