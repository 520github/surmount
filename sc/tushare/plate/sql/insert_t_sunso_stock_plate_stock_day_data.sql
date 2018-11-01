insert into t_sunso_stock_plate_stock_day_data(plate_name,plate_start_date,code,name,
up_down_ratio,net_amt,continue_up_limit_days,continue_down_limit_days,trade_date)
select '{{plate_name}}','{{plate_start_date}}',
code,name,close_pre_close_diff_amt_ratio,trade_net_amt,
continue_up_limit_days,continue_down_limit_days,'{{trade_date}}'
from t_sunso_stock_day_trade_statistic_core_data
where 1 > 0
and trade_date = '{{trade_date}}'
and code in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}')
and code not in (select code from t_sunso_stock_plate_stock_day_data
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}' and trade_date='{{trade_date}}')
;
