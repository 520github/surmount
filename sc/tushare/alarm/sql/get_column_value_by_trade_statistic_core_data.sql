select {{column}} as c from (
    select * from t_sunso_stock_day_trade_statistic_core_data
    where 1 > 0
    and code = '{{code}}'
    and trade_date {{{date_compare}}} '{{trade_date}}'
    order by trade_date {{sort}} limit {{limit}}
) as t
;
