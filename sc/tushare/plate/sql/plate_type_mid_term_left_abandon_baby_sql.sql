-- 中线左弃婴（中间十字星与左侧K线远离）

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
and cd.up_limit_type <=0
and cd.close_amt - cd.open_amt > 0.5
and cd.pre1_avg_turnover_rate_ratio > 1
and cd.pre20_close_price_ratio < -5
and cd.pre30_close_price_ratio < -5
-- and cd.low_amt > s.open_amt
and cd.low_amt < s.high_amt
and s.pre5_close_price_ratio < 0
and t.close_amt < t.open_amt
and t.close_pre_close_diff_amt_ratio < 0
and t.low_amt > s.high_amt
order by cd.pre20_close_price_ratio asc
;