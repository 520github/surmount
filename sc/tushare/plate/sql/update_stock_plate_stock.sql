update t_sunso_stock_plate_stock
set total_up_down_ratio={{total_up_down_ratio}},total_count={{total_count}},avg_up_down_ratio={{avg_up_down_ratio}},
large_above_total_bs_trade_amt={{large_above_total_bs_trade_amt}},large_above_total_bs_trade_amt_ratio={{large_above_total_bs_trade_amt_ratio}},
first_up_down_ratio={{first_up_down_ratio}},first_pre3_up_down_ratio={{first_pre3_up_down_ratio}},first_pre5_up_down_ratio={{first_pre5_up_down_ratio}},
last_pre3_up_down_ratio={{last_pre3_up_down_ratio}},last_pre5_up_down_ratio={{last_pre5_up_down_ratio}},
first_close_amt={{first_close_amt}},last_close_amt={{last_close_amt}},last_first_close_amt_ratio={{last_first_close_amt_ratio}},
last_circulation_amt={{last_circulation_amt}},large_above_total_bs_trade_last_circulatio_ratio={{large_above_total_bs_trade_last_circulatio_ratio}}
where 1 > 0
and plate_name='{{plate_name}}'
and plate_start_date='{{plate_start_date}}'
and code = '{{code}}'
;