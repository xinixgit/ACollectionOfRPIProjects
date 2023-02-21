import sqlite3
import string
from ..domain import config
from typing import Tuple

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

    def overwrite_scheduled_feeds(self, feeds: Tuple[str, int]):
        con = sqlite3.connect(FEEDER_DB)
        cur = con.cursor()
        cur.execute("DELETE FROM {0}".format(SCHEDULED_FEEDS_TBL))
        cur.executemany("INSERT INTO {0} (time, portion) VALUES(?,?)".format(SCHEDULED_FEEDS_TBL), feeds)
        print(cur.rowcount, "feeds have been inserted")

        con.commit()
        con.close()