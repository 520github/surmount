-- 短线葵花向阳

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
and cd.pre10_close_price_ratio between 10 and 99
and cd.close_pre_close_diff_amt_ratio > 0
and cd.open_amt between t.close_amt and t.open_amt
and cd.close_amt > t.open_amt
and t.continue_up_down_days =1
and cd.close_amt < t.pre_close_amt
and t.pre1_avg_turnover_rate_ratio < 1
and cd.pre1_avg_turnover_rate_ratio > 1
and t.open_amt < t.pre_close_amt
;