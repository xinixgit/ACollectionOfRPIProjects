import socketserver
from http import server
from functools import partial
from threading import Thread

from ..db import repo
from ..feeder import Feeder
from .feed_request_helper import FeedRequestHelper
from .cam_request_helper import CameraRequestHelper, CameraStreamer

class RequestHandlerContext:
    def __init__(self, dbRepo: repo.DBRepo, cam: CameraStreamer, feeder: Feeder):
        self.dbRepo = dbRepo
        self.cam = cam
        self.feeder = feeder

class WebServer:
    def __init__(self, ctx: RequestHandlerContext):
        address = ('', 8000)
        handler = partial(self.RequestHandler, ctx)
        self.server = self.MultiTheadSockerServer(address, handler)
    
    def start(self):
        thread = Thread(target=self.server.serve_forever)
        thread.start()
        print("web server started")

    def stop(self):
        self.server.server_close()
        print("web server stopped")

    class MultiTheadSockerServer(socketserver.ThreadingMixIn, server.HTTPServer):
        allow_reuse_address = True
        daemon_threads = True

    class RequestHandler(server.BaseHTTPRequestHandler):
        def __init__(self, ctx: RequestHandlerContext, *args, **kwargs):
            self.ctx = ctx
            self.feedRequestHelper = FeedRequestHelper(dbRepo=ctx.dbRepo)
            self.cameraRequestHelper = CameraRequestHelper(cam=ctx.cam)
            super().__init__(*args, **kwargs)

        def do_GET(self):
            if self.path == '/feed':
                self.feedRequestHelper.get_feed(reqHandler=self)
            elif self.path == '/stream.mjpg':
                self.cameraRequestHelper.get_camera_stream(reqHandler=self)
            else:
                self.send_error(404)
                self.end_headers()

        def do_POST(self):
            if self.path == '/feed':
                self.ctx.feeder.feed(1)
