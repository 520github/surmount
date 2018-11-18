insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,industry,area,circulation_amt,join_date)
select '{{plate_name}}','{{plate_start_date}}',code,name,industry,area,round(circulation_amt/10000,6),'{{join_date}}'
from t_sunso_stock_day_trade_statistic_core_data
where 1 > 0
and trade_date='{{trade_date}}'
and close_amt > 0
and up_limit_type=20
and low_high_diff_amt_ratio > 5
and pre1_avg_turnover_rate_ratio > 1
and open_pre_close_diff_amt_ratio = close_pre_close_diff_amt_ratio
;