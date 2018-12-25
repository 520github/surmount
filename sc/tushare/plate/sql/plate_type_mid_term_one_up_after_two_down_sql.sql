-- 中幅上涨之后，后续连续2次下跌

select cd.* from t_sunso_stock_day_trade_statistic_core_data cd,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
     select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
     where trade_date<'{{trade_date}}' order by trade_date desc limit 1
     )
) s,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
		select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 2
		 ) temp  order by trade_date asc limit 1
     )
) t
where 1 >0
-- and cd.code='300251'
and cd.trade_date='{{trade_date}}'
and cd.code = s.code
and s.code = t.code
and cd.pre5_close_price_ratio > 5
and cd.pre10_close_price_ratio >10
-- and cd.pre20_close_price_ratio < cd.pre10_close_price_ratio
and t.close_pre_close_diff_amt_ratio > 5
and s.close_pre_close_diff_amt_ratio < 0
and abs(s.high_amt - t.close_amt) <0.05
and s.low_amt > t.open_amt
and cd.close_pre_close_diff_amt_ratio < 0
and abs(cd.open_amt - s.close_amt) < 0.05
and cd.pre1_avg_turnover_rate_ratio < 1
and s.pre1_avg_turnover_rate_ratio < 1
and t.low_high_diff_amt_ratio < 10
;