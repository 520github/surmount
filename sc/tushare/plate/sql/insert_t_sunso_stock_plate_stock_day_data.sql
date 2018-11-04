insert into t_sunso_stock_plate_stock_day_data(plate_name,plate_start_date,code,name,industry,area,
up_down_ratio,pre3_up_down_ratio,pre5_up_down_ratio,close_amt,trade_amt,net_amt,circulation_amt,
continue_up_limit_days,continue_down_limit_days,
continue_up_down_days,contiune_up_down_percent,
large_above_sum_trade_amt_ratio,large_above_buy_trade_amt_ratio,large_above_bs_trade_amt_ratio,
large_above_day1_bs_trade_amt,large_above_day1_bs_trade_amt_ratio,
large_above_day3_bs_trade_amt,large_above_day3_bs_trade_amt_ratio,
large_above_day5_bs_trade_amt,large_above_day5_bs_trade_amt_ratio,
join_days,trade_date)
select '{{plate_name}}','{{plate_start_date}}',
code,name,industry,area,close_pre_close_diff_amt_ratio,pre3_close_price_ratio,pre5_close_price_ratio,
close_amt,trade_amt,trade_net_amt,circulation_amt,
continue_up_limit_days,continue_down_limit_days,
continue_up_down_days,contiune_up_down_percent,
large_above_sum_trade_amt_ratio,large_above_buy_trade_amt_ratio,large_above_bs_trade_amt_ratio,
large_above_day1_bs_diff_trade_amt,round(large_above_day1_bs_diff_trade_amt/trade_amt*100,2),
large_above_day3_bs_diff_trade_amt,round(large_above_day3_bs_diff_trade_amt/trade_amt*100,2),
large_above_day5_bs_diff_trade_amt,round(large_above_day5_bs_diff_trade_amt/trade_amt*100,2),
(select (total_count+1) from t_sunso_stock_plate_stock t1
where t1.plate_name='{{plate_name}}' and t1.plate_start_date='{{plate_start_date}}' and t1.code=t.code
),
'{{trade_date}}'
from t_sunso_stock_day_trade_statistic_core_data t
where 1 > 0
and close_amt > 0
and trade_date = '{{trade_date}}'
and code in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}')
and code not in (select code from t_sunso_stock_plate_stock_day_data
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}' and trade_date='{{trade_date}}')
;
