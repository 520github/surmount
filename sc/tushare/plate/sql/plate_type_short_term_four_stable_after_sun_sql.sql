-- 短线四平稳后一阳

select cd.* from t_sunso_stock_day_trade_statistic_core_data cd,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
		select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 4
		 ) temp  order by trade_date asc limit 1
     )
) t,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
		select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 40
		 ) temp  order by trade_date asc limit 1
     )
) t
where 1 >0
-- and cd.code='300420'
and cd.trade_date='{{trade_date}}'
and cd.code = t.code
and cd.pre1_avg_turnover_rate_ratio > 1
and cd.close_pre_close_diff_amt_ratio >0
and cd.pre10_close_price_ratio >5
and cd.pre10_close_price_ratio > cd.pre30_close_price_ratio
and cd.close_amt > cd.open_amt
and t.pre10_close_price_ratio between 5 and 15
and t.pre5_close_price_ratio between 5 and 15
and (abs(t.close_amt-cd.close_amt)/cd.close_amt*100) between 0 and 1
;