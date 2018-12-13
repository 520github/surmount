insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,industry,area,circulation_amt,join_date)
select '{{plate_name}}','{{plate_start_date}}',code,name,industry,area,round(circulation_amt/10000,6),'{{join_date}}'
from t_sunso_stock_day_trade_statistic_core_data
where trade_date='{{trade_date}}' and close_amt > 0
and close_pre_close_diff_amt_ratio between -2 and 0 -- 当日较前日微跌
and pre1_avg_turnover_rate_ratio < 1 -- 缩量
and pre5_avg_turnover_rate_ratio < 1 -- 较前5日平均缩量
and pre5_close_price_ratio > 0  -- 前5日涨幅大于0
and pre3_close_price_ratio > 0  -- 前3日涨幅大于0
and pre20_close_price_ratio > pre30_close_price_ratio  -- 说明30日线到20日线是下跌趋势
and pre10_close_price_ratio > pre30_close_price_ratio  -- 说明10日上涨幅度并没有超过30日线
and pre30_close_price_ratio < -10
and code not in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}')
;