insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,industry,area,circulation_amt,join_date)
select '{{plate_name}}','{{plate_start_date}}',cd.code,cd.name,cd.industry,cd.area,round(cd.circulation_amt/10000,6),'{{join_date}}'
from t_sunso_stock_day_trade_statistic_core_data cd,
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
(
select * from t_sunso_stock_day_trade_statistic_range_avg_data
where 1 >0
and trade_date = (
		select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_range_avg_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 20
		 ) temp  order by trade_date asc limit 1
     )
) t,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
		select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 30
		 ) temp  order by trade_date asc limit 1
     )
) f
where 1 >0
-- and cd.code='300420'
and cd.trade_date='{{trade_date}}'
and cd.close_pre_close_diff_amt_ratio > 0
-- and cd.pre5_close_price_ratio <=8
and cd.pre20_close_price_ratio < -10
-- and cd.pre30_close_price_ratio <=15
and cd.pre5_close_price_ratio < -5
and cd.code=rd.code
and cd.trade_date=rd.trade_date
and rd.code = s.code
and s.code = t.code
and t.code=f.code
and rd.nearly5_avg_close_price < s.nearly5_avg_close_price
and rd.nearly10_avg_close_price < s.nearly10_avg_close_price
and s.nearly10_avg_close_price < t.nearly10_avg_close_price
and f.pre10_close_price_ratio < -5
;