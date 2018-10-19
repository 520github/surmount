#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
# from matplotlib import rc
# rc('font',**{'family':'sans-serif','sans-serif':['AR PL KaitiM GB']})
import matplotlib.pyplot as plt

class BaseChart(object):
    def __init__(self):
        print("init ")


    def showOneDateListXAndValueListYChart(self, date_list, value_list, title="date and value chart", x_label="date", y_label="value"):
        plt.plot(date_list, value_list)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc='upper left')
        plt.yticks(value_list)
        plt.show()

    def showMulitDateListXAndValueListYChart(self, date_list, value_lists, title="date and value chart", x_label="date", y_label="value"):
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc='upper left')
        for x in value_lists:
            plt.plot(date_list, x)
        plt.show()

    def test(self, date_list, value_list):
        x = np.asanyarray(date_list)
        y = np.asanyarray(value_list)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x, y)
        ax.yaxis.set_ticks(y)
        plt.show()

# list = [1,2,3,4,5,6,7]
# plt.plot(list)
# plt.show()


chart = BaseChart()
date_list = ['2018-09-20', '2018-09-21', '2018-09-25', '2018-09-26', '2018-09-27', '2018-09-28']
#date_list = [20180920, 20180921, 20180925, 20180926, 20180927, 20180928]
value_list = [10.1, 2.29, -4.71, -0.91, 0.71, 9.91]
# chart.showOneDateListXAndValueListYChart(date_list, value_list)
# chart.test(date_list, value_list)

volumn_list = [164692.94, 444322.47, 254868.56, 186554.92, 261650.64, 225486.62]
# chart.showOneDateListXAndValueListYChart(date_list, volumn_list)

x_lists = [value_list]
chart.showMulitDateListXAndValueListYChart(date_list, x_lists)