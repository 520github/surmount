select
'{{industry}}' as a_行业,
trade_date as b_交易日期,
avg_close_price_ratio as c_当日平均涨幅,
sum_up_count as cf_上涨数,
sum_down_count as ch_下跌数,
pre1_totals_stock_amt_ratio as f_市值较前1日增幅,
pre3_totals_stock_amt_ratio as fb_市值较前3日增幅,
pre5_totals_stock_amt_ratio as fc_市值较前5日增幅,
pre10_totals_stock_amt_ratio as fd_市值较前10日增幅,
pre20_totals_stock_amt_ratio as fe_市值较前20日增幅,
totals_stock_amt as h_当日总市值,
trade_volume as hb_当日总交易手数,
trade_count as hc_当日总交易次数,
stock_num as j_行业股票数
from t_sunso_stock_day_industry_statistic_core_data id
where 1 > 0
and industry='{{industry}}'
;