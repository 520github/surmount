-- 高点往下连续两天下跌，幅度超过6，接下来2天可能会反抽，只适合接下来超短2天
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and pre10_close_price_ratio > 10
and pre20_close_price_ratio > 10
and continue_up_down_days = 2
and contiune_up_down_percent < -6
and pre1_avg_turnover_rate_ratio < 1
and open_pre_close_diff_amt_ratio >-1
and trade_date='{{trade_date}}'
;