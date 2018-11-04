select {{pre_column_name}} as c from (
select * from t_sunso_stock_plate_stock_day_data
where 1 > 0
and plate_name='{{plate_name}}'
and plate_start_date='{{plate_start_date}}'
and code = '{{code}}'
order by trade_date {{sort}} limit 1
) as t
;