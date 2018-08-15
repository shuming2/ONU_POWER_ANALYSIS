import datetime
import time
import tkinter
from tkinter import ttk, messagebox

import clipboard as clipboard

from chart import Chart
from config_dialog import ConfigDialog
from sql_command import *
from update_dialog import UpdateDialog


class Analysis(object):
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

        self.root = tkinter.Tk()
        self.root.title("家客ONU光功率分析")
        self.root.resizable(0, 0)

        # Manu Bar
        self.menu_bar = tkinter.Menu(self.root, tearoff=0)
        self.menu_file = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_file.add_command(label='更新数据', command=self._update_db)
        self.menu_file.add_command(label='设置', command=self._config)
        self.menu_bar.add_cascade(label='文件', menu=self.menu_file)

        self.root['menu'] = self.menu_bar

        # Tab Control
        self.tab_control = ttk.Notebook(self.root)
        self.search_tab = ttk.Frame(self.tab_control)
        self.tab_control.bind('<<NotebookTabChanged>>', self._clear_status_bar)
        self.alert_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.search_tab, text='查询')
        self.tab_control.add(self.alert_tab, text='告警')

        # Search Tab
        self.column_name = tkinter.StringVar()
        self.column_name_combobox = ttk.Combobox(self.search_tab, width=20, textvariable=self.column_name,
                                                 state='readonly')
        self.column_name_combobox['values'] = ('ONU_NAME', 'ONU_SN')
        self.column_name_combobox.set('ONU_NAME')

        self.search_input = tkinter.StringVar()
        self.search_entry = tkinter.Entry(self.search_tab, width=45, textvariable=self.search_input)
        self.search_entry.bind('<Return>', self._search)
        self.result_button = tkinter.Button(self.search_tab, width=5, command=self._search, text='查询')

        self.frame1 = tkinter.Frame(self.search_tab)
        # TreeView
        self.search_result_treeview = ttk.Treeview(self.frame1, show='headings', selectmode='browse')
        self.search_result_treeview.grid_size()
        self.search_result_treeview.bind('<Double-Button-1>', self._show_chart)
        self.treeview_column_config = {'ONU_NAME': 380, 'ONU_SN': 160}
        self._set_up_treeview(self.search_result_treeview, self.treeview_column_config)

        # Copy Menu
        self.copy_menu = tkinter.Menu(self.search_result_treeview, tearoff=0)
        self.copy_menu.add_command(label='复制', command=self._copy_handler)
        self.copy_menu.add_command(label='详情', command=self._show_chart)
        self.search_result_treeview.bind('<3>', self._show_copy_menu)

        # ScrollBar
        self.treeview_scrollbar = ttk.Scrollbar(self.frame1, orient='vertical',
                                                command=self.search_result_treeview.yview)
        self.search_result_treeview.configure(yscrollcommand=self.treeview_scrollbar.set)

        # Alert Tab
        # Start Time
        self.start_time_frame = ttk.Frame(self.alert_tab)
        self.start_time_label = ttk.Label(self.start_time_frame, text='开始时间: ')

        self.start_year = tkinter.StringVar()
        self.start_year_combobox = ttk.Combobox(self.start_time_frame, width=4, textvariable=self.start_year,
                                                state='readonly')
        self.start_year_combobox['values'] = (self._get_year_options())
        self.start_year_combobox.bind("<<ComboboxSelected>>", self._update_start_day_options)
        self.start_year_combobox.set(str(datetime.datetime.now().year))
        self.start_year_label = ttk.Label(self.start_time_frame, text='年')

        self.start_month = tkinter.StringVar()
        self.start_month_combobox = ttk.Combobox(self.start_time_frame, width=2, textvariable=self.start_month,
                                                 state='readonly')
        self.start_month_combobox['values'] = tuple([str(month) for month in range(1, 13)])
        self.start_month_combobox.bind("<<ComboboxSelected>>", self._update_start_day_options)
        self.start_month_combobox.set(str(datetime.datetime.now().month))
        self.start_month_label = ttk.Label(self.start_time_frame, text='月')

        self.start_day = tkinter.StringVar()
        self.start_day_combobox = ttk.Combobox(self.start_time_frame, width=2, textvariable=self.start_day,
                                               state='readonly')
        self.start_day_combobox['values'] = (tuple([str(day) for day in range(1, 32)]))
        self.start_day_combobox.set(str(datetime.datetime.now().day))
        self.start_day_label = ttk.Label(self.start_time_frame, text='日')

        # End Time
        self.end_time_frame = ttk.Frame(self.alert_tab)
        self.end_time_label = ttk.Label(self.end_time_frame, text='结束时间: ')

        self.end_year = tkinter.StringVar()
        self.end_year_combobox = ttk.Combobox(self.end_time_frame, width=4, textvariable=self.end_year,
                                              state='readonly')
        self.end_year_combobox['values'] = (self._get_year_options())
        self.end_year_combobox.bind("<<ComboboxSelected>>", self._update_end_day_options)
        self.end_year_combobox.set(str(datetime.datetime.now().year))
        self.end_year_label = ttk.Label(self.end_time_frame, text='年')

        self.end_month = tkinter.StringVar()
        self.end_month_combobox = ttk.Combobox(self.end_time_frame, width=2, textvariable=self.end_month,
                                               state='readonly')
        self.end_month_combobox['values'] = tuple([str(month) for month in range(1, 13)])
        self.end_month_combobox.bind("<<ComboboxSelected>>", self._update_end_day_options)
        self.end_month_combobox.set(str(datetime.datetime.now().month))
        self.end_month_label = ttk.Label(self.end_time_frame, text='月')

        self.end_day = tkinter.StringVar()
        self.end_day_combobox = ttk.Combobox(self.end_time_frame, width=2, textvariable=self.end_day,
                                             state='readonly')
        self.end_day_combobox['values'] = (tuple([str(day) for day in range(1, 32)]))
        self.end_day_combobox.set(str(datetime.datetime.now().day))
        self.end_day_label = ttk.Label(self.end_time_frame, text='日')

        self.scan_button = tkinter.Button(self.alert_tab, width=5, command=self._scan, text='扫描')
        self.start_time_frame.bind_all('<Return>', self._scan)
        self.end_time_frame.bind_all('<Return>', self._scan)

        self.frame2 = tkinter.Frame(self.alert_tab)
        # TreeView
        self.scan_result_treeview = ttk.Treeview(self.frame2, show='headings', selectmode='browse')
        self.scan_result_treeview.grid_size()
        self.scan_result_treeview.bind('<Double-Button-1>', self._show_scan_chart)
        self.scan_treeview_column_config = {'DATE': 60, 'ONU_NAME': 300, 'ONU_SN': 130, 'VALUE': 50}
        self._set_up_treeview(self.scan_result_treeview, self.scan_treeview_column_config)

        # Copy Menu
        self.scan_copy_menu = tkinter.Menu(self.scan_result_treeview, tearoff=0)
        self.scan_copy_menu.add_command(label="复制", command=self._copy_handler)
        self.scan_copy_menu.add_command(label="详情", command=self._show_scan_chart)
        self.scan_result_treeview.bind('<3>', self._show_scan_copy_menu)

        # ScrollBar
        self.scan_treeview_scrollbar = ttk.Scrollbar(self.frame2, orient='vertical',
                                                     command=self.scan_result_treeview.yview)
        self.scan_result_treeview.configure(yscrollcommand=self.scan_treeview_scrollbar.set)

        # Status Bar
        self.status_bar = ttk.Frame(self.root)
        self.version_label = ttk.Label(self.status_bar, text='数据库版本时间： ' + self._get_version_time())
        # Progress Bar
        self.scan_percentage_label = ttk.Label(self.status_bar, text='')
        self.scan_status_label = ttk.Label(self.status_bar, text='')
        self.progress_bar = tkinter.Canvas(self.status_bar, width=100, height=10, bg='white')
        self.out_line = self.progress_bar.create_rectangle(2, 2, 100, 10, width=1, outline='black')
        self.fill_line = self.progress_bar.create_rectangle(2, 2, 0, 10, width=0, fill="black")

    def gui_arrang(self):
        self.tab_control.pack(expand=1, fill='both')

        # Search Tab
        self.column_name_combobox.grid(row=0, column=0)
        self.search_entry.grid(row=0, column=1, columnspan=2)
        self.result_button.grid(row=0, column=3)

        self.frame1.grid(row=1, column=0, columnspan=4)
        self.search_result_treeview.grid(row=0, column=0)
        self.treeview_scrollbar.grid(row=0, column=1, sticky='ns')
        self._search()
        for child in self.search_tab.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Alert Tab
        # Start Time
        self.start_time_frame.grid(row=0, column=0)
        self.start_time_label.grid(row=0, column=0)
        self.start_year_combobox.grid(row=0, column=1)
        self.start_year_label.grid(row=0, column=2)
        self.start_month_combobox.grid(row=0, column=3)
        self.start_month_label.grid(row=0, column=4)
        self.start_day_combobox.grid(row=0, column=5)
        self.start_day_label.grid(row=0, column=6)

        # End Time
        self.end_time_frame.grid(row=0, column=1)
        self.end_time_label.grid(row=0, column=0)
        self.end_year_combobox.grid(row=0, column=1)
        self.end_year_label.grid(row=0, column=2)
        self.end_month_combobox.grid(row=0, column=3)
        self.end_month_label.grid(row=0, column=4)
        self.end_day_combobox.grid(row=0, column=5)
        self.end_day_label.grid(row=0, column=6)

        self.scan_button.grid(row=0, column=2)

        self.frame2.grid(row=1, column=0, columnspan=3)
        self.scan_result_treeview.grid(row=0, column=0)
        self.scan_treeview_scrollbar.grid(row=0, column=1, sticky='ns')

        for child in self.alert_tab.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.status_bar.pack(fill='x', padx=5)
        self.version_label.pack(side=tkinter.LEFT)

    def _search(self, event=None):
        items = self.search_result_treeview.get_children()
        list(map(self.search_result_treeview.delete, items))
        results = self._get_search_results_from_db(self.cursor, self.column_name.get(), self.search_input.get())
        for i, result in enumerate(results):
            result_str = [str(ele) for ele in result]
            self.search_result_treeview.insert('', i, values=tuple(result_str))
        return

    @staticmethod
    def _set_up_treeview(treeview, column_config):
        treeview["columns"] = tuple(column_config.keys())
        for column, width in column_config.items():
            treeview.column(column, width=width, anchor='w')
            treeview.heading(column, text=column)

    def _show_chart(self, event=None):
        items = self.search_result_treeview.selection()
        if len(items) == 0:
            return
        item = items[0]
        item_text = self.search_result_treeview.item(item, "values")
        chart = Chart(item_text[0], self.db, self.cursor)
        chart.gui_arrang()
        tkinter.mainloop()

    def _show_scan_chart(self, event=None):
        items = self.scan_result_treeview.selection()
        if len(items) == 0:
            return
        item = items[0]
        item_text = self.scan_result_treeview.item(item, "values")
        chart = Chart(item_text[1], self.db, self.cursor)
        chart.gui_arrang()
        tkinter.mainloop()

    def _show_copy_menu(self, event):
        item_id = self.search_result_treeview.identify_row(event.y)
        self.search_result_treeview.selection_set(item_id)
        i = int(self.search_result_treeview.identify_column(event.x).strip('#')) - 1
        self.selected_value = self.search_result_treeview.item(item_id, 'values')[i]
        self.copy_menu.post(event.x_root, event.y_root)

    def _show_scan_copy_menu(self, event):
        item_id = self.scan_result_treeview.identify_row(event.y)
        self.scan_result_treeview.selection_set(item_id)
        i = int(self.scan_result_treeview.identify_column(event.x).strip('#')) - 1
        self.selected_value = self.scan_result_treeview.item(item_id, 'values')[i]
        self.scan_copy_menu.post(event.x_root, event.y_root)

    def _copy_handler(self):
        clipboard.copy(self.selected_value)

    @staticmethod
    def _get_search_results_from_db(cursor, column_name, search_input):
        if column_name == 'ONU_NAME':
            column_name = 'GPON_REPORT_OLT'

        if search_input == '':
            cursor.execute(SELECT_DISTINCT_GPON_REPORT_OLT)
        else:
            cursor.execute(SELECT_DISTINCT_GPON_REPORT_OLT_WITH_SEARCH_INPUT.format(column_name, search_input))
        results = list(cursor.fetchall())

        distinct_lst = []
        for ele in results:
            new_ele = list(ele)
            if type(new_ele[1]) == float:
                new_ele[1] = int(new_ele[1])
            distinct_lst.append(new_ele)

        return distinct_lst

    def _update_db(self):
        update_dialog = UpdateDialog(self.root, self.db, self.cursor)
        update_dialog.gui_arrang()
        self.root.wait_window(update_dialog)
        self.version_label.configure(text='数据库版本时间： ' + self._get_version_time())
        self._search()

    @staticmethod
    def _get_year_options():
        initial_year = 2018
        current_year = datetime.datetime.now().year
        year_lst = [str(year) for year in range(initial_year, current_year + 1)]
        return tuple(year_lst)

    def _update_start_day_options(self, event):
        last_day = self._get_last_day(int(self.start_year.get()), int(self.start_month.get()))
        self.start_day_combobox['values'] = tuple([str(day) for day in range(1, last_day + 1)])
        if int(self.start_day.get()) > last_day:
            self.start_day_combobox.set(str(last_day))

    def _update_end_day_options(self, event):
        last_day = self._get_last_day(int(self.end_year.get()), int(self.end_month.get()))
        self.end_day_combobox['values'] = tuple([str(day) for day in range(1, last_day + 1)])
        if int(self.end_day.get()) > last_day:
            self.end_day_combobox.set(str(last_day))

    @staticmethod
    def _get_last_day(year, month):
        if month != 12:
            first_day = datetime.datetime(year, month + 1, 1)
        else:
            first_day = datetime.datetime(year + 1, 1, 1)
        last_day = (first_day - datetime.timedelta(days=1)).day
        return last_day

    def _get_version_time(self):
        self.cursor.execute(SELECT_MAX_STATIS_TIME)
        latest_update_time = self.cursor.fetchone()[0]
        if latest_update_time:
            return latest_update_time.strftime('%Y-%m-%d')
        else:
            return '-'

    def _scan(self, event=None):
        t = time.time()
        # Clear treeview
        items = self.scan_result_treeview.get_children()
        list(map(self.scan_result_treeview.delete, items))
        self._clear_status_bar()

        # Check start time and end time
        start_time = datetime.datetime(int(self.start_year.get()),
                                       int(self.start_month.get()),
                                       int(self.start_day.get()))
        end_time = datetime.datetime(int(self.end_year.get()),
                                     int(self.end_month.get()),
                                     int(self.end_day.get()))
        if start_time > end_time:
            messagebox.showwarning('错误', '请检查输入时间。')
            return

        # Get number of data in this time period
        self.cursor.execute(SELECT_COUNT_IN_TIME_PERIOD.format(start_time.strftime('%Y-%m-%d 00:00:00'),
                                                               end_time.strftime('%Y-%m-%d 00:00:00')))
        start_time, end_time, total_number = self.cursor.fetchone()

        scanned_number = 0
        self._update_scan_results(0, scanned_number, total_number)
        if total_number:
            self.scan_percentage_label.pack(side=tkinter.RIGHT)
            self.progress_bar.pack(side=tkinter.RIGHT, padx=5)
            self.scan_status_label.pack(side=tkinter.RIGHT)
        else:
            self.scan_status_label.pack(side=tkinter.RIGHT)
            return

        scan_time_period = []
        tmp_time = start_time
        while tmp_time <= end_time:
            scan_time_period.append(tmp_time)
            tmp_time += datetime.timedelta(days=1)

        scan_treeview_index = 0
        for scan_time in scan_time_period:
            if scan_time == start_time:
                previous_date = scan_time - datetime.timedelta(days=1)
                self.cursor.execute(SELECT_DATA_BY_STATIS_TIME.format(previous_date.strftime('%Y-%m-%d 00:00:00')))
                previous_data = list(self.cursor.fetchall())
            else:
                previous_data = data

            scan_dic = {}
            for ele in previous_data:
                scan_dic[ele[1]] = ele[3]

            self.cursor.execute(SELECT_DATA_BY_STATIS_TIME.format(scan_time.strftime('%Y-%m-%d 00:00:00')))
            data = list(self.cursor.fetchall())

            for ele in data:
                if ele[1] in scan_dic.keys():
                    value = ele[3] - scan_dic[ele[1]]
                    if value < -self._get_alert_threshold():
                        result_str = [ele[0].strftime('%y/%m/%d'), ele[1], ele[2], str(round(value, 2))]
                        self.scan_result_treeview.insert('', scan_treeview_index, values=tuple(result_str))
                        scan_treeview_index += 1
                        self.scan_result_treeview.update()
                scanned_number += 1
                self._update_scan_results(scan_treeview_index, scanned_number, total_number)
        print("Execution time: {} s".format(time.time() - t))

    def _update_scan_results(self, found_number, scanned_number, total_number):
        if total_number == 0:
            self.scan_status_label.configure(text='该时间段内没有数据')
            return
        self.scan_percentage_label.configure(text='%3s %%' % str(scanned_number * 100 // total_number))
        self.progress_bar.coords(self.fill_line, (2, 2, scanned_number * 100 // total_number, 10))
        self.scan_status_label.configure(text='发现 {} 条告警 {} / {}'.format(found_number, scanned_number, total_number))
        self.status_bar.update()

    def _clear_status_bar(self, event=None):
        self.scan_percentage_label.pack_forget()
        self.progress_bar.pack_forget()
        self.scan_status_label.pack_forget()

    def _config(self):
        config_dialog = ConfigDialog(self.root)
        config_dialog.gui_arrang()
        self.root.wait_window(config_dialog)

    @staticmethod
    def _get_alert_threshold():
        alert_threshold = 0
        with open('config.py', 'r') as config_file:
            for line in config_file:
                if 'ALERT_THRESHOLD ' in line or 'ALERT_THRESHOLD=' in line:
                    alert_threshold = line.strip().split('=')[1].strip()
        return int(alert_threshold)
