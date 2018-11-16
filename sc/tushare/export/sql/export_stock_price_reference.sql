
select
'{{type_name}}' as a_类型,
d.trade_date as aa_日期,
d.code as ab_代码,
d.name as b_名称,

(select round((t.open_amt-d.close_amt)/d.close_amt*100,2) from t_sunso_stock_day_trade_statistic_core_data t
where t.code=d.code and t.trade_date > d.trade_date
order by t.trade_date asc limit 1
) as ba_第二日开盘幅度,

(select round((t.low_amt-d.close_amt)/d.close_amt*100,2) from t_sunso_stock_day_trade_statistic_core_data t
where t.code=d.code and t.trade_date > d.trade_date
order by t.trade_date asc limit 1
) as bb_第二日最低幅度,

(select round((t.high_amt-d.close_amt)/d.close_amt*100,2) from t_sunso_stock_day_trade_statistic_core_data t
where t.code=d.code and t.trade_date > d.trade_date
order by t.trade_date asc limit 1
) as bc_第二日最高幅度,

(select round((t.low_amt - t.high_amt)/t.high_amt*100,2) from t_sunso_stock_day_trade_statistic_core_data t
where t.code=d.code and t.trade_date > d.trade_date
order by t.trade_date asc limit 1
) as bd_第二日底稿幅度,

(select round((t.close_amt-d.close_amt)/d.close_amt*100,2) from t_sunso_stock_day_trade_statistic_core_data t
where t.code=d.code and t.trade_date > d.trade_date
order by t.trade_date asc limit 1
) as be_第二日收盘幅度,

d.close_pre_close_diff_amt_ratio as ca_涨幅,
d.open_pre_close_diff_amt_ratio as cb_开盘幅度,
d.low_pre_close_diff_amt_ratio as cd_最低幅度,
d.low_high_diff_amt_ratio as ce_高低振幅,
d.open_ten_time_ratio as cf_开盘前10分钟振幅,

d.close_amt as d_收盘价,
-- concat("=(",d.close_amt,"-",d.close_amt,")/",d.close_amt,"*100") as da_价格模拟,
d.low_amt as db_最低价,
round(close_amt*0.97,2) as ea_高开买入价1,
round(close_amt*0.95,2) as eb_高开买入价2,
round(close_amt*0.95,2) as ec_低开买入价1,
round(close_amt*0.93,2) as ed_低开买入价2,

0 as eh_当日买入价,
"=0*(1+0.05)" as em_当日买入价5点盈利,
"=0*(1+0.07)" as en_当日买入价7点盈利,
"=0*(1+0.09)" as en_当日买入价9点盈利,
if(open_pre_close_diff_amt_ratio>0 and d.low_amt<=round(pre_close_amt*0.97,2), "高开满足", "") as fa_高开情况,
if(open_pre_close_diff_amt_ratio<=0 and d.low_amt<=round(pre_close_amt*0.95,2), "低开满足", "") as fb_低开情况,
if(open_pre_close_diff_amt_ratio>0 and d.low_amt>round(pre_close_amt*0.97,2), round((low_amt-round(pre_close_amt*0.97,2))*100/pre_close_amt,2), -1) as fc_高开缺比例,
if(open_pre_close_diff_amt_ratio<=0 and d.low_amt>round(pre_close_amt*0.95,2), round((low_amt-round(pre_close_amt*0.95,2))*100/pre_close_amt,2), -1) as fd_低开缺比例

from t_sunso_stock_day_trade_statistic_core_data d
where 1 > 0
and d.code = '{{code}}'