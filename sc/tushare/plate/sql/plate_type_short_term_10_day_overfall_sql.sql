insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,industry,area,circulation_amt,join_date)
select '{{plate_name}}','{{plate_start_date}}',code,name,industry,area,round(circulation_amt/10000,6),'{{join_date}}'
from t_sunso_stock_day_trade_statistic_core_data
where 1 > 0
and trade_date='{{trade_date}}'
and close_amt > 0
and close_pre_close_diff_amt_ratio between 0 and 5 -- 当日收盘价涨幅介于0到5之间
and pre10_close_price_ratio <= -15 -- 前10日跌幅超过15%
and pre1_avg_turnover_rate_ratio > 1 -- 当日换手率比昨日换手率大
and pre3_avg_turnover_rate_ratio > 1 -- 当日换手率大于前3日平均换手率
and pre_avg5_trade_price_ratio > pre_avg10_trade_price_ratio  -- 5日线平均收盘价大于10日线平均收盘价
and code not in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}')
;