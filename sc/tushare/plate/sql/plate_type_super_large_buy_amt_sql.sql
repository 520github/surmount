insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,industry,area,circulation_amt,join_date)
select '{{plate_name}}','{{plate_start_date}}',code,name,industry,area,round(circulation_amt/10000,6),'{{join_date}}'
from t_sunso_stock_day_trade_statistic_core_data
where trade_date='{{trade_date}}' and close_amt > 0
and large_above_sum_trade_amt_ratio > 20
and large_above_bs_trade_amt_ratio > 2
and large_above_day1_bs_diff_trade_amt  > 0
and large_above_day1_bs_diff_trade_amt > large_above_day5_bs_diff_trade_amt
and large_above_day1_bs_diff_trade_amt >= 50000000
and market_cap_amt < 5000000
and code not in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}')
order by large_above_day1_bs_diff_trade_amt desc
;