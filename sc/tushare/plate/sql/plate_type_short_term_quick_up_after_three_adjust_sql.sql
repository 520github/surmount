-- 短线(上升过程的一个中续调整)

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
,(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
		select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 3
		 ) temp  order by trade_date asc limit 1
     )
) f
where 1 >0
-- and cd.code='300251'
and cd.trade_date='{{trade_date}}'
and cd.code = s.code
and s.code = t.code
and t.code = f.code
and cd.pre1_avg_turnover_rate_ratio <1
and cd.close_pre_close_diff_amt_ratio < 0
and cd.close_amt > cd.open_amt
and s.close_pre_close_diff_amt_ratio <0
and s.pre1_avg_turnover_rate_ratio < 1
and s.close_amt < s.open_amt
and s.close_amt > f.open_amt
and t.close_pre_close_diff_amt_ratio <0
and t.pre1_avg_turnover_rate_ratio < 1
and t.high_amt > t.open_amt
-- and t.high_amt < f.high_amt
and f.close_pre_close_diff_amt_ratio > 0
and f.pre5_close_price_ratio >=15
and f.pre3_close_price_ratio >=10
;