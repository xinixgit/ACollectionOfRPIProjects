import io
import picamera
import logging
from threading import Condition, Thread
from http import server


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


class CameraStreamer():
    def __init__(self):
        self.output = StreamingOutput()
        self.camera = picamera.PiCamera(resolution='800x600', framerate=24)
        self.camera.rotation = 180
        self.streaming = False

    def start_recording(self):
        if not self.streaming:
            self.camera.start_recording(self.output, format='mjpeg')
            self.streaming = True
            print('camera stream started')

    def stop_recording(self):
        if self.streaming:
            self.camera.stop_recording()
            self.streaming = False
            print('cam streamer stopped')

    def get_output(self):
        return self.output
