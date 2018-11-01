select  group_concat(name) as c from (
 select * from t_sunso_stock_plate_stock_day_data
 where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}' and trade_date='{{trade_date}}'
 order by up_down_ratio asc limit 5
 ) as t
;