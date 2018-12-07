insert into t_sunso_stock_classify_track_config(
classify_type,
classify_name,
track_date,
reback_day,
track_day
)
select 'industry',industry,'{{trade_date}}',5,20
from t_sunso_stock_day_industry_statistic_core_data
where 1 > 0
and pre5_totals_stock_amt_ratio < -5
and pre10_totals_stock_amt_ratio < 0
and pre20_totals_stock_amt_ratio < 0
and pre1_totals_stock_amt_ratio > 0
and pre1_totals_stock_amt_ratio > pre3_totals_stock_amt_ratio
and trade_volume > pre3_avg_trade_volume
and trade_date='{{trade_date}}'
and concat('industry',industry,'{{trade_date}}',5) not in (
  select concat(classify_type,classify_name,track_date,5)
  from t_sunso_stock_classify_track_config
  where 1>0
  and classify_type='industry'
  and track_date='{{trade_date}}'
)
;