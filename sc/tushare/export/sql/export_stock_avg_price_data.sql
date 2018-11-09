 select
 -- *
 '{{start_trade_date}}' as a_开始时间,'{{end_trade_date}}' as b_结束时间,

 min(if(large_above_avg_trade_price>0,large_above_avg_trade_price,null)) as c_大单上最小价,
 max(large_above_avg_trade_price) as d_大单上最大价,
 round(sum(large_above_trade_amt)*1000000/sum(large_above_trade_volume),2) as e_大单上平均价,
 round(sum(super_trade_amt)*1000000/sum(super_trade_volume),2) as ea_超单平均价,
 round(sum(large_trade_amt)*1000000/sum(large_trade_volume),2) as eb_大单平均价,
 round(sum(medium_after_trade_amt)*1000000/sum(medium_after_trade_volume),2) as ec_中单后平均价,
 round(sum(medium_before_trade_amt)*1000000/sum(medium_before_trade_volume),2) as ed_中单前平均价,
 round(sum(small_trade_amt)*1000000/sum(small_trade_volume),2) as eh_小单平均价,


 min(if(large_above_buy_avg_trade_price>0, large_above_buy_avg_trade_price, null)) as f_大单上买入最小价,
 max(large_above_buy_avg_trade_price) as g_大单上买入最大价,
 round(sum(large_above_buy_trade_amt)*1000000/sum(large_above_buy_trade_volume),2) as h_大单上买入平均价,
 round(sum(super_buy_trade_amt)*1000000/sum(super_buy_trade_volume),2) as ha_超单买入平均价,
 round(sum(large_buy_trade_amt)*1000000/sum(large_buy_trade_volume),2) as hb_大单买入平均价,
 round(sum(medium_after_buy_trade_amt)*1000000/sum(medium_after_buy_trade_volume),2) as hc_中单后买入平均价,
 round(sum(medium_before_buy_trade_amt)*1000000/sum(medium_before_buy_trade_volume),2) as hd_中单前买入平均价,
 round(sum(small_buy_trade_amt)*1000000/sum(small_buy_trade_volume),2) as he_小单买入平均价,

 (select close_amt from t_sunso_stock_day_trade_statistic_core_data where code = '{{code}}' and trade_date='{{end_trade_date}}') as i_最近收盘价,
 (select open_amt from t_sunso_stock_day_trade_statistic_core_data where code = '{{code}}' and trade_date='{{end_trade_date}}') as j_最近开盘价,
 (select low_amt from t_sunso_stock_day_trade_statistic_core_data where code = '{{code}}' and trade_date='{{end_trade_date}}') as k_最近最低价,
 (select high_amt from t_sunso_stock_day_trade_statistic_core_data where code = '{{code}}' and trade_date='{{end_trade_date}}') as l_最近最高价,
 (select avg_amt from t_sunso_stock_day_trade_statistic_core_data where code = '{{code}}' and trade_date='{{end_trade_date}}') as m_最近平均价
 from t_sunso_stock_day_trade_statistic_volume_data
 where 1 > 0
 and code = '{{code}}'
 and trade_date between '{{start_trade_date}}' and '{{end_trade_date}}'
 order by trade_date desc
 ;