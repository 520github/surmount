select
s.name as a_名称,
s.code as b_代码,
s.industry as c_行业,
s.area as d_地区,
round(cd.trade_amt/100000000,2) as db_交易金额,
cd.turnover_rate as df_换手率,
cd.close_pre_close_diff_amt_ratio as ea_收盘幅度,
cd.open_pre_close_diff_amt_ratio as eb_开盘价幅度,
cd.high_pre_close_diff_amt_ratio as ec_最高价幅度,
cd.pre1_avg_turnover_rate_ratio as ed_比昨日换手率,
cd.close_amt as ef_收盘价,
s.join_date as f_加入时间,
s.total_count as g_加入天数,
s.total_up_down_ratio as ga_加入之后总上涨幅度,
s.first_up_down_ratio as gb_加入第一次上涨幅度,
s.first_close_amt as gc_加入第一次收盘价,
s.last_close_amt as gd_加入最近收盘价,
s.large_above_total_bs_trade_amt as ge_大单上净额亿,
s.large_above_total_bs_trade_amt_ratio as gf_大单上占交易比例,
dtd.nearly5_day_sale_top3_count as hl_前3营业部数,
dtd.nearly5_day_sale_top1_count as hm_前1营业部数,
dtd.nearly5_day_sale_only_count as hn_独立营业数,
dtd.nearly5_day_sale_only_buy_count as ho_纯买独立营业数,
dtd.nearly5_day_sale_only_sell_count as hp_纯卖独立营业数,
dtd.today_buy_amt_ratio as hq_当日龙虎榜买入占比,
dtd.today_sell_amt_ratio as hr_当日龙虎榜卖出占比,
dtd.nearly5_day_buy_amt as hs_近5日龙虎榜买入金额,
dtd.nearly5_day_sell_amt as ht_近5日龙虎榜卖出金额

from t_sunso_stock_plate_stock s
left join t_sunso_stock_dragon_tiger_day_total_data dtd
on s.code = dtd.code and s.join_date = dtd.trade_date
left join t_sunso_stock_day_trade_statistic_core_data cd
on s.code = cd.code  and s.join_date = cd.trade_date
where 1> 0
and s.plate_name = '{{plate_name}}'
and s.plate_start_date = '{{plate_start_date}}'
order by s.created_at desc
;