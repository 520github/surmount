
select
'{{type_name}}' as a_类型,
d.trade_date as aa_日期,
d.code as ab_代码,
d.name as b_名称,

d.close_pre_close_diff_amt_ratio as ca_涨幅,
d.open_pre_close_diff_amt_ratio as cb_开盘幅度,
d.low_pre_close_diff_amt_ratio as cd_最低幅度,
d.low_high_diff_amt_ratio as ce_高低振幅,
d.open_ten_time_ratio as cf_开盘前10分钟振幅,

d.close_amt as d_收盘价,
d.low_amt as da_最低价,
round(close_amt*0.97,2) as ea_高开买入价1,
round(close_amt*0.95,2) as eb_高开买入价2,
round(close_amt*0.95,2) as ec_低开买入价1,
round(close_amt*0.93,2) as ed_低开买入价2,
if(open_pre_close_diff_amt_ratio>0 and d.low_amt<=round(pre_close_amt*0.97,2), "高开满足", "") as fa_高开情况,
if(open_pre_close_diff_amt_ratio<=0 and d.low_amt<=round(pre_close_amt*0.95,2), "低开满足", "") as fb_低开情况,
if(open_pre_close_diff_amt_ratio>0 and d.low_amt>round(pre_close_amt*0.97,2), round((low_amt-round(pre_close_amt*0.97,2))*100/pre_close_amt,2), -1) as fc_高开缺比例,
if(open_pre_close_diff_amt_ratio<=0 and d.low_amt>round(pre_close_amt*0.95,2), round((low_amt-round(pre_close_amt*0.95,2))*100/pre_close_amt,2), -1) as fd_低开缺比例

from t_sunso_stock_day_trade_statistic_core_data d
where 1 > 0
and d.code = '{{code}}'