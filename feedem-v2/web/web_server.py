import socketserver
import json
from http import server
from functools import partial
from threading import Thread
from gpiozero import LED
import logging

from db import repo
from feeder.feeder import Feeder
from .feed_request_helper import FeedRequestHelper
from .event_listener import EventListener
from .camera_streamer import CameraStreamer


class RequestHandlerContext:
    def __init__(
            self,
            dbRepo: repo.DBRepo,
            cam: CameraStreamer,
            feeder: Feeder,
            event_listener: EventListener,
            led: LED,
    ):
        self.dbRepo = dbRepo
        self.cam = cam
        self.feeder = feeder
        self.event_listener = event_listener
        self.led = led


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
            super().__init__(*args, **kwargs)

        def do_GET(self):
            if self.path == '/feeds':
                self.feedRequestHelper.get_feeds(reqHandler=self)
            elif self.path == '/stream.mjpg':
                self.get_camera_stream()
            else:
                self.send_error(404)
                self.send_standard_header()

        def do_POST(self):
            if self.path == '/feed':
                self.ctx.feeder.feed(1)
                self.ctx.event_listener.publish_portion_fed(1)
                self.send_response(200)
                self.send_standard_header(content_type='application/json')
            elif self.path == '/feeds':
                payload = self.rfile.read(int(self.headers['Content-Length']))
                objList = json.loads(payload)
                self.feedRequestHelper.save_feeds(
                    objList=objList, reqHandler=self)
                self.send_response(200)
            elif self.path == '/cam/start':
                self.ctx.led.on()
                self.ctx.cam.start_recording()
                self.send_response(200)
                self.send_standard_header()
            elif self.path == '/cam/stop':
                self.ctx.led.off()
                self.ctx.cam.stop_recording()
                self.send_response(200)
                self.send_standard_header()
            else:
                self.send_error(404)

        def get_camera_stream(self):
            output = self.ctx.cam.get_output()

            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header(
                'Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    f"Removed streaming client {self.client_address}: {str(e)}")

        def send_standard_header(self, content_type='text/html'):
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Content-Type', content_type + '; charset=utf-8')
            self.end_headers()
