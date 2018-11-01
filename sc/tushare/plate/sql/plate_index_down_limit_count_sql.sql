select count(*) as c
from t_sunso_stock_day_trade_statistic_core_data
where 1 > 0
and trade_date = '{{trade_date}}'
and down_limit_type>=10
and code in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}'
);