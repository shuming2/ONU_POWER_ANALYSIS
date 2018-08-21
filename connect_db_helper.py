import pymysql
import re
from sql_command import CREATE_ONUFIBERN_TABLE


class ConnectDBHelper:
    def __init__(self, ip, username, pwd, db_name, table_name):
        self.ip = ip
        self.username = username
        self.pwd = pwd
        self.db_name = db_name
        self.table_name = table_name.lower()

    def connect(self):
        try:
            connect = pymysql.connect(self.ip, self.username, self.pwd, self.db_name)
        except pymysql.err.OperationalError:
            return None, None
        cursor = connect.cursor()

        if not self._check_table_exist(cursor, self.table_name):
            cursor.execute(CREATE_ONUFIBERN_TABLE)
            print('创建数据表 {}'.format(self.table_name))

        return connect, cursor

    @staticmethod
    def _check_table_exist(cursor, table_name):
        # From cj_cian 2016-11-27
        # https://zhidao.baidu.com/question/394979567818963085.html
        cursor.execute('show tables;')
        results = [cursor.fetchall()]
        table_list = re.findall("('.*?')", str(results))
        table_list = [re.sub("'", '', each) for each in table_list]
        return table_name in table_list

