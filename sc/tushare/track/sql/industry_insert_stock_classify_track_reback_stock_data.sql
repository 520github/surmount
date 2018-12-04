insert into t_sunso_stock_classify_track_reback_stock_data(
classify_type,
classify_name,
track_date,
reback_day,
code,
name,
avg_close_amt_ratio
)
select * from (
    select
    '{{classify_type}}' as classify_type,'{{classify_name}}' as classify_name,'{{track_date}}' as track_date,
    {{reback_day}} as reback_day,cd.code,cd.name,avg(cd.close_pre_close_diff_amt_ratio)
    from t_sunso_stock_day_trade_statistic_core_data cd
    where 1 > 0
    and cd.trade_date < '{{track_date}}'
    and cd.trade_date >=(
        select trade_date from (
            select distinct trade_date from t_sunso_stock_day_trade_statistic_core_data
            where trade_date < '{{track_date}}' order by desc limit {{reback_day}}
        ) t order by trade_date asc limit 1
    )
    and industry='{{classify_name}}'
    group by code,name
) t
where concat(classify_type,classify_name,track_date,reback_day,code) not in (
    select concat(classify_type,classify_name,track_date,reback_day,code)
    from t_sunso_stock_classify_track_reback_stock_data
    where 1>0
    and classify_type='{{classify_type}}'
    and classify_name='{{classify_name}}'
    and track_date='{{track_date}}'
    and reback_day={{reback_day}}
)
;
