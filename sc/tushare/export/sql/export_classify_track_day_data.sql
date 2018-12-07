select
ct.classify_type as a_类别,
ct.classify_name as b_名称,
ct.track_date as c_跟踪日期,
ct.trade_date as d_交易日期,
ct.from_track_date_up_down_ratio as e_跟踪日截止交易日的涨幅比,
ct.avg_close_amt_ratio as eb_当日平均涨幅,
ct.sum_close_amt_ratio as ec_当日累计涨幅,
ct.stock_num as f_对应股票数,
ct.track_sum_day as g_跟踪天数,
ct.trade_volume as h_交易量
from
t_sunso_stock_classify_track_day_data ct
where 1 > 0
and ct.classify_type='{{classify_type}}'
and ct.classify_name='{{classify_name}}'
and ct.track_date='{{track_date}}'
;