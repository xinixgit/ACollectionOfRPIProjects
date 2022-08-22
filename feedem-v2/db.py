import sqlite3
from config import ScheduledFeed

FEEDER_DB = "feeder.db"

CREATE_TBL_SQL = "CREATE TABLE IF NOT EXISTS scheduled_feeds (id INTEGER PRIMARY KEY, time TEXT, portion INTEGER)"

def create_db():
    con = sqlite3.connect(FEEDER_DB)
    cur = con.cursor()
    cur.execute(CREATE_TBL_SQL)
    con.commit()
    con.close()

def get_scheduled_feeds() -> list[ScheduledFeed]:
    scheduled_feeds = []
    con = sqlite3.connect(FEEDER_DB)
    cur = con.cursor()
    res = cur.execute("SELECT time, portion FROM scheduled_feeds ORDER BY time")
    for row in res:
        feed = ScheduledFeed(row[0], row[1])
        scheduled_feeds.append(feed)

    con.close()
    return scheduled_feeds