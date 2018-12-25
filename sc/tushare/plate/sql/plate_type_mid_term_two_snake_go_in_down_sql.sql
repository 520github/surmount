-- 中线双蛇出动
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
and cd.pre5_close_price_ratio between 5 and 10
and cd.pre10_close_price_ratio < 0
-- and cd.pre5_close_price_ratio < 0
-- and cd.pre20_close_price_ratio < -10
-- and cd.pre30_close_price_ratio < -10
-- and cd.pre20_close_price_ratio > cd.pre30_close_price_ratio
-- and cd.pre10_close_price_ratio between 5 and 10
-- and cd.pre20_close_price_ratio between 10 and 20
-- and cd.close_pre_close_diff_amt_ratio between 0 and 0.5
-- and cd.continue_up_down_days =2
and abs(cd.open_amt - t.open_amt) between 0 and 0.1
and abs(cd.close_amt - t.close_amt) between 0 and 0.1
-- and t.close_pre_close_diff_amt_ratio between 1 and 5
and t.close_amt > t.open_amt
and cd.close_amt > cd.open_amt
and round((t.close_amt - t.open_amt)/t.open_amt*100,2) > 2
and round((cd.close_amt - cd.open_amt)/cd.open_amt*100,2) > 2
and abs((t.close_amt - t.open_amt) - (cd.close_amt - cd.open_amt)) between 0 and 0.5
;