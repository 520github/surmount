select
code as a_代码,name as b_名称,area as c_地区,
round(circulation_amt/10000,2) as d_流通市值,close_amt as e_收盘价,
pre1_close_price_ratio as f_前1日涨幅,
pre3_close_price_ratio as g_前3日涨幅,
pre5_close_price_ratio as h_前5日涨幅,
 (
    select round(avg(turnover_rate),2) from t_sunso_stock_day_trade_statistic_core_data d
    where 1 > 0
    and d.code = t.code
    and d.trade_date between DATE_SUB(STR_TO_DATE('{{trade_date}}',"%Y-%m-%d"), INTERVAL {{limit}} DAY)  and STR_TO_DATE('{{trade_date}}',"%Y-%m-%d")
 ) as i_前5日平均换手率,
 (
    select round(avg(trade_amt/100000000),2) from t_sunso_stock_day_trade_statistic_core_data d
    where 1 > 0
    and d.code = t.code
    and d.trade_date between DATE_SUB(STR_TO_DATE('{{trade_date}}',"%Y-%m-%d"), INTERVAL {{limit}} DAY)  and STR_TO_DATE('{{trade_date}}',"%Y-%m-%d")
 ) as j_前5日平均交易金额

from  t_sunso_stock_day_trade_statistic_core_data t
where 1 > 0
and trade_date='{{trade_date}}'
and industry=(select industry from t_sunso_stock_day_trade_statistic_core_data where code='{{code}}' and trade_date = '{{trade_date}}')
order by circulation_amt asc