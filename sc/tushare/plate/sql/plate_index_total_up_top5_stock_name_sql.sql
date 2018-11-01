select group_concat(name) as c  from (
select * from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}'
order by total_up_down_ratio desc limit 5
) as t
;