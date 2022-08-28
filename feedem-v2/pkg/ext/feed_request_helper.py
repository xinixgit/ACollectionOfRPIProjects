from http import server
from json import JSONEncoder
from ..domain import config
from ..db import repo
import json

class FeedRequestHelper:
    def __init__(self, dbRepo: repo.DBRepo):
        self.dbRepo = dbRepo

    def get_feed(self, reqHandler: server.BaseHTTPRequestHandler):
        scheduled_feeds = self.dbRepo.get_scheduled_feeds()
        payload = json.dumps(scheduled_feeds, cls=self.DefaultJsonEncoder)

        reqHandler.send_response(200)
        reqHandler.send_header('Content-Type', 'application/json')
        reqHandler.end_headers()
        reqHandler.wfile.write(bytes(payload, "utf-8"))

    def save_feed(self, objList, reqHandler: server.BaseHTTPRequestHandler):
        feeds = []
        for obj in objList:
            feeds.append(config.ScheduledFeed(int(obj['hr']), int(obj['min']), int(obj['portion'])))

        self.dbRepo.overwrite_scheduled_feeds(feeds)
        reqHandler.send_response(200)

    class DefaultJsonEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
