insert into t_sunso_stock_plate_day_data
(plate_name,plate_start_date,avg_ratio,tap_ratio,mid_ratio,up_limit_count,
down_limit_count,up_count,down_count,up_down_count_ratio,net_amt,
up_top5_stock_name,down_top5_stock_name,trade_date)
values('{{plate_name}}','{{plate_start_date}}',{{avg_ratio}},{{tap_ratio}},
{{mid_ratio}},{{up_limit_count}},{{down_limit_count}},{{up_count}},
{{down_count}},{{up_down_count_ratio}},{{net_amt}}
,'{{up_top5_stock_name}}','{{down_top5_stock_name}}','{{trade_date}}')
;