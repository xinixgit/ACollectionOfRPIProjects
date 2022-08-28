from http import server
from json import JSONEncoder
import json

class FeedRequestHelper:
    def __init__(self, dbRepo):
        self.dbRepo = dbRepo

    def get_feed(self, reqHandler: server.BaseHTTPRequestHandler):
        scheduled_feeds = self.dbRepo.get_scheduled_feeds()
        payload = json.dumps(scheduled_feeds, cls=self.DefaultJsonEncoder)

        reqHandler.send_response(200)
        reqHandler.send_header('Content-Type', 'application/json')
        reqHandler.end_headers()
        reqHandler.wfile.write(bytes(payload, "utf-8"))

    class DefaultJsonEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
