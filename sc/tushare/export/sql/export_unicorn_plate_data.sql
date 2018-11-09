select name as a_名称,trade_date as a_交易日期,continue_up_limit_days as a_涨停天数,up_limit_type as b_涨停类型,first_limit_up_time as c_涨停时间,
circulation_amt as d_流通盘,close_amt as e_价格,turnover_rate as f_换手率,
trade_amt as g_交易金额,
large_above_day1_bs_trade_amt as ga_当日大单上净流入金额,
large_above_day3_bs_trade_amt as gb_近3日大单上净流入金额,
large_above_day5_bs_trade_amt as gc_近5日大单上净流入金额,
round(trade_amt*large_above_buy_trade_amt_ratio/100,4) as h_大单上买入金额,
round(trade_amt*large_above_sell_trade_amt_ratio/100,4) as i_大单上卖出金额,
round(trade_amt*medium_after_buy_trade_amt_ratio/100,4) as j_中单后买入金额,
round(trade_amt*medium_after_sell_trade_amt_ratio/100,4) as k_中单后卖出金额,
round(trade_amt*medium_before_buy_trade_amt_ratio/100,4) as l_中单前买入金额,
round(trade_amt*medium_before_sell_trade_amt_ratio/100,4) as m_中单前卖出金额,
round(trade_amt*small_buy_trade_amt_ratio/100,4) as n_小单买入金额,
round(trade_amt*small_sell_trade_amt_ratio/100,4) as o_小单卖出金额,
large_above_sum_trade_amt_ratio as p_大单上占比,
large_above_buy_trade_amt_ratio as r_大单买入占比,
large_above_sell_trade_amt_ratio as s_大单卖出占比,
medium_after_buy_trade_amt_ratio as t_中单后买入占比,
medium_after_sell_trade_amt_ratio as u_中单后卖出占比,
medium_before_buy_trade_amt_ratio as v_中单前买入占比,
medium_before_sell_trade_amt_ratio as w_中单前卖出占比,
small_buy_trade_amt_ratio as y_小单买入占比,
small_sell_trade_amt_ratio as z_小单卖出占比
from t_sunso_stock_plate_stock_day_data
where 1 > 0
and code='{{code}}'
and plate_name='{{plate_name}}'
and plate_start_date = '{{plate_start_date}}'