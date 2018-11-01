insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,join_date)
select '{{plate_name}}','{{plate_start_date}}',code,name,'{{join_date}}'
from t_sunso_stock_day_trade_statistic_core_data
where trade_date='{{trade_date}}' and up_limit_type >=10
and code not in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}')
;