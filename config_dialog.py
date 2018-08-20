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
        icopath = self._resource_path(r'pic/panda.ico')
        if os.path.exists(icopath):
            self.iconbitmap(icopath)

        self.frame = ttk.Frame(self)
        self.ok_button = tkinter.Button(self.frame, text="确定")
        self.cancel_button = tkinter.Button(self.frame, text="取消", command=self.destroy)

    def _set_config(self, config_name, config_value):
        config_name = str.upper(config_name)
        config_path = self._resource_path(r'config.py')
        with open(config_path, 'r') as config_file:
            lines = config_file.readlines()
        with open(config_path, 'w') as new_config_file:
            for line in lines:
                if '{} '.format(config_name) in line or '{}='.format(config_name) in line:
                    new_config_file.write('{} = {}\n'.format(config_name, str(config_value)))
                else:
                    new_config_file.write(line)
        self.destroy()

    def _get_config(self, config_name):
        config_name = str.upper(config_name)
        config_value = None
        config_path = self._resource_path(r'config.py')
        with open(config_path, 'r') as config_file:
            for line in config_file:
                if '{} '.format(config_name) in line or '{}='.format(config_name) in line:
                    config_value = line.strip().split('=')[1].strip()
        return config_value

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
        self.alert_threshold_value.set(self._get_config('alert_threshold'))

        self.ok_button.configure(command=self._update_alert_threshold)

    def gui_arrang(self):
        self.frame.grid(row=0, column=0, padx=10, pady=5)
        self.alert_threshold_label.grid(row=0, column=0)
        self.alert_threshold_spinbox.grid(row=0, column=1)

        self.ok_button.grid(row=2, column=3, pady=5)
        self.cancel_button.grid(row=2, column=4, pady=5)
        self.focus()

    def _update_alert_threshold(self):
        self._set_config('alert_threshold', self.alert_threshold_spinbox.get())

