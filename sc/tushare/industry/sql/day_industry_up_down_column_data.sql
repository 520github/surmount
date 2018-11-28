select
{{column}}
from t_sunso_stock_day_trade_statistic_core_data
where 1 > 0
and trade_date = '{{trade_date}}'
and industry = '{{industry}}'
and close_pre_close_diff_amt_ratio {{{symbol}}} 0
;