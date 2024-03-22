from datetime import datetime
from feeder.feeder import Feeder
from web.web_server import WebServer, RequestHandlerContext
from web.cam_request_helper import CameraStreamer
from web.event_listener import EventListener
from db.migration import MigrationRunner
from db.repo import DBRepo
from domain.config import Config
import time
import sys

db_migration = MigrationRunner()
db_migration.execute()

try:
    event_listener = EventListener()
    event_listener.connect(user=sys.argv[1], pwd=sys.argv[2])
except:
    print("Failed to start MQTT event listener")

feeder = Feeder()
dbRepo = DBRepo()
cam = CameraStreamer()
ctx = RequestHandlerContext(
    dbRepo=dbRepo,
    cam=cam,
    feeder=feeder,
    event_listener=event_listener
)
webSvr = WebServer(ctx)
webSvr.start()

# main thread runs feed while addons are run in separate threads
while True:
    scheduled_feeds = dbRepo.get_scheduled_feeds()
    config = Config(scheduled_feeds=scheduled_feeds)
    now = datetime.now().time()
    next_scheduled_feed = config.feed_schedule.get_next_scheduled_feed(now)
    print('next scheduled feed is: {0}'.format(next_scheduled_feed))

    min = config.feed_schedule.get_min_until_next_scheduled_feed(
        now, next_scheduled_feed)
    print('next scheduled feed is: {0} min away'.format(min))

    time.sleep(min * 60)
    feeder.feed(next_scheduled_feed.portion)
    event_listener.publish_portion_fed(next_scheduled_feed.portion)
    time.sleep(60)  # sleep a min to avoid repeating
