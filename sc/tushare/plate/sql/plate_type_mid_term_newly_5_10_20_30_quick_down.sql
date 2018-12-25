-- 中线近5日急跌，10日跌幅大于5日跌幅，20日跌幅大于10跌幅

select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
-- and code='603922'
and trade_date='{{trade_date}}'
and close_amt > open_amt
and (close_amt-open_amt)/open_amt*100>1
and pre5_close_price_ratio <= -10
and pre10_close_price_ratio < pre5_close_price_ratio
and pre20_close_price_ratio < pre10_close_price_ratio
and pre30_close_price_ratio < pre20_close_price_ratio
;