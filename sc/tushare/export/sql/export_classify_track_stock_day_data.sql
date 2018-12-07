select
ct.classify_type as a_类别,
ct.classify_name as b_名称,
ct.track_date as c_跟踪日期,
ct.trade_date as d_交易日期,
ct.code as db_代码,
ct.name as dc_名称,
{{reback_day}} as de_回溯日,
rd.avg_close_amt_ratio as df_回溯平均涨幅,
ct.from_track_date_up_down_ratio as e_跟踪日截止交易日的涨幅比,
ct.avg_close_amt_ratio as eb_截止当日平均涨幅,
ct.sum_close_amt_ratio as ec_截止当日累计涨幅,
ct.close_amt_ratio as ed_当日涨幅,
ct.close_amt as ef_当日涨停价,
ct.track_date_close_amt as em_追踪日收盘价,
ct.track_date_close_amt_ratio as en_追踪日涨幅,
ct.track_sum_day as g_跟踪天数
from
t_sunso_stock_classify_track_stock_day_data ct
left join
t_sunso_stock_classify_track_reback_stock_data rd
on ct.classify_type = rd.classify_type
and ct.classify_name = rd.classify_name
and ct.track_date = rd.track_date
and ct.code = rd.code
and rd.reback_day={{reback_day}}
where 1 > 0
and ct.classify_type='{{classify_type}}'
and ct.classify_name='{{classify_name}}'
and ct.track_date='{{track_date}}'
and ct.code='{{code}}'
;