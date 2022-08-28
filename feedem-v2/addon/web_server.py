from http import server
from functools import partial
from threading import Thread

from .feed_req_handler import FeedRequestHandler

class RequestHandler(server.BaseHTTPRequestHandler):
    def __init__(self, dbRepo, *args, **kwargs):
        self.feedRequestHandler = FeedRequestHandler(dbRepo, self)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/feed':
            self.feedRequestHandler.get_feed()

class WebServer:
    def __init__(self, dbRepo):
        address = ('', 8001)
        handler = partial(RequestHandler, dbRepo)
        self.server = server.HTTPServer(address, handler)
    
    def start(self):
        thread = Thread(target=self.server.serve_forever)
        thread.start()
        print("web server started")

    def stop(self):
        self.server.server_close()
        print("web server stopped")