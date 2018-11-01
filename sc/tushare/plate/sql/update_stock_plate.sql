update t_sunso_stock_plate
set total_up_down_ratio = {{total_up_down_ratio}},total_count={{total_count}},
total_up_top5_stock_name='{{total_up_top5_stock_name}}',total_down_top5_stock_name='{{total_down_top5_stock_name}}'
where 1 > 0
and plate_name='{{plate_name}}'
and plate_start_date='{{plate_start_date}}'
;