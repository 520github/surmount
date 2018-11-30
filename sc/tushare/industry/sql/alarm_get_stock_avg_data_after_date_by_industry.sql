select
code,name,avg(close_pre_close_diff_amt_ratio) as av
from t_sunso_stock_day_trade_statistic_core_data
where 1 >0
and trade_date>'2018-11-12'
and trade_date<=
(
    select trade_date from (
        select trade_date from t_sunso_stock_day_trade_statistic_core_data
        where trade_date>'2018-11-12' order by trade_date asc limit {{limit}}
    ) as t order by trade_date desc limit 1
)
and industry='{{industry}}'
group by code,name
order by av asc
;