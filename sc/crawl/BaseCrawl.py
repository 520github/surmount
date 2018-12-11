#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import urlopen, Request
import json
import pandas as pd

class BaseCrawl(object):

    def __init__(self):
        print("")

    def getTextByUrl(self, url):
        request = Request(url)
        text = urlopen(request, timeout=10).read()
        return text

    def getTest(self):
        url = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,sortType=,startDate=2018-12-10,endDate=2018-12-10,gpfw=0,js=vardata_tab_1.html'
        text = self.getTextByUrl(url)
        text = text.decode("GBK")
        text = text.split('_1=')[1]

        text = eval(text, type('Dummy', (dict,),
                               dict(__getitem__=lambda s, n: n))())

        text = json.dumps(text)
        text = json.loads(text)
        temp_cols = ['SCode', 'SName', 'Chgradio', 'ZeMoney', 'Bmoney', 'Smoney', 'Ctypedes', 'Turnover']
        df = pd.DataFrame(text['data'], columns=temp_cols)

        df.columns = ['code', 'name', 'pchange', 'amount', 'buy', 'sell', 'reason', 'Turnover']
        df = df.fillna(0)
        df = df.replace('', 0)

        FORMAT = lambda x: '%.2f' % x

        df['buy'] = df['buy'].astype(float)
        df['sell'] = df['sell'].astype(float)
        df['amount'] = df['amount'].astype(float)
        df['Turnover'] = df['Turnover'].astype(float)
        df['bratio'] = df['buy'] / df['Turnover']
        df['sratio'] = df['sell'] / df['Turnover']
        df['bratio'] = df['bratio'].map(FORMAT)
        df['sratio'] = df['sratio'].map(FORMAT)

        for col in ['amount', 'buy', 'sell']:
            df[col] = df[col].astype(float)
            df[col] = df[col] / 10000
            df[col] = df[col].map(FORMAT)
        df = df.drop('Turnover', axis=1)
        return df


if __name__ == "__main__":
    crawl = BaseCrawl()
    crawl.getTest()
    # url = "http://www.baidu.com"
    # text = crawl.getTextByUrl(url)
    # print("text-->" + text)