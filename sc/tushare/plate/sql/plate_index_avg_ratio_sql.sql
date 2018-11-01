select avg(close_pre_close_diff_amt_ratio) as c
from t_sunso_stock_day_trade_statistic_core_data
where 1 > 0
and trade_date = '{{trade_date}}'
and code in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}'
);