import datetime
import json
import time
import tkinter
from tkinter import ttk, messagebox

import requests

from config import INITIAL_TIME, MAX_EMPTY_DAYS, API_URL, CONTENT_TYPE, APP_KEY, APP_SECRET
from sql_command import *


class UpdateDialog(tkinter.Toplevel):
    def __init__(self, parent, db, cursor):
        super().__init__()
        self.transient(parent)
        self.grab_set()
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        self.title('更新数据')
        self.frame = tkinter.Frame(self)
        self.frame1 = tkinter.Frame(self.frame)
        self.text = tkinter.Text(self.frame1, width=60, height=10, state='disabled')

        # ScrollBar
        self.text_scrollbar = ttk.Scrollbar(self.frame1, orient='vertical', command=self.text.yview)
        self.text.configure(yscrollcommand=self.text_scrollbar.set)

        self.frame2 = tkinter.Frame(self.frame)
        self.button = tkinter.Button(self.frame2, text="开始更新", command=self.update_db)

        self.db = db
        self.cursor = cursor
        self.update_time_lst = self._get_update_time_lst()

    def gui_arrang(self):
        self.frame.pack(padx=10, pady=10, ipadx=5, ipady=0)
        self.frame1.pack()
        self.text.pack(side=tkinter.LEFT)
        self.text_scrollbar.pack(side=tkinter.RIGHT, fill='y')
        self.frame2.pack()
        self.button.pack(anchor=tkinter.CENTER, pady=5)

    def update_db(self):
        # Close Button
        self.protocol("WM_DELETE_WINDOW", self._show_warning)

        self.button.configure(text="确定", command=self.destroy, state='disabled')
        self.button.update()

        # For test
        # for i in range(0, 20):
        #     self.text.configure(state='normal')
        #     self.text.insert(tkinter.END, '{} 开始更新数据...\n'.format(self._get_current_time_str()))
        #     self.text.see(tkinter.END)
        #     self.text.configure(state='disabled')
        #     self.text.update()
        #     time.sleep(0.5)

        start_time = time.time()
        self.text.configure(state='normal')
        self.text.insert(tkinter.END, '{} 开始更新数据...\n'.format(self._get_current_time_str()))
        self.text.see(tkinter.END)
        self.text.configure(state='disabled')
        self.text.update()
        empty_days = 0
        data_count = 0
        for update_time in self.update_time_lst:
            data_lst = self._get_data_from_api(update_time)
            if not data_lst:
                data_lst = []

            empty_days = empty_days + 1 if not data_lst else 0
            if empty_days == MAX_EMPTY_DAYS:
                break

            for data in data_lst:
                self._write_to_db(data)
                self.update()

            if data_lst:
                self.text.configure(state='normal')
                self.text.insert(tkinter.END, '{} {} 更新成功, 共{}条数据...\n'.format(self._get_current_time_str(),
                                                                               update_time.strftime('%Y-%m-%d'),
                                                                               len(data_lst)))
                self.text.see(tkinter.END)
                self.text.configure(state='disabled')
                self.text.update()
                data_count += len(data_lst)
        self.text.configure(state='normal')
        self.text.insert(tkinter.END, '{} 本次共更新 {} 条新数据, 用时 {} s, 更新完成\n'.format(self._get_current_time_str(),
                                                                                 str(data_count),
                                                                                 '%.2f' % (time.time() - start_time)))
        self.text.see(tkinter.END)
        self.text.configure(state='disabled')
        self.button.configure(state='normal')
        # Close Button
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _get_update_time_lst(self):
        self.cursor.execute(SELECT_MAX_STATIS_TIME)
        latest_update_time = self.cursor.fetchone()[0]
        if not latest_update_time:
            latest_update_time = INITIAL_TIME

        update_time = latest_update_time + datetime.timedelta(days=1)
        today = datetime.datetime.now()

        update_time_lst = []
        while update_time < today:
            update_time_lst.append(update_time)
            update_time += datetime.timedelta(days=1)

        return update_time_lst

    def _write_to_db(self, data):
        value_lst = []
        for column_name in COLUMN_NAME_ONUFIBERN:
            try:
                value = data[column_name]
                if type(value) == str:
                    value_lst.append("'{}'".format(value))
                else:
                    value_lst.append("{}".format(value))
            except KeyError:
                value_lst.append('null')

        insert_command = INSERT_ONUFIBERN + '({});'.format(', '.join(value_lst))
        try:
            self.cursor.execute(insert_command)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    @staticmethod
    def _get_data_from_api(update_time):
        update_time_str = update_time.strftime('%Y-%m-%d %H:%M')

        params = {
            'app_key': APP_KEY,
            'app_secret': APP_SECRET,
            'conditions': json.dumps([{'cn': 'STATIS_TIME', 'op': '=', 'cv': update_time_str},
                                      {'cn': 'CITY_NAME ', 'op': '=', 'cv': '威海'}])  # TODO: Optimization for Re-use
        }
        response = requests.post(API_URL,
                                 headers={'Content-Type': CONTENT_TYPE},
                                 params=params)

        content = response.content.decode()
        results = json.loads(content)

        return results

    @staticmethod
    def _get_current_time_str():
        current_time = datetime.datetime.now()
        return current_time.strftime('[%Y/%m/%d %H:%M:%S]')

    # TODO
    def _show_warning(self):
        answer = messagebox.askokcancel(title='警告',
                                        message='现在退出会导致数据缺失，确认要退出吗？',
                                        default='cancel')
        if answer:
            self.destroy()
