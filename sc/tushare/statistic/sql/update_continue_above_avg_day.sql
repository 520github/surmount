update t_sunso_stock_day_trade_statistic_range_avg_data
set
continue_above_nearly5_avg_day={{continue_above_nearly5_avg_day}},
continue_above_nearly10_avg_day={{continue_above_nearly10_avg_day}},
continue_above_nearly20_avg_day={{continue_above_nearly20_avg_day}},
continue_above_nearly30_avg_day={{continue_above_nearly30_avg_day}},
continue_above_nearly60_avg_day={{continue_above_nearly60_avg_day}}
where 1 >0
and code='{{code}}'
and trade_date='{{trade_date}}'
;