select
*
from t_sunso_stock_day_trade_statistic_core_data cd
where 1 > 0
and cd.trade_date='{{trade_date}}'
and cd.industry='{{industry}}'
;
