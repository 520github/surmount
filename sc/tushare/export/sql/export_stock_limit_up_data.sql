select
c.name as a_名称,
c.code as b_代码,
c.continue_up_limit_days as c_涨停次数,
c.up_limit_type as d_涨停类型,
c.first_limit_up_time as e_第一次涨停时间,
c.close_amt as f_收盘价,
c.pre3_close_price_ratio as g_前3日涨幅,
c.pre5_close_price_ratio as h_前5日涨幅,
c.pre10_close_price_ratio as i_前10日涨幅,
c.turnover_rate as j_换手率,
round(c.trade_amt/100000000,2) as jd_交易金额亿,
round(t.amount/10000,2) as je_龙虎榜交易金额亿,
if(t.amount=null, "",round(t.amount*10000/c.trade_amt*100,2)) as jea_龙虎榜交易金额占比,
t.buy as jf_龙虎榜买入金额,
t.sell as jl_龙虎榜卖出金额,
if(t.buy=null, "", t.buy/t.sell) as jla_龙虎榜买卖比,
t.bratio as jm_龙虎榜买入占总成交比例,
t.sratio as jn_龙虎榜卖出占总成交比例,
t.reason as jo_龙虎榜原因,
c.industry as k_行业,
c.area as l_地区

from t_sunso_stock_day_trade_statistic_core_data c
left join t_tushare_stock_dragon_tiger_today_data t
on c.code = t.code and c.trade_date = t.date


where 1 > 0
and c.up_limit_type>=10
and c.trade_date = '{{trade_date}}'
order by c.continue_up_limit_days desc
