insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,industry,area,circulation_amt,join_date)
select '{{plate_name}}','{{plate_start_date}}',cd.code,cd.name,cd.industry,cd.area,round(cd.circulation_amt/10000,6),'{{join_date}}'
from t_sunso_stock_day_trade_statistic_core_data cd,
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
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 3
		 ) temp  order by trade_date asc limit 1
     )
) t
where 1 >0
-- and cd.code='300420'
and cd.trade_date='{{trade_date}}'
and cd.code = s.code
and s.code = t.code
and cd.pre1_avg_turnover_rate_ratio > 1
and ((cd.open_amt-cd.low_amt)/abs(cd.close_amt-cd.open_amt))>=3
and cd.close_pre_close_diff_amt_ratio < 0
and cd.pre5_close_price_ratio <= -5
and cd.pre10_close_price_ratio <= -10
and cd.pre20_close_price_ratio <= -15
and s.pre1_avg_turnover_rate_ratio < 1
and s.pre5_close_price_ratio <= -5
and t.pre1_avg_turnover_rate_ratio < 1
;