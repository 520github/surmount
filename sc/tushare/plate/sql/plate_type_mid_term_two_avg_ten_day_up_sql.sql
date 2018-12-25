-- 中线连续2个10日平均收盘价，一个比一个高

select cd.* from t_sunso_stock_day_trade_statistic_core_data cd,
t_sunso_stock_day_trade_statistic_range_avg_data rd,
(
select * from t_sunso_stock_day_trade_statistic_range_avg_data
where 1 >0
and trade_date = (
		select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_range_avg_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 10
		 ) temp  order by trade_date asc limit 1
     )
) s,
t_sunso_stock_day_trade_statistic_core_data scd
where 1 >0
-- and cd.code='300420'
and cd.trade_date='{{trade_date}}'
and cd.code = rd.code
and cd.trade_date = rd.trade_date
and cd.close_pre_close_diff_amt_ratio > 0
and cd.close_amt > cd.open_amt
and cd.pre5_close_price_ratio between -2 and 2
and cd.pre10_close_price_ratio > 5
and cd.pre20_close_price_ratio > cd.pre10_close_price_ratio
and cd.code=s.code
and s.code = scd.code
and s.trade_date=scd.trade_date
and rd.nearly10_avg_close_price > s.nearly10_avg_close_price
and scd.pre10_close_price_ratio > 0
and scd.pre20_close_price_ratio <= -5
;