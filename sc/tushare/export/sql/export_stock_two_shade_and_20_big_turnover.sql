select
'{{trade_date}}' as a_交易日期,
cd.code as aa_代码,
cd.name as ab_名称,
cd.industry as ac_行业,
cd.area as ad_地区,
cd.close_amt as ba_收盘价,
cd.pre_close_amt as bb_前日收盘价,
cd.close_pre_close_diff_amt_ratio as bc_当日涨幅,
cd.pre5_close_price_ratio as bfa_前5日涨幅,
cd.pre10_close_price_ratio as bfb_前10日涨幅,
cd.pre20_close_price_ratio as bfc_前20日涨幅,
cd.pre30_close_price_ratio as bfd_前30日涨幅,
cd.turnover_rate as ca_换手率,
round(cd.circulation_amt/10000,2) as cb_流通市值亿,
round(cd.market_cap_amt/10000,2) as cc_总市值亿
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
select code,avg(turnover_rate) as turnover_rate
from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date > (
        select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 20
		 ) temp  order by trade_date asc limit 1
     )
group by code
) t

where 1 >0
and cd.trade_date='{{trade_date}}'
and cd.code = s.code
and s.code = t.code
and cd.close_pre_close_diff_amt_ratio < 0
and s.close_pre_close_diff_amt_ratio < 0
and t.turnover_rate >= 8
order by cd.turnover_rate desc
;