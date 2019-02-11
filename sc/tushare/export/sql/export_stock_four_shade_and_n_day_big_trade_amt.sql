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
cd.turnover_rate as ca_当日换手率,
t.turnover_rate as caa_近N日平均换手率,
round(cd.trade_amt/100000000,2) as caad_当日交易金额,
t.trade_amt as caag_平均交易金额,
round(cd.circulation_amt/10000,2) as cb_流通市值亿,
round(cd.market_cap_amt/10000,2) as cc_总市值亿,
fi.earnings_per_share as ff_每股收益,
-- fi.cash_flow_per_share as fh_每股现金流量,
fi.main_business_per_share as fl_每股主营业务收入元,
fi.business_income as ft_营业收入百万,
fi.rise_main_business_income_ratio as fu_主营业务收入增长率,
fi.net_profits as ga_净利润百万,
fi.profits_yy_ratio as gb_净利润同比,
fi.net_profit_ratio as gc_净利率,
fi.rise_net_profit_ratio as gd_净利润增长率
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
) two,
(
select * from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date = (
        select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit 3
		 ) temp  order by trade_date asc limit 1
     )
) three,
(
select code,round(avg(turnover_rate),2) as turnover_rate,
round(avg(trade_amt)/100000000,2) as trade_amt
from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date > (
        select trade_date from (
			 select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
			 where trade_date<'{{trade_date}}' order by trade_date desc limit {{limit}}
		 ) temp  order by trade_date asc limit 1
     )
group by code
) t
left join t_sunso_stock_foundation_index fi
on t.code = fi.code and fi.year={{year}} and fi.quarter={{quarter}}

where 1 >0
and cd.trade_date='{{trade_date}}'
and cd.code = s.code
and s.code = two.code
and two.code=three.code
and three.code = t.code
and cd.close_pre_close_diff_amt_ratio < 0
and s.close_pre_close_diff_amt_ratio < 0
and two.close_pre_close_diff_amt_ratio < 0
and three.close_pre_close_diff_amt_ratio < 0
and t.trade_amt >= 1
and t.turnover_rate >= 3
and fi.rise_net_profit_ratio>0
and fi.rise_main_business_income_ratio > 0
order by fi.net_profits desc
;