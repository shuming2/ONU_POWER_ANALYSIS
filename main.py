import re
import tkinter

import pymysql
from analysis import Analysis
from sql_command import *
from config import *


def check_table_exist(cursor, table_name):
    # From cj_cian 2016-11-27
    # https://zhidao.baidu.com/question/394979567818963085.html
    cursor.execute('show tables;')
    results = [cursor.fetchall()]
    table_list = re.findall("('.*?')", str(results))
    table_list = [re.sub("'", '', each) for each in table_list]
    return table_name in table_list


def connect_db(username, pwd, db_name, table_name):
    table_name = table_name.lower()
    connect = pymysql.connect('localhost', username, pwd, db_name)
    cursor = connect.cursor()

    if not check_table_exist(cursor, table_name):
        cursor.execute(CREATE_ONUFIBERN_TABLE)
        print('创建数据表 {}'.format(table_name))

    return connect, cursor


def main():
    db, cursor = connect_db(USERNAME, PWD, DB_NAME, TABLE_NAME)

    analysis = Analysis(db, cursor)
    analysis.gui_arrang()
    tkinter.mainloop()
    db.close()


if __name__ == '__main__':
    main()
