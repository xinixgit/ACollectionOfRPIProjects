import socketserver
import json
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
            self.cam = ctx.cam
            super().__init__(*args, **kwargs)

        def do_GET(self):
            if self.path == '/feeds':
                self.feedRequestHelper.get_feeds(reqHandler=self)
            elif self.path == '/stream.mjpg':
                self.cameraRequestHelper.get_camera_stream(reqHandler=self)
            else:
                self.send_error(404)
                self.send_standard_header()

        def do_POST(self):
            if self.path == '/feed':
                self.ctx.feeder.feed(1)
                self.send_response(200)
                self.send_standard_header(content_type='application/json')
            elif self.path == '/feeds':
                payload = self.rfile.read(int(self.headers['Content-Length']))
                objList = json.loads(payload)
                self.feedRequestHelper.save_feeds(objList=objList, reqHandler=self)
                self.send_response(200)
            elif self.path == '/cam/start':
                self.cam.start_recording()
                self.send_response(200)
                self.send_standard_header()
            elif self.path == '/cam/stop':
                self.cam.stop_recording()
                self.send_response(200)
                self.send_standard_header()
            else:
                self.send_error(404)

        def send_standard_header(self, content_type = 'text/html'):
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Content-Type', content_type + '; charset=utf-8')
            self.end_headers()
