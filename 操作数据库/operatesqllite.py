# coding: utf-8
import importlib

from DBUtils.PooledDB import PooledDB
from logger import logger


class OperateSqlite:

    def __init__(self, conf):
        self.pool = PooledDB(creator=importlib.import_module("sqlite3"), maxcached=50, maxconnections=1000,
                             maxusage=1000, **conf)

    def select(self, sql, dict_mark=False):
        result = []
        conn = self.pool.connection()
        cur = conn.cursor()
        try:
            if dict_mark:
                cur.execute(sql)

                fields = [desc[0] for desc in cur.description]
                rst = cur.fetchall()
                if rst:
                    result = [dict(zip(fields, row)) for row in rst]
            else:
                cur.execute(sql)
                result = cur.fetchall()
        except Exception as e:
            logger.error(e)
        finally:
            cur.close()
            conn.close()
            return result

    def excute(self, sql):
        result = []
        conn = self.pool.connection()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            result = cur.row_factory()
        except Exception as e:
            logger.error(e)
        finally:
            cur.close()
            conn.close()
            return result


if __name__ == "__main__":
    conf = {"database": ""}
    sql = "select * from amc limit 5"
    OO = OperateSqlite(conf)
    res = OO.select(sql)
    print(res)
