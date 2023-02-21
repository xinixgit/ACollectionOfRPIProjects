from datetime import datetime
from pkg.feeder import Feeder
from pkg.ext.web_server import WebServer, RequestHandlerContext
from pkg.ext.cam_request_helper import CameraStreamer
from pkg.ext.event_listener import EventListener
from pkg.db.repo import DBRepo
from pkg.domain.config import Config
import time
import sys

feeder = Feeder()
cam = CameraStreamer()

# try:
#     event_listener = EventListener(cam)
#     event_listener.connect(user=sys.argv[1], pwd=sys.argv[2])
# except:
#     print("Failed to start MQTT event listener")

dbRepo = DBRepo()
ctx = RequestHandlerContext(dbRepo=dbRepo, cam=cam, feeder=feeder)
webSvr = WebServer(ctx)
webSvr.start()

# main thread runs feed while addons are run in separate threads
while True:
    scheduled_feeds = dbRepo.get_scheduled_feeds()
    config = Config(scheduled_feeds=scheduled_feeds)
    now = datetime.now().time()
    next_scheduled_feed = config.feed_schedule.get_next_scheduled_feed(now)
    print('next scheduled feed is: {0}'.format(next_scheduled_feed))

    min = config.feed_schedule.get_min_until_next_scheduled_feed(now, next_scheduled_feed)
    print('next scheduled feed is: {0} min away'.format(min))

    time.sleep(min * 60)
    feeder.feed(next_scheduled_feed.portion)
    time.sleep(60)  # sleep a min to avoid repeating