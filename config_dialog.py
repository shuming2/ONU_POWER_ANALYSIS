import os
import re
import sys
import tkinter
from tkinter import ttk, Spinbox


class ConfigDialog(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.transient(parent)
        self.grab_set()
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        self.resizable(0, 0)
        icopath = self._resource_path(r'pic/panda.ico')
        if os.path.exists(icopath):
            self.iconbitmap(icopath)

        self.frame = ttk.Frame(self)
        self.ok_button = tkinter.Button(self.frame, text="确定")
        self.cancel_button = tkinter.Button(self.frame, text="取消", command=self.destroy)

    def _set_config(self, config_dict=None):
        if config_dict:
            config_path = self._resource_path(r'config.py')
            with open(config_path, 'r') as config_file:
                lines = config_file.readlines()
            with open(config_path, 'w') as new_config_file:
                for line in lines:
                    config_name = re.sub(r' = .*', '', line.strip())
                    lower_config_name = str.lower(config_name)
                    if lower_config_name in config_dict:
                        new_config_file.write('{} = {}\n'.format(config_name, config_dict[lower_config_name]))
                    else:
                        new_config_file.write(line)
        self.destroy()

    def _get_config(self, config_name_lst=None):
        config_value_lst = []
        config_path = self._resource_path(r'config.py')
        with open(config_path, 'r') as config_file:
            for line in config_file:
                line = line.strip()
                config_name = re.sub(r' = .*', '', line)
                if config_name_lst:
                    lower_config_name = str.lower(config_name)
                    if lower_config_name in config_name_lst:
                        config_value = line.split('=')[1].strip().strip("'")
                        config_value_lst.append(config_value)
        return config_value_lst

    @staticmethod
    def _resource_path(relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)


class AlertConfigDialog(ConfigDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('告警设置')

        self.alert_threshold_label = ttk.Label(self.frame, text='告警阈值：')
        self.alert_threshold_value = tkinter.StringVar()
        self.alert_threshold_spinbox = Spinbox(self.frame, from_=0, to=10, width=5, bd=1,
                                               textvariable=self.alert_threshold_value)
        self.alert_threshold_value.set(self._get_config(['alert_threshold'])[0])

        self.ok_button.configure(command=self._update_alert_threshold)

    def gui_arrang(self):
        self.frame.grid(row=0, column=0, padx=10, pady=5)
        self.alert_threshold_label.grid(row=0, column=0, sticky='W')
        self.alert_threshold_spinbox.grid(row=0, column=1)
        self.ok_button.grid(row=2, column=3, pady=5)
        self.cancel_button.grid(row=2, column=4, pady=5)
        self.focus()

    def _update_alert_threshold(self):
        self._set_config({'alert_threshold': self.alert_threshold_value.get()})


class DBConfigDialog(ConfigDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('数据库设置')
        self.config_names = ['ip', 'username', 'pwd', 'db_name']

        self.ip_label = ttk.Label(self.frame, text='IP地址：')
        self.username_label = ttk.Label(self.frame, text='用户名：')
        self.pwd_label = ttk.Label(self.frame, text='密码：')
        self.db_name_label = ttk.Label(self.frame, text='数据库名：')
        # self.table_name_label = ttk.Label(self.frame, text='表名：')
        self.ui_labels = [self.ip_label, self.username_label, self.pwd_label, self.db_name_label]

        self.ip_value = tkinter.StringVar()
        self.username_value = tkinter.StringVar()
        self.pwd_value = tkinter.StringVar()
        self.db_name_value = tkinter.StringVar()
        # self.table_name_value = tkinter.StringVar()
        self.ui_values = [self.ip_value, self.username_value, self.pwd_value, self.db_name_value]

        self.ip_entry = tkinter.Entry(self.frame, width=20, textvariable=self.ip_value)
        self.username_entry = tkinter.Entry(self.frame, width=20, textvariable=self.username_value)
        self.pwd_entry = tkinter.Entry(self.frame, width=20, textvariable=self.pwd_value)
        self.db_name_entry = tkinter.Entry(self.frame, width=20, textvariable=self.db_name_value)
        # self.table_name_entry = tkinter.Entry(self.frame, width=20, textvariable=self.table_name_value)
        self.ui_entries = [self.ip_entry, self.username_entry, self.pwd_entry, self.db_name_entry]
        self.pwd_entry['show'] = '*'

        config_values = self._get_config(self.config_names)
        for i in range(len(self.config_names)):
            self.ui_values[i].set(config_values[i])

        self.ok_button.configure(command=self._update_db_config, text='连接')

    def gui_arrang(self):
        self.frame.grid(row=0, column=0, padx=10, pady=5)
        for i in range(len(self.config_names)):
            self.ui_labels[i].grid(row=i, column=0, sticky='W')
            self.ui_entries[i].grid(row=i, column=1)

        self.ok_button.grid(row=len(self.config_names), column=3, pady=5)
        self.cancel_button.grid(row=len(self.config_names), column=4, pady=5)
        self.focus()

    def _update_db_config(self):
        config_dict = {}
        for i in range(len(self.config_names)):
            config_dict[self.config_names[i]] = "'{}'".format(self.ui_values[i].get())
        self._set_config(config_dict)

