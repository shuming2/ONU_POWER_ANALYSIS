import os
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
        self.title('设置')
        icopath = self._resource_path(r'pic/panda.ico')
        if os.path.exists(icopath):
            self.iconbitmap(icopath)

        self.frame = ttk.Frame(self)
        self.alert_threshold_label = ttk.Label(self.frame, text='告警阈值：')
        self.alert_threshold_value = tkinter.StringVar()
        self.alert_threshold_spinbox = Spinbox(self.frame, from_=0, to=10, width=5, bd=1,
                                               textvariable=self.alert_threshold_value)
        self.alert_threshold_value.set(str(self._get_alert_threshold()))

        self.ok_button = tkinter.Button(self.frame, text="确定", command=self._update_alert_threshold)
        self.cancel_button = tkinter.Button(self.frame, text="取消", command=self.destroy)

    def gui_arrang(self):
        self.frame.grid(row=0, column=0, padx=10, pady=5)
        self.alert_threshold_label.grid(row=0, column=0)
        self.alert_threshold_spinbox.grid(row=0, column=1)

        self.ok_button.grid(row=2, column=3, pady=5)
        self.cancel_button.grid(row=2, column=4, pady=5)
        self.focus()

    def _update_alert_threshold(self):
        config_path = self._resource_path(r'config.py')
        with open(config_path, 'r') as config_file:
            lines = config_file.readlines()
        with open(config_path, 'w') as new_config_file:
            for line in lines:
                if 'ALERT_THRESHOLD ' in line or 'ALERT_THRESHOLD=' in line:
                    new_config_file.write('ALERT_THRESHOLD = {}\n'.format(self.alert_threshold_spinbox.get()))
                else:
                    new_config_file.write(line)
        self.destroy()

    def _get_alert_threshold(self):
        alert_threshold = 0
        config_path = self._resource_path(r'config.py')
        with open(config_path, 'r') as config_file:
            for line in config_file:
                if 'ALERT_THRESHOLD ' in line or 'ALERT_THRESHOLD=' in line:
                    alert_threshold = line.strip().split('=')[1].strip()
        return int(alert_threshold)

    @staticmethod
    def _resource_path(relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)

