update t_sunso_stock_day_trade_statistic_range_avg_data t
set {{column}}=(
    select av from (
        select code,round(avg(close_amt),2) as av
        from t_sunso_stock_day_trade_statistic_range_avg_data ra
        where 1 >0
        and ra.trade_date<='{{trade_date}}'
        and ra.trade_date>(
            select trade_date from (
                select distinct trade_date from t_sunso_stock_day_trade_statistic_range_avg_data
                where trade_date < '{{trade_date}}' order by trade_date desc limit {{limit}}
            ) as tmp order by trade_date asc limit 1
        )
        group by code
	) as ra
    where ra.code = t.code
)
where 1 >0
and t.trade_date='{{trade_date}}'
-- and t.code='300532'
;