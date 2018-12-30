-- 短线三阳

select cd.* from t_sunso_stock_day_trade_statistic_core_data cd,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
     select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
     where trade_date<'{{trade_date}}' order by trade_date desc limit 1
     )
) s
where 1 >0
-- and cd.code='300420'
and cd.trade_date='{{trade_date}}'
and cd.code = s.code
and cd.close_pre_close_diff_amt_ratio > 0
and cd.open_amt < cd.pre_close_amt
and cd.close_amt < cd.pre_close_amt
and cd.close_amt < cd.open_amt
and cd.high_amt < cd.pre_close_amt
and cd.close_amt > s.open_amt
and s.up_limit_type=10
and s.pre1_avg_turnover_rate_ratio < 3
and cd.low_amt > s.low_amt
;