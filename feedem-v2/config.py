import yaml
from datetime import time

class ScheduledFeed:
    def __init__(self, scheduled_feed):
        self.hr = int(scheduled_feed['time'][:2])
        self.min = int(scheduled_feed['time'][2:])
        self.portion = scheduled_feed['portion']

    def __repr__(self):
        hr = ('' if self.hr >= 10 else '0') + str(self.hr)
        min = ('' if self.min >= 10 else '0') + str(self.min)
        return '(time: {0}:{1}, portion: {2})'.format(hr, min, self.portion)


class FeedSchedule:
    def __init__(self, feed_schedule):
        self.scheduled_feeds = []
        for schedule in feed_schedule:
            self.scheduled_feeds.append(ScheduledFeed(schedule))

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
    def __init__(self):
        with open("config.yaml", "r") as stream:
            try:
                dataMap = yaml.safe_load(stream)
                self.feed_schedule = FeedSchedule(dataMap['feed_schedule'])
            except yaml.YAMLError as exc:
                print(exc)
