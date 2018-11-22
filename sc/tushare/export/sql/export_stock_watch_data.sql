select t.trade_date as a_日期,t.name as aa_名称,
t.close_amt as ab_收盘价,
t.circulation_amt as ac_流通盘,
t.area as ad_地区,t.industry as ae_地区,
t.pre3_close_price_ratio as af_前3价格幅度,
t.pre5_close_price_ratio as af_前5价格幅度,
t.close_pre_close_diff_amt_ratio as b_涨幅,

t.open_pre_close_diff_amt_ratio as ba_开盘幅度,
t.low_pre_close_diff_amt_ratio as baa_最低幅度,
t.high_pre_close_diff_amt_ratio as bab_最高幅度,
t.low_high_diff_amt_ratio as bac_低高幅度,
t.up_limit_type as bc_涨停方式,
t.first_limit_up_time as bd_涨停时间,
t.turnover_rate as c_换手率,t.trade_amt/100000000 as d_交易金额亿,
v.large_above_trade_count as da_大单上次数,
v.large_above_buy_trade_count as dab_大单上买单次数,
v.large_above_sell_trade_count as dac_大单上卖单次数,

v.sum_buy_trade_amt_ratio as dba_总买盘占比,
v.sum_sell_trade_amt_ratio as dbb_总卖盘占比,

-- v.large_above_trade_amt as dc_大单上金额,
-- v.super_trade_amt as dd_超级大单金额,
-- v.large_trade_amt as de_大单金额,
-- v.medium_after_trade_amt as df_中单后金额,
-- v.medium_before_trade_amt as dg_中单前金额,
-- v.small_trade_amt as dh_小单金额,

v.large_above_sum_trade_amt_ratio as dc_大单上金占比 ,
v.super_sum_trade_amt_ratio as dd_超级大单金额占比,
v.large_sum_trade_amt_ratio as de_大单金额占比,
v.medium_after_sum_trade_amt_ratio as df_中单后金额占比,
v.medium_before_sum_trade_amt_ratio as dg_中单前金额占比,
v.small_sum_trade_amt_ratio as dh_小单金额占比,

v.large_above_buy_trade_amt as zc_大单上买入金额,v.super_buy_trade_amt as zd_超级大单买入金额,
v.large_buy_trade_amt as ze_大单买入金额,v.medium_after_buy_trade_amt as zf_中单后买入金额,
v.medium_before_buy_trade_amt as zg_中单前买入金额,v.small_buy_trade_amt as zh_小单买入金额,

v.large_above_sell_trade_amt as zi_大单上卖出金额,v.super_sell_trade_amt as zj_超级大单卖出金额,
v.large_sell_trade_amt as zk_大单卖出金额,v.medium_after_sell_trade_amt as zl_中单后卖出金额,
v.medium_before_sell_trade_amt as zm_中单前卖出金额,v.small_sell_trade_amt as zn_小单卖出金额
from t_sunso_stock_day_trade_statistic_core_data t
left join t_sunso_stock_day_trade_statistic_volume_data v
on t.code = v.code and t.trade_date = v.trade_date
where 1 > 0
-- and t.code = '600122'
and t.code = '{{code}}'
order by t.trade_date asc
;