insert into t_sunso_stock_plate_stock_day_data(plate_name,plate_start_date,code,name,industry,area,
up_down_ratio,pre3_up_down_ratio,pre5_up_down_ratio,close_amt,
avg_price,all_buy_avg_trade_price,all_sell_avg_trade_price,
pre3_all_buy_avg_trade_price,pre3_all_sell_avg_trade_price,
pre5_all_buy_avg_trade_price,pre5_all_sell_avg_trade_price,
large_above_buy_avg_trade_price,super_buy_avg_trade_price,large_buy_avg_trade_price,
medium_before_buy_avg_trade_price,medium_after_buy_avg_trade_price,small_buy_avg_trade_price,
pre3_large_above_buy_avg_trade_price,pre3_super_buy_avg_trade_price,pre3_large_buy_avg_trade_price,
pre3_medium_before_buy_avg_trade_price,pre3_medium_after_buy_avg_trade_price,pre3_small_buy_avg_trade_price,
pre5_large_above_buy_avg_trade_price,pre5_super_buy_avg_trade_price,pre5_large_buy_avg_trade_price,
pre5_medium_before_buy_avg_trade_price,pre5_medium_after_buy_avg_trade_price,pre5_small_buy_avg_trade_price,
trade_amt,net_amt,circulation_amt,
continue_up_limit_days,continue_down_limit_days,
continue_up_down_days,contiune_up_down_percent,
large_above_sum_trade_amt_ratio,large_above_buy_trade_amt_ratio,large_above_bs_trade_amt_ratio,
large_above_day1_bs_trade_amt,large_above_day1_bs_trade_amt_ratio,
large_above_day3_bs_trade_amt,large_above_day3_bs_trade_amt_ratio,
large_above_day5_bs_trade_amt,large_above_day5_bs_trade_amt_ratio,
join_days,trade_date)
select '{{plate_name}}','{{plate_start_date}}',
t.code,t.name,t.industry,t.area,t.close_pre_close_diff_amt_ratio,t.pre3_close_price_ratio,t.pre5_close_price_ratio,
t.close_amt,t.avg_amt,
v.all_buy_avg_trade_price,v.all_sell_avg_trade_price,v.pre3_all_buy_avg_trade_price,
v.pre3_all_sell_avg_trade_price,v.pre5_all_buy_avg_trade_price,v.pre5_all_sell_avg_trade_price,
v.large_above_buy_avg_trade_price,v.super_buy_avg_trade_price,v.large_buy_avg_trade_price,
v.medium_before_buy_avg_trade_price,v.medium_after_buy_avg_trade_price,v.small_buy_avg_trade_price,
v.pre3_large_above_buy_avg_trade_price,v.pre3_super_buy_avg_trade_price,v.pre3_large_buy_avg_trade_price,
v.pre3_medium_before_buy_avg_trade_price,v.pre3_medium_after_buy_avg_trade_price,v.pre3_small_buy_avg_trade_price,
v.pre5_large_above_buy_avg_trade_price,v.pre5_super_buy_avg_trade_price,v.pre5_large_buy_avg_trade_price,
v.pre5_medium_before_buy_avg_trade_price,v.pre5_medium_after_buy_avg_trade_price,v.pre5_small_buy_avg_trade_price,
t.trade_amt,t.trade_net_amt,t.circulation_amt,
t.continue_up_limit_days,t.continue_down_limit_days,
t.continue_up_down_days,t.contiune_up_down_percent,
t.large_above_sum_trade_amt_ratio,t.large_above_buy_trade_amt_ratio,t.large_above_bs_trade_amt_ratio,
t.large_above_day1_bs_diff_trade_amt,round(t.large_above_day1_bs_diff_trade_amt/trade_amt*100,2),
t.large_above_day3_bs_diff_trade_amt,round(t.large_above_day3_bs_diff_trade_amt/trade_amt*100,2),
t.large_above_day5_bs_diff_trade_amt,round(t.large_above_day5_bs_diff_trade_amt/trade_amt*100,2),
(select (total_count+1) from t_sunso_stock_plate_stock t1
where t1.plate_name='{{plate_name}}' and t1.plate_start_date='{{plate_start_date}}' and t1.code=t.code
),
'{{trade_date}}'
from t_sunso_stock_day_trade_statistic_core_data t left join t_sunso_stock_day_trade_statistic_volume_data v
on t.code = v.code and t.trade_date = v.trade_date
where 1 > 0
and t.close_amt > 0
and t.trade_date = '{{trade_date}}'
and t.code in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}')
and t.code not in (select code from t_sunso_stock_plate_stock_day_data
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}' and trade_date='{{trade_date}}')
;
