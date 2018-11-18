select
'{{trade_date}}' as aa_交易日期,
cd.name as ab_名称,
cd.code as ac_code,
cd.close_amt as ad_收盘价,
round(cd.circulation_amt/10000,2) as ae_流通盘,
cd.close_pre_close_diff_amt_ratio as b_涨幅,
cd.open_pre_close_diff_amt_ratio as ba_开盘幅度,
cd.low_pre_close_diff_amt_ratio as baa_最低幅度,
cd.high_pre_close_diff_amt_ratio as bab_最高幅度,
cd.low_high_diff_amt_ratio as bac_低高幅度,
dtd.nearly5_day_sale_top3_count as dl_前3营业部数,
dtd.nearly5_day_sale_top1_count as dm_前1营业部数,
dtd.nearly5_day_sale_only_count as dn_独立营业数,
dtd.nearly5_day_sale_only_buy_count as do_纯买独立营业数,
dtd.nearly5_day_sale_only_sell_count as dp_纯卖独立营业数,
dtd.today_buy_amt_ratio as dq_当日龙虎榜买入占比,
dtd.today_sell_amt_ratio as dr_当日龙虎榜卖出占比,
dtd.nearly5_day_buy_amt as ds_近5日龙虎榜买入金额,
dtd.nearly5_day_sell_amt as dt_近5日龙虎榜卖出金额

from  tushare.t_sunso_stock_day_trade_statistic_core_data cd
left join t_sunso_stock_dragon_tiger_day_total_data dtd
on cd.code = dtd.code and dtd.trade_date = '{{trade_date}}'
where 1>0
and  cd.trade_date='{{trade_date}}'
and cd.low_high_diff_amt_ratio > 10  -- 高低幅度超过10
and cd.down_limit_type<=0   -- 非跌停
and cd.open_pre_close_diff_amt_ratio between -7 and -1  -- 开盘价
and cd.open_pre_close_diff_amt_ratio > cd.low_pre_close_diff_amt_ratio  -- 开盘价大于最低价
and cd.close_pre_close_diff_amt_ratio > 0 -- 收盘价大于0
and abs(cd.low_pre_close_diff_amt_ratio ) - abs(cd.open_pre_close_diff_amt_ratio ) >1 -- 开盘价高于收盘价1个点以上

order by cd.open_pre_close_diff_amt_ratio asc


