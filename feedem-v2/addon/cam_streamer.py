import io
import picamera
import logging
import socketserver
import time
from threading import Condition
from http import server
from threading import Thread
from functools import partial

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def __init__(self, output, *args, **kwargs):
        self.output = output
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', 'stream.mjpg')
            self.end_headers()
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with self.output.condition:
                        self.output.condition.wait()
                        frame = self.output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class CamStreamer():
    def __init__(self):
        address = ('', 8000)
        self.output = StreamingOutput()
        handler = partial(StreamingHandler, self.output)
        self.server = StreamingServer(address, handler)
        self.camera = picamera.PiCamera(resolution='800x600', framerate=24)
        self.streaming = False

    def start_recording(self):
        if not self.streaming:
            self.camera.start_recording(self.output, format='mjpeg')
            thread = Thread(target=self.server.serve_forever)
            thread.start()
            self.streaming = True
            print('camera stream started')

    def stop_recording(self):
        if self.streaming:
            self.server.shutdown()
            self.camera.stop_recording()
            self.streaming = False
            print('cam streamer stopped')
