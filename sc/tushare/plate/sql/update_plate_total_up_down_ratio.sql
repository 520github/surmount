update t_sunso_stock_plate set total_up_down_ratio = {{total_up_down_ratio}}
where 1 > 0
and plate_name='{{plate_name}}'
and plate_start_date='{{plate_start_date}}'
;