import tkinter
from tkinter import ttk, Spinbox
from config import ALERT_THRESHOLD


class ConfigDialog(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.transient(parent)
        self.grab_set()
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        self.resizable(0, 0)
        self.title('设置')

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

    def _update_alert_threshold(self):
        with open('config.py', 'r') as config_file:
            lines = config_file.readlines()
        with open('config.py', 'w') as new_config_file:
            for line in lines:
                if 'ALERT_THRESHOLD ' in line or 'ALERT_THRESHOLD=' in line:
                    new_config_file.write('ALERT_THRESHOLD = {}\n'.format(self.alert_threshold_spinbox.get()))
                else:
                    new_config_file.write(line)
        self.destroy()

    @staticmethod
    def _get_alert_threshold():
        alert_threshold = 0
        with open('config.py', 'r') as config_file:
            for line in config_file:
                if 'ALERT_THRESHOLD ' in line or 'ALERT_THRESHOLD=' in line:
                    alert_threshold = line.strip().split('=')[1].strip()
        return int(alert_threshold)
