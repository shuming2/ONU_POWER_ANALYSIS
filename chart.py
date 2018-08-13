import tkinter

import pymysql
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from sql_command import *


class Chart(object):
    def __init__(self, title, db, cursor):
        self.db = db
        self.cursor = cursor

        self.root = tkinter.Tk()
        self.root.title(title)
        self.root.resizable(0, 0)

        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.chart = FigureCanvasTkAgg(self.figure, master=self.root)

        self.a = self.figure.add_subplot(111)
        self.date_lst, self.power_avg_lst = self._get_data_from_db_by_name(cursor, title)
        print(self.date_lst)
        print(self.power_avg_lst)
        # self.a.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%y/%m/%d'))
        self.a.axes.set_xticklabels(labels=list(dict.fromkeys(self.date_lst)), fontdict={'rotation': 40, 'size': 'small'})

        # Show text tab when hovering on scattered points
        # From ImportanceOfBeingErnest
        # https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib
        self.sc = None
        self.annot = self.a.annotate('', xy=(0, 0), xytext=(-15, 20), textcoords="offset points",
                                     bbox={'boxstyle': "round", 'fc': "w"},
                                     arrowprops=dict(arrowstyle="simple"))
        self.annot.set_visible(False)
        self.figure.canvas.mpl_connect("motion_notify_event", self._hover)

    def gui_arrang(self):
        self.sc = self.a.scatter(self.date_lst, self.power_avg_lst)
        self.a.plot(self.date_lst, self.power_avg_lst, linestyle="-")

        self.chart.draw()
        self.chart.get_tk_widget().pack(side=tkinter.TOP)

    @staticmethod
    def _show_at_center(screen_width, screen_height, current_width, current_height):
        geometry_size = '{}x{}+{}+{}'.format(current_width,
                                             current_height,
                                             (screen_width - current_width) // 2,
                                             (screen_height - current_height) // 2)
        return geometry_size

    @staticmethod
    def _get_data_from_db_by_name(cursor, onu_name):
        cursor.execute(SELECT_DATA_BY_GPON_REPORT_OLT.format(onu_name))
        results = list(cursor.fetchall())
        print(results)
        date_lst = []
        power_avg_lst = []
        for ele in results:
            date_lst.append(ele[1].strftime('%y/%m/%d'))
            # date_lst.append(ele[1])
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


def connect_db(username, pwd, db_name):
    connect = pymysql.connect('localhost', username, pwd, db_name)
    cursor = connect.cursor()
    return connect, cursor


def test():
    db, cursor = connect_db('amber', '19950613', 'cm_gpon_report')

    chart = Chart('家客_SDWH00246919', db, cursor)
    chart.gui_arrang()
    tkinter.mainloop()
    db.close()


if __name__ == '__main__':
    test()

