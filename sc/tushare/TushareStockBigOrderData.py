
from TushareBase import TushareBase
import tushare as ts


class TushareStockBigOrderData(TushareBase, object):

    def __init__(self):
        super(TushareStockBigOrderData, self).__init__()
        print("big order data")

    def get_one_stock_big_order_data(self, stock_code=None, date=None, vol=400):
        data = ts.get_sina_dd(stock_code, date, vol)
        data["date"] = date
        print(data)
        return data

    def get_one_stock_big_order_data_to_db(self, stock_code, date):
        self.data_to_db_append(self.get_one_stock_big_order_data(stock_code, date), "t_tushare_stocke_big_order_data")


# big_order = TushareStockBigOrderData()
# big_order.get_one_stock_big_order_data("002113", "2018-09-28")
# big_order.get_one_stock_big_order_data_to_db("002113", "2018-09-26")