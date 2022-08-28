import sqlite3
from ..domain import config

FEEDER_DB = "feeder.db"
SCHEDULED_FEEDS_TBL = "scheduled_feeds"

class DBRepo:
    def get_scheduled_feeds(self) -> list[config.ScheduledFeed]:
        scheduled_feeds = []
        con = sqlite3.connect(FEEDER_DB)
        cur = con.cursor()
        res = cur.execute("SELECT time, portion FROM {0} ORDER BY time".format(SCHEDULED_FEEDS_TBL))
        for row in res:
            time = row[0]
            feed = config.ScheduledFeed(int(time[:2]), int(time[2:]), row[1])
            scheduled_feeds.append(feed)

        con.close()
        return scheduled_feeds

    def overwrite_scheduled_feeds(self, scheduled_feeds: list[config.ScheduledFeed]):
        records = []
        for feed in scheduled_feeds:
            records.append((str(feed.hr) + str(feed.min), feed.portion))

        con = sqlite3.connect(FEEDER_DB)
        cur = con.cursor()
        cur.execute("DELETE FROM {0}".format(SCHEDULED_FEEDS_TBL))
        cur.executemany("INSERT INTO {0} VALUES(?,?)", records)
        print(cur.rowcount, "feeds have been inserted")

        con.commit()
        con.close()
