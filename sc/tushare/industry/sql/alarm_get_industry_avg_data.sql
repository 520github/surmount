select industry,trade_date,
sum(avg_close_price_ratio),
avg(avg_close_price_ratio)
from t_sunso_stock_day_industry_statistic_core_data
where 1 > 0
and trade_date > ''
and trade_date<=
(
    select trade_date from (
        select trade_date from t_sunso_stock_day_industry_statistic_core_data
        where trade_date>'2018-11-12' order by trade_date asc limit {{limit}}
    ) as t order by trade_date desc limit 1
)
and industry='{{industry}}'
;