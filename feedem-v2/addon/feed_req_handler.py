from http import server
from json import JSONEncoder
import json

class DefaultJsonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class FeedRequestHandler:
    def __init__(self, dbRepo, reqHandler: server.BaseHTTPRequestHandler):
        self.dbRepo = dbRepo
        self.reqHandler = reqHandler

    def get_feed(self):
        scheduled_feeds = self.dbRepo.get_scheduled_feeds()
        payload = json.dumps(scheduled_feeds, cls=DefaultJsonEncoder)

        self.reqHandler.send_response(200)
        self.reqHandler.send_header('Content-Type', 'application/json')
        self.reqHandler.end_headers()
        self.reqHandler.wfile.write(bytes(payload, "utf-8"))
