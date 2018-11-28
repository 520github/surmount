select {{column}} as c from (
    select
    *
    from t_sunso_stock_day_industry_statistic_core_data
    where 1>0
    and trade_date < '{{trade_date}}'
    and industry = '{{industry}}'
    order by trade_date desc
    limit {{limit}}
) as t