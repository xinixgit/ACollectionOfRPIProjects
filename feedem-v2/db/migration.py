import sqlite3
from .repo import FEEDER_DB, SCHEDULED_FEEDS_TBL

CREATE_TBL_SQL = "CREATE TABLE IF NOT EXISTS {0} (id INTEGER PRIMARY KEY, time TEXT, portion INTEGER)".format(
    SCHEDULED_FEEDS_TBL)


class MigrationRunner:
    def execute(self):
        con = sqlite3.connect(FEEDER_DB)
        cur = con.cursor()
        cur.execute(CREATE_TBL_SQL)
        con.commit()
        con.close()
