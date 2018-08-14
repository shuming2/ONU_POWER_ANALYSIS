import time

import clipboard as clipboard
import tkinter
from tkinter import ttk
from sql_command import *
from chart import Chart
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
        # self.menu_bar.add_command(label='文件')

        self.menu_about = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_about.add_command(label='更新数据', command=self._update_db)
        self.menu_bar.add_cascade(label='关于', menu=self.menu_about)

        self.root['menu'] = self.menu_bar

        # Tab Control
        self.tab_control = ttk.Notebook(self.root)
        self.search_tab = ttk.Frame(self.tab_control)
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
        self.treeview_column_config = {"ONU_NAME": 380, "ONU_SN": 160}
        self._set_up_treeview(self.search_result_treeview, self.treeview_column_config)

        # Copy Menu
        self.copy_menu = tkinter.Menu(self.search_result_treeview, tearoff=0)
        self.copy_menu.add_command(label="复制", command=self._copy_handler)
        self.copy_menu.add_command(label="详情", command=self._show_chart)
        self.search_result_treeview.bind('<3>', self._show_copy_menu)

        # ScrollBar
        self.treeview_scrollbar = ttk.Scrollbar(self.frame1, orient='vertical',
                                                command=self.search_result_treeview.yview)
        self.search_result_treeview.configure(yscrollcommand=self.treeview_scrollbar.set)

        # TODO: Alert Tab
        # Alert Tab
        # self.column_name = tkinter.StringVar()
        # self.column_name_combobox = ttk.Combobox(self.alert_tab, width=20, textvariable=self.column_name,
        #                                          state='readonly')
        # self.column_name_combobox['values'] = ('ONU_NAME', 'ONU_SN')
        # self.column_name_combobox.set('ONU_NAME')
        #
        # self.search_input = tkinter.StringVar()
        # self.search_entry = tkinter.Entry(self.alert_tab, width=45, textvariable=self.search_input)
        # self.search_entry.bind('<Return>', self._search)
        # self.result_button = tkinter.Button(self.alert_tab, width=5, command=self._search, text='查询')
        #
        # self.frame1 = tkinter.Frame(self.alert_tab)
        # # TreeView
        # self.search_result_treeview = ttk.Treeview(self.frame1, show='headings', selectmode='browse')
        # self.search_result_treeview.grid_size()
        # self.search_result_treeview.bind('<Double-Button-1>', self._show_chart)
        # self.treeview_column_config = {"ONU_NAME": 380, "ONU_SN": 160}
        # self._set_up_treeview(self.search_result_treeview, self.treeview_column_config)
        #
        # # Copy Menu
        # self.copy_menu = tkinter.Menu(self.search_result_treeview, tearoff=0)
        # self.copy_menu.add_command(label="复制", command=self._copy_handler)
        # self.copy_menu.add_command(label="详情", command=self._show_chart)
        # self.search_result_treeview.bind('<3>', self._show_copy_menu)
        #
        # # ScrollBar
        # self.treeview_scrollbar = ttk.Scrollbar(self.frame1, orient='vertical',
        #                                         command=self.search_result_treeview.yview)
        # self.search_result_treeview.configure(yscrollcommand=self.treeview_scrollbar.set)

    def gui_arrang(self):
        self.tab_control.pack(expand=1, fill='both')

        self.column_name_combobox.grid(row=0, column=0)
        self.search_entry.grid(row=0, column=1, columnspan=2)
        self.result_button.grid(row=0, column=3)

        self.frame1.grid(row=1, column=0, columnspan=4)
        self.search_result_treeview.grid(row=0, column=0)
        self.treeview_scrollbar.grid(row=0, column=1, sticky='ns')
        self._search()
        for child in self.search_tab.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def _search(self, event=None):
        items = self.search_result_treeview.get_children()
        list(map(self.search_result_treeview.delete, items))
        results = self._get_search_results_from_db(self.cursor, self.column_name.get(), self.search_input.get())
        for i, result in enumerate(results):
            result_str = [str(ele) for ele in result]
            self.search_result_treeview.insert("", i, values=tuple(result_str))
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

    def _show_copy_menu(self, event):
        item_id = self.search_result_treeview.identify_row(event.y)
        self.search_result_treeview.selection_set(item_id)
        i = int(self.search_result_treeview.identify_column(event.x).strip('#')) - 1
        self.selected_value = self.search_result_treeview.item(item_id, 'values')[i]
        self.copy_menu.post(event.x_root, event.y_root)

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

        self._search()
