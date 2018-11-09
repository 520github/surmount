select t.trade_date as a_日期,
t.close_pre_close_diff_amt_ratio as b_涨幅,
t.open_pre_close_diff_amt_ratio as ba_开盘幅度,
t.low_pre_close_diff_amt_ratio as bb_最低幅度,
t.low_high_diff_amt_ratio as bc_高低振幅,
t.open_ten_time_ratio as bd_开盘前10分钟振幅,
t.turnover_rate as c_换手率,t.trade_amt/100000000 as d_交易金额亿,
v.large_above_buy_trade_count as f_大单上买单次数,v.large_above_sell_trade_count as fa_大单上卖单次数,
v.medium_after_buy_trade_count as fb_中单后买单次数,v.medium_after_sell_trade_count as fc_中单后卖单次数,
v.medium_before_buy_trade_count as fd_中单前买单次数,v.medium_before_sell_trade_count as fe_中单前卖单次数,
v.small_buy_trade_count as ff_小单买单次数,v.small_sell_trade_count as fg_小单卖单次数,
t.large_above_sum_trade_amt_ratio as fh_大单上占比,
t.large_above_buy_trade_amt_ratio as g_大单上买单占比,t.large_above_sell_trade_amt_ratio as h_大单上卖单占比,
v.medium_after_buy_trade_amt_ratio as ha_中单后买单占比,v.medium_after_sell_trade_amt_ratio as hb_中单后卖单占比,
v.medium_before_buy_trade_amt_ratio as hc_中单前买单占比,v.medium_before_sell_trade_amt_ratio as hd_中单前卖单占比,
v.small_buy_trade_amt_ratio as i_小单买单占比,v.small_sell_trade_amt_ratio as j_小单卖单占比,
t.large_above_day1_bs_diff_trade_amt/100000000 as k_当日大单净额亿,
t.large_above_day3_bs_diff_trade_amt/100000000 as l_3日期大单净额,
t.large_above_day5_bs_diff_trade_amt/100000000 as m_5日期大单净额,
t.close_amt as n_收盘价,t.avg_amt as o_平均价,
v.all_buy_avg_trade_price as p_买单平均价,v.pre3_all_buy_avg_trade_price as q_前3日买单平均价,v.pre5_all_buy_avg_trade_price as r_前5日买单平均价,
v.large_above_buy_avg_trade_price s_大单上买单平均价,v.super_buy_avg_trade_price as t_超单买单平均价,v.large_buy_avg_trade_price as u_大单买单平均价,
v.medium_before_buy_avg_trade_price as v_中单前买单平均价,v.medium_after_buy_avg_trade_price as w_中单后买单平均价,v.small_buy_avg_trade_price as x_小单买单平均价,
t.code as y_代码,t.name as z_名称,t.industry as za_行业
from t_sunso_stock_day_trade_statistic_core_data t left join t_sunso_stock_day_trade_statistic_volume_data v
on t.code = v.code and t.trade_date = v.trade_date
where 1 > 0
-- and t.code = '600122'
and t.code = '{{code}}'
order by t.trade_date asc
;