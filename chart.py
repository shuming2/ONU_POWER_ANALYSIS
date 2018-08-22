import datetime
import os
import sys
import tkinter
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from sql_command import *
from tooltip import ToolTip


class Chart(object):
    def __init__(self, title, db, cursor):
        self.db = db
        self.cursor = cursor

        self.root = tkinter.Tk()
        self.onu_name = title
        self.root.title(title)
        self.root.resizable(0, 0)
        icopath = self._resource_path(r'pic/panda.ico')
        if os.path.exists(icopath):
            self.root.iconbitmap(icopath)

        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.chart = FigureCanvasTkAgg(self.figure, master=self.root)

        self.a = self.figure.add_subplot(111)
        self.date_lst, self.power_avg_lst = self._get_data_from_db_by_name(cursor, title)
        self.a.axes.set_xticklabels(labels=list(dict.fromkeys(self.date_lst)),
                                    fontdict={'rotation': 40, 'size': 'small'})

        # Show text tab when hovering on scattered points
        # From ImportanceOfBeingErnest
        # https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib
        self.sc = None
        self.annot = self.a.annotate('', xy=(0, 0), xytext=(-15, 20), textcoords="offset points",
                                     bbox={'boxstyle': "round", 'fc': "w"},
                                     arrowprops=dict(arrowstyle="simple"))
        self.annot.set_visible(False)
        self.figure.canvas.mpl_connect("motion_notify_event", self._hover)

        self.detail_frame = ttk.Frame(self.root)
        self.labels = []
        self.details = []
        for column in COLUMN_NAME_ONUFIBERN:
            self.labels.append(ttk.Label(self.detail_frame, text=column+': ', width=25,
                                         font='Times -12 normal'))
            self.details.append(ttk.Label(self.detail_frame, width=40, text='-',
                                          font='Times -12 normal'))

    def gui_arrang(self):
        self.sc = self.a.scatter(self.date_lst, self.power_avg_lst)
        self.a.plot(self.date_lst, self.power_avg_lst, linestyle="-")

        self.chart.draw()
        self.chart.get_tk_widget().pack(side=tkinter.TOP)
        self.detail_frame.pack(side=tkinter.TOP, padx=5, pady=5)
        for i in range(0, len(self.labels)):
            self.labels[i].grid(row=i//2, column=(i % 2)*2, sticky='W')
            self.details[i].grid(row=i//2, column=(i % 2)*2+1, sticky='W')

    # @staticmethod
    # def _show_at_center(screen_width, screen_height, current_width, current_height):
    #     geometry_size = '{}x{}+{}+{}'.format(current_width,
    #                                          current_height,
    #                                          (screen_width - current_width) // 2,
    #                                          (screen_height - current_height) // 2)
    #     return geometry_size

    @staticmethod
    def _get_data_from_db_by_name(cursor, onu_name):
        cursor.execute(SELECT_DATA_BY_GPON_REPORT_OLT.format(onu_name))
        results = list(cursor.fetchall())
        date_lst = []
        power_avg_lst = []
        for ele in results:
            date_lst.append(ele[1].strftime('%y/%m/%d'))
            power_avg_lst.append(ele[0])
        return date_lst, power_avg_lst

    # Show text tab when hovering on scattered points
    # From ImportanceOfBeingErnest
    # https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib
    def _hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.a:
            cont, ind = self.sc.contains(event)
            if cont:
                self._update_annot(ind)
                self.annot.set_visible(True)
                self.chart.draw()
                self._show_detail(ind)
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.chart.draw()

    # Show text tab when hovering on scattered points
    # From ImportanceOfBeingErnest
    # https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib
    def _update_annot(self, ind):
        i = ind["ind"][0]
        self.annot.xy = self.sc.get_offsets()[i]
        self.annot.set_text(str(self.power_avg_lst[i]))
        self.annot.get_bbox_patch().set_alpha(0.4)

    @staticmethod
    def _resource_path(relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)

    @staticmethod
    def _get_detail_from_db_by_name(cursor, onu_name):
        cursor.execute(SELECT_DATA_BY_GPON_REPORT_OLT.format(onu_name))
        results = list(cursor.fetchall())
        date_lst = []
        power_avg_lst = []
        for ele in results:
            date_lst.append(ele[1].strftime('%y/%m/%d'))
            power_avg_lst.append(ele[0])
        return date_lst, power_avg_lst

    def _show_detail(self, ind):
        self.detail_frame.pack(side=tkinter.LEFT)
        dt = datetime.datetime.strptime(self.date_lst[ind["ind"][0]], '%y/%m/%d')
        self.cursor.execute(SELECT_DETAIL_BY_GPON_REPORT_OLT_AND_STATIS_TIME.format(self.onu_name, dt))
        results = list(self.cursor.fetchall()[0])

        for i, detail in enumerate(self.details):
            result = results[i]
            if result:
                if type(result) == float:
                    if int(result) == result:
                        result = int(result)
                detail.configure(text=result)
                self._create_tooltip(detail, result)
            else:
                detail.configure(text='-')

    # From i_chaoren
    # https://blog.csdn.net/i_chaoren/article/details/56296713
    @staticmethod
    def _create_tooltip(widget, text):
        tooltip = ToolTip(widget)

        def enter(event):
            tooltip.showtip(text)

        def leave(event):
            tooltip.hidetip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)


