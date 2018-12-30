-- insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,industry,area,circulation_amt,join_date)
-- select '{{plate_name}}','{{plate_start_date}}',cd.code,cd.name,cd.industry,cd.area,round(cd.circulation_amt/10000,6),'{{join_date}}'
select cd.*
from t_sunso_stock_day_trade_statistic_core_data cd,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
        select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 1
		 ) temp  order by trade_date asc limit 1
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
) t,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
		select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 3
		 ) temp  order by trade_date asc limit 1
     )
) f,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
		select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 4
		 ) temp  order by trade_date asc limit 1
     )
) l
where 1 >0
-- and cd.code='300647'
and cd.trade_date='{{trade_date}}'
and cd.code = s.code
and s.code = t.code
and t.code = f.code
and f.code = l.code
and cd.close_amt < cd.open_amt
and cd.pre1_avg_turnover_rate_ratio > 1
and s.close_amt > s.open_amt
and s.pre1_avg_turnover_rate_ratio >1
and t.close_amt > t.open_amt
and t.pre1_avg_turnover_rate_ratio > 1
and f.close_amt > f.open_amt
and f.pre1_avg_turnover_rate_ratio > 1
and l.close_amt > l.open_amt
;