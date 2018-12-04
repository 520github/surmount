insert into t_sunso_stock_classify_track_basic(
classify_type,
classify_name,
track_date
)
select 'industry',industry,'{{trade_date}}'
from t_sunso_stock_day_industry_statistic_core_data
where 1 > 0
and pre5_totals_stock_amt_ratio < -5
and pre10_totals_stock_amt_ratio < 0
and pre20_totals_stock_amt_ratio < 0
and pre1_totals_stock_amt_ratio > 0
and pre1_totals_stock_amt_ratio > pre3_totals_stock_amt_ratio
and trade_volume > pre3_avg_trade_volume
and trade_date='{{trade_date}}'
and concat('industry',industry,'{{trade_date}}') not in (
  select concat(classify_type,classify_name,track_date)
  from t_sunso_stock_classify_track_basic
  where 1 >0
  and classify_type='industry'
  and track_date='{{trade_date}}'
)
;