select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date='{{trade_date}}'
and pre1_avg_turnover_rate_ratio < 1
and contiune_up_down_percent < -4
and continue_up_down_days = 1
and pre20_close_price_ratio < -15
and pre5_close_price_ratio > -1
;