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
c.industry as k_行业,
c.area as l_地区

from t_sunso_stock_day_trade_statistic_core_data c

where 1 > 0
and c.up_limit_type>=10
and c.trade_date = '{{trade_date}}'
order by c.continue_up_limit_days desc
