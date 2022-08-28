from http import server
from functools import partial
from threading import Thread
import json

class FeedRequestHandler:
    def __init__(self, dbRepo, reqHandler: server.BaseHTTPRequestHandler):
        self.dbRepo = dbRepo
        self.reqHandler = reqHandler

    def get_feed(self):
        scheduled_feeds = self.dbRepo.get_scheduled_feeds()
        payload = json.dumps(scheduled_feeds)

        self.reqHandler.send_response(200)
        self.reqHandler.send_header('Content-Type', 'application/json')
        self.reqHandler.end_headers()
        self.reqHandler.wfile.write(bytes(payload, "utf-8"))
