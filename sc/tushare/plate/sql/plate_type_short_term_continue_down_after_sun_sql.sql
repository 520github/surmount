-- 短线连续快速下跌然后一个阳线

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
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 4
		 ) temp  order by trade_date asc limit 1
     )
) t
where 1 >0
and cd.trade_date='{{trade_date}}'
and cd.code = s.code
and s.code = t.code
and cd.close_amt > cd.open_amt
and cd.close_pre_close_diff_amt_ratio > 2
and cd.pre1_avg_turnover_rate_ratio > 1
and s.close_pre_close_diff_amt_ratio < 0
and s.continue_up_down_days >= 3
and s.contiune_up_down_percent <= -10
and s.pre10_close_price_ratio between 2 and 10
and s.pre1_avg_turnover_rate_ratio < 1
and t.pre10_close_price_ratio <15
;