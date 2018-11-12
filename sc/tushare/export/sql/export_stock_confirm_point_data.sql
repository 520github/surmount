select
t.trade_date as a_日期,
s.join_date as aa_加入日期,
'{{plate_name}}' as ab_板块,
t.name as ac_名称,
t.close_amt as n_收盘价,
t.close_pre_close_diff_amt_ratio as b_涨幅,
t.turnover_rate as c_换手率,

t.trade_amt/100000000 as d_交易金额亿,

v.large_above_trade_amt as ea_大单上交易金额,v.super_trade_amt as eb_超单交易金额,
v.large_trade_amt as ec_大单交易金额,v.medium_after_trade_amt as ed_中单后交易金额,
v.medium_before_trade_amt as ee_中单前交易金额,v.small_trade_amt as ef_小单交易金额,

t.large_above_sum_trade_amt_ratio as el_大单上占比,
v.super_sum_trade_amt_ratio as em_超单占比,
v.large_sum_trade_amt_ratio as en_大单占比,
v.medium_after_sum_trade_amt_ratio as eo_中单后占比,
v.medium_before_sum_trade_amt_ratio as ep_中单前占比,
v.small_sum_trade_amt_ratio as eq_小单占比,

t.large_above_day1_bs_diff_trade_amt/100000000 as fa_当日大单净额亿,
t.large_above_day3_bs_diff_trade_amt/100000000 as fb_3日期大单净额,
t.large_above_day5_bs_diff_trade_amt/100000000 as fc_5日期大单净额,

t.large_above_buy_trade_amt_ratio as g_大单上买单占比,
v.medium_after_buy_trade_amt_ratio as ha_中单后买单占比,
v.medium_before_buy_trade_amt_ratio as hc_中单前买单占比,
v.small_buy_trade_amt_ratio as i_小单买单占比,

t.large_above_sell_trade_amt_ratio as ia_大单上卖单占比,
v.medium_after_sell_trade_amt_ratio as ib_中单后卖单占比,
v.medium_before_sell_trade_amt_ratio as ic_中单前卖单占比,
v.small_sell_trade_amt_ratio as id_小单卖单占比,

v.large_above_buy_trade_count as k_大单上买单次数,
v.large_above_sell_trade_count as ka_大单上卖单次数,
v.medium_after_buy_trade_count as kb_中单后买单次数,
v.medium_after_sell_trade_count as kc_中单后卖单次数,
v.medium_before_buy_trade_count as kd_中单前买单次数,
v.medium_before_sell_trade_count as ke_中单前卖单次数,
v.small_buy_trade_count as kf_小单买单次数,
v.small_sell_trade_count as kg_小单卖单次数,

v.super_buy_times as la_超单买入时间,
v.super_sell_times as lb_超单卖出时间,
v.large_buy_times as lc_大单买入时间,
v.large_sell_times as ld_大单卖出时间,
t.code as y_代码,t.industry as za_行业

from t_sunso_stock_day_trade_statistic_core_data t
left join t_sunso_stock_day_trade_statistic_volume_data v
on t.code = v.code and t.trade_date = v.trade_date
left join t_sunso_stock_plate_stock s
on t.code = s.code and s.plate_name='{{plate_name}}' and s.plate_start_date='{{plate_start_date}}'
where 1 > 0
-- and t.code = '600122'
and t.code = '{{code}}'
order by t.trade_date asc
;