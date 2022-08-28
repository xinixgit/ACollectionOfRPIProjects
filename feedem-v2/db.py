import sqlite3
from config import ScheduledFeed

FEEDER_DB = "feeder.db"
SCHEDULED_FEEDS_TBL = "scheduled_feeds"

CREATE_TBL_SQL = "CREATE TABLE IF NOT EXISTS scheduled_feeds (id INTEGER PRIMARY KEY, time TEXT, portion INTEGER)"

def create_db():
    con = sqlite3.connect(FEEDER_DB)
    cur = con.cursor()
    cur.execute(CREATE_TBL_SQL)
    con.commit()
    con.close()

class DBRepo:
    def get_scheduled_feeds(self) -> list[ScheduledFeed]:
        scheduled_feeds = []
        con = sqlite3.connect(FEEDER_DB)
        cur = con.cursor()
        res = cur.execute("SELECT time, portion FROM {0} ORDER BY time".format(SCHEDULED_FEEDS_TBL))
        for row in res:
            time = row[0]
            feed = ScheduledFeed(int(time[:2]), int(time[2:]), row[1])
            scheduled_feeds.append(feed)

        con.close()
        return scheduled_feeds

    def overwrite_scheduled_feeds(self, scheduled_feeds: list[ScheduledFeed]):
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
