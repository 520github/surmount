select cd.* from t_sunso_stock_day_trade_statistic_core_data cd,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
     select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
     where trade_date<'{{trade_date}}' order by trade_date desc limit 1
     )
) t
where 1 >0
and cd.trade_date='{{trade_date}}'
and cd.code = t.code
and cd.pre3_close_price_ratio > 2
and cd.pre5_close_price_ratio > 0
and cd.pre10_close_price_ratio between 25 and 99
and cd.close_pre_close_diff_amt_ratio <=-4
and cd.pre1_avg_turnover_rate_ratio < 0.8
and t.pre1_avg_turnover_rate_ratio < 2
and t.pre10_close_price_ratio > 0
-- and t.close_pre_close_diff_amt_ratio > 0
and t.close_amt<t.open_amt
-- and t.open_amt - t.close_amt < 2
;

