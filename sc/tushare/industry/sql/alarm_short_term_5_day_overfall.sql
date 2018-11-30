select * from t_sunso_stock_day_industry_statistic_core_data
where 1 > 0
and pre5_totals_stock_amt_ratio < -5  --行业前5日跌幅超过5%
and pre10_totals_stock_amt_ratio < 0  --当日比前10日低
and pre20_totals_stock_amt_ratio < 0  --当日比前20日低
and pre1_totals_stock_amt_ratio > 0   --当日比昨日高
-- and pre3_totals_stock_amt_ratio > 0
and pre1_totals_stock_amt_ratio > pre3_totals_stock_amt_ratio -- 当日涨幅大于前3日涨幅
and trade_volume > pre3_avg_trade_volume -- 当日交易量大于前3日平均交易量
and trade_date='2018-11-29'
order by avg_close_price_ratio desc