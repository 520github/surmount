select
c.turnover_rate,
v.large_above_sum_trade_amt_ratio,
v.large_above_trade_count
from t_sunso_stock_day_trade_statistic_core_data c left join t_sunso_stock_day_trade_statistic_volume_data v
on c.code = v.code and c.trade_date = v.trade_date
where 1 > 0
and c.code = '{{code}}'
and c.trade_date = '{{trade_date}}'
;