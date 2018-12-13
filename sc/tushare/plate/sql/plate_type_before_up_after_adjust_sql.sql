insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,industry,area,circulation_amt,join_date)
select '{{plate_name}}','{{plate_start_date}}',code,name,industry,area,round(circulation_amt/10000,6),'{{join_date}}'
FROM
t_sunso_stock_day_trade_statistic_core_data cd,
tushare.t_sunso_stock_day_trade_statistic_range_avg_data ra
where 1 >0
and cd.close_amt > 0
and cd.code = ra.code
and cd.trade_date = ra.trade_date
and cd.trade_date='2018-12-12'
and cd.pre10_close_price_ratio between 5 and 12 -- 近10日涨幅
and cd.pre5_close_price_ratio between -3 and 3 -- 近5日涨幅情况
and cd.pre3_close_price_ratio between -3 and 3 -- 近3日涨幅
and cd.pre20_close_price_ratio > 5  -- 近20日涨幅
and cd.pre1_avg_turnover_rate_ratio < 1 -- 前1日缩量
and cd.pre5_avg_turnover_rate_ratio < 1 -- 前5日缩量
and ra.pre5_avg_close_pre_close_diff_amt_ratio between -0.8 and 0.8 -- 前5日平均涨幅很小
and cd.code not in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}')
;