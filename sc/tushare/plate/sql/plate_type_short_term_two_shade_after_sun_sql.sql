-- 短线(高点下走过程的一个中续)双阴一阳

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
and cd.pre5_close_price_ratio <-5
and cd.close_amt > cd.open_amt
and t.close_amt < t.open_amt
and s.close_pre_close_diff_amt_ratio between -5 and -1
and s.close_amt < s.open_amt
and cd.low_amt < s.low_amt
and cd.close_amt < s.close_amt
and cd.pre1_avg_turnover_rate_ratio > 1
;