from config import Config
from datetime import datetime
from feeder import Feeder
import time

config = Config()
feeder = Feeder()

while True:
    now = datetime.now().time()
    next_scheduled_feed = config.feed_schedule.get_next_scheduled_feed(now)
    print('next scheduled feed is: {0}'.format(next_scheduled_feed))

    min = config.feed_schedule.get_min_until_next_scheduled_feed(now, next_scheduled_feed)
    print('next scheduled feed is: {0} min away'.format(min))

    time.sleep(min * 60)
    feeder.feed(next_scheduled_feed.portion)
    time.sleep(60)  # sleep a min to avoid repeating