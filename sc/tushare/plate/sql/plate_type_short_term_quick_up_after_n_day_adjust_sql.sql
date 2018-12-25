-- 短线(上升过程的一个中续调整)

select cd.* from t_sunso_stock_day_trade_statistic_core_data cd,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
        select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 1
		 ) temp  order by trade_date asc limit 1
     )
) o,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
        select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 5
		 ) temp  order by trade_date asc limit 1
     )
) s,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
		select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 15
		 ) temp  order by trade_date asc limit 1
     )
) t
where 1 >0
-- and cd.code='300420'
and cd.trade_date='{{trade_date}}'
and cd.code = o.code
and cd.code = s.code
and s.code = t.code
and cd.pre5_avg_turnover_rate_ratio < 1
and cd.pre5_close_price_ratio <=-10
and cd.pre20_close_price_ratio >=-5
and cd.close_amt > cd.open_amt
and o.close_pre_close_diff_amt_ratio < 0
and o.continue_up_down_days >=2
and o.pre1_avg_turnover_rate_ratio < 1
and s.pre5_close_price_ratio between 5 and 10
and s.pre10_close_price_ratio between 5 and 20
and s.pre20_close_price_ratio >= 15
and t.pre10_close_price_ratio between 10 and 20
-- and t.pre20_close_price_ratio < t.pre10_close_price_ratio
-- and t.pre20_close_price_ratio <2
;