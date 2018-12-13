insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,industry,area,circulation_amt,join_date)
select '{{plate_name}}','{{plate_start_date}}',code,name,industry,area,round(circulation_amt/10000,6),'{{join_date}}'
from (
    select cd.* from t_sunso_stock_day_trade_statistic_core_data cd,
    (select * from t_sunso_stock_day_trade_statistic_core_data
    where trade_date=(
        select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
        where trade_date<'{{trade_date}}'
        order by trade_date desc limit 1
        )
    ) t
    where 1 >0
    and cd.code = t.code
    and cd.trade_date='{{trade_date}}'
    and cd.pre1_close_price_ratio > 3
    and cd.pre10_close_price_ratio > 5
    and cd.pre1_avg_turnover_rate_ratio > 1
    and cd.pre5_avg_turnover_rate_ratio >1
    and t.contiune_up_down_percent between -10 and -1
    and t.continue_up_down_days between 4 and 8
) as tmp
where 1 > 0
and close_amt > 0
and code not in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}')
;