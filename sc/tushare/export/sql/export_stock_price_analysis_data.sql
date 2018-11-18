select
t.trade_date as a_日期,
t.name as aa_名称,

t.close_amt as ab_收盘价,
round(t.close_amt*0.97,2) as ac_收盘价跌3点,
round(t.close_amt*0.95,2) as ad_收盘价跌5点,
round(t.close_amt*0.93,2) as ae_收盘价跌7点,
v.large_above_buy_low_trade_price as af_大单上买入最低价,
v.large_above_low_trade_price as ag_大单上最低价,
v.large_above_avg_trade_price as ah_大单上平均价格,
v.all_buy_avg_trade_price as ai_买单平均价,
t.avg_amt as aj_平均价,
v.all_sell_avg_trade_price as ak_卖单平均价,
v.pre3_all_buy_avg_trade_price as al_前3日买单平均价,
v.pre5_all_buy_avg_trade_price as am_前5日买单平均价,

t.close_pre_close_diff_amt_ratio as b_涨幅,
t.open_pre_close_diff_amt_ratio as ba_开盘幅度,
t.low_pre_close_diff_amt_ratio as bb_最低幅度,
t.low_high_diff_amt_ratio as bc_高低振幅,
t.open_ten_time_ratio as bd_开盘前10分钟振幅,

t.open_amt as dfa_开盘价,
t.low_amt as dfa_最低价,
t.high_amt as dfb_最高价,

v.large_above_buy_high_trade_price as dfd_大单上买入最高价,
v.large_above_high_trade_price as dff_大单上最高价,
v.super_avg_trade_price as dh_超单平均价格,
v.large_avg_trade_price as di_大单平均价格,
v.medium_after_avg_trade_price as dj_中单后平均价格,
v.medium_before_avg_trade_price as dk_中单前平均价格,
v.small_avg_trade_price as dl_小单平均价格,

v.large_above_buy_avg_trade_price s_大单上买单平均价,
v.super_buy_avg_trade_price as t_超单买单平均价,
v.large_buy_avg_trade_price as u_大单买单平均价,
v.medium_before_buy_avg_trade_price as v_中单前买单平均价,
v.medium_after_buy_avg_trade_price as w_中单后买单平均价,
v.small_buy_avg_trade_price as x_小单买单平均价,

t.code as y_代码,t.industry as za_行业,
t.turnover_rate as zb_换手率

from t_sunso_stock_day_trade_statistic_core_data t
left join t_sunso_stock_day_trade_statistic_volume_data v
on t.code = v.code and t.trade_date = v.trade_date
where 1 > 0
-- and t.code = '600122'
and t.code = '{{code}}'
order by t.trade_date asc
;