# coding: utf8
import pymysql

"""
操作mysql数据
"""


class OperateMysql:
    def __init__(self, conf):
        self.conn = self.create_conn(conf)

    def create_conn(self, section):
        try:
            conn = pymysql.connect(section['host'], section['username'], section['password'], section['database'])
        except Exception as e:
            raise Exception("Connect Error %d: %s" % (e.args[0], e.args[1]))
        return conn

    def choose_database_info(self, env):
        if env == 'test':
            key = 'testEnv'
        elif env == 'trail':
            key = 'trailEnv'
        elif env == 'prod':
            key = 'prodEnv'
        else:
            raise 'No this environment as %s' % env
        getconfig = GetConfig('database.ini')  # 自己写一个读取ini格式的方法
        section = getconfig.getsection(key)
        return section

    def close(self, cur, conn):
        cur.close()
        conn.close()

    """查找语句"""

    def select(self, sql):
        sql = str(sql)
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            results = cur.fetchall()
        except Exception as e:
            self.close(cur, self.conn)
            raise Exception("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        self.close(cur, self.conn)
        return results

    """增删改都是调用excute写在一个里面"""

    def modifiy(self, sql):
        sql = str(sql)
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            # 发生错误先回滚，再抛出异常
            self.conn.rollback()
            self.conn.commit()
            self.close(cur, self.conn)
            raise Exception("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        self.close(cur, self.conn)


if __name__ == '__main__':
    conf = {"host": "", "port": "", "username": "", "password": "", "database": ""}
    OP = OperateMysql(conf)
    res = OP.select('SELECT * from ts_storage_partinfo_order_batch   LIMIT 1')
    print(res)
