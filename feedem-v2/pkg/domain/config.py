import yaml
from datetime import time

# Object imported by reading the yaml config file, served as an intermediary 
# before moving to DB based config persistence. Do not use.
class ScheduledFeed:
    def __init__(self, hr: int, min: int, portion: int):
        self.hr = hr
        self.min = min
        self.portion = portion

    def __repr__(self):
        hr = ('' if self.hr >= 10 else '0') + str(self.hr)
        min = ('' if self.min >= 10 else '0') + str(self.min)
        return '(time: {0}:{1}, portion: {2})'.format(hr, min, self.portion)

# A container of all scheduled feeds and logic to select scheduled feeds
class FeedSchedule:
    def __init__(self, scheduled_feeds):
        self.scheduled_feeds = scheduled_feeds

    def get_next_scheduled_feed(self, now: time) -> ScheduledFeed:
        for feed in self.scheduled_feeds:
            if now.hour < feed.hr or (now.hour == feed.hr and now.minute <= feed.min):
                return feed

        return self.scheduled_feeds[0]

    def get_min_until_next_scheduled_feed(self, now: time, next_scheduled_feed: ScheduledFeed) -> int:
        next_hr = next_scheduled_feed.hr
        if next_hr < now.hour:
            next_hr += 24
            
        return (next_hr - now.hour) * 60 + (next_scheduled_feed.min - now.minute)

class Config:
    def __init__(self, scheduled_feeds: list[ScheduledFeed]=None, yaml_based_config=False):
        if yaml_based_config:
            scheduled_feeds = self.read_yaml()
        
        self.feed_schedule = FeedSchedule(scheduled_feeds)

    def json_to_scheduled_feeds(scheduled_feeds_json_arr) -> list[ScheduledFeed]:
        scheduled_feeds = []
        for feed in scheduled_feeds_json_arr:
            scheduled_feeds.append(ScheduledFeed(feed['time'], int(feed['portion'])))

        return scheduled_feeds

    def read_yaml(self) -> list[ScheduledFeed]:
        with open("config.yaml", "r") as stream:
            try:
                dataMap = yaml.safe_load(stream)
                return self.json_to_scheduled_feeds(dataMap['feed_schedule'])
            except yaml.YAMLError as exc:
                print(exc)