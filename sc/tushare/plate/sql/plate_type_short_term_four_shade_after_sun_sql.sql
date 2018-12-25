-- 短线四阴一阳

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
-- and cd.code='300420'
and cd.trade_date='{{trade_date}}'
and cd.code = s.code
and s.code = t.code
and cd.pre10_close_price_ratio >=7
and cd.pre5_close_price_ratio<=0
and cd.pre20_close_price_ratio < 20
and cd.pre30_close_price_ratio < 30
and cd.close_pre_close_diff_amt_ratio > 0
and cd.close_amt > cd.open_amt
and s.close_amt < s.open_amt
and t.close_amt < t.open_amt
and t.close_pre_close_diff_amt_ratio < 0
and t.continue_up_down_days = 3
;