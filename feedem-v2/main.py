from config import Config
from datetime import datetime
from feeder import Feeder
from addon.web_server import WebServer
from addon.cam_streamer import CamStreamer
from addon.event_listener import EventListener
from db import DBRepo
import time

feeder = Feeder()

cam = CamStreamer()
event_listener = EventListener(
    on_cam_start_event=cam.start_recording,
    on_cam_stop_event=cam.stop_recording
)
event_listener.connect()

dbRepo = DBRepo()
webSvr = WebServer(dbRepo)
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