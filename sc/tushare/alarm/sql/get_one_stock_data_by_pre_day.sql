select
t.turnover_rate,
t.pre5_close_price_ratio,
t.pre10_close_price_ratio
from (
    select c.* from t_sunso_stock_day_trade_statistic_core_data c
    left join t_sunso_stock_day_trade_statistic_volume_data v
    on c.code = v.code and c.trade_date = v.trade_date
    where 1 > 0
    and c.code = '{{code}}'
    and c.trade_date < '{{trade_date}}'
    order by c.trade_date desc limit {{limit}}
) as t
order by t.trade_date asc limit 1
;