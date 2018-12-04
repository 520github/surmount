insert into t_sunso_stock_classify_track_day_data(
    classify_type,
    classify_name,
    track_date,
    trade_date,
    track_sum_day,
    from_track_date_up_down_ratio,
    trade_volume,
    sum_close_amt_ratio,
    avg_close_amt_ratio,
    stock_num
)
select * from (
    select
        '{{classify_type}}' as classify_type,
        '{{classify_name}}' as classify_name,
        '{{track_date}}' as track_date,
        '{{trade_date}}' as trade_date,
        {{track_sum_day}} as track_sum_day,
        {{from_track_date_up_down_ratio}} as from_track_date_up_down_ratio,
        {{trade_volume}} as trade_volume,
        {{sum_close_amt_ratio}} as sum_close_amt_ratio,
        {{avg_close_amt_ratio}} as avg_close_amt_ratio,
        {{stock_num}} as stock_num
    from dual
) t
where 1>0
and concat(classify_type,classify_name,track_date,trade_date) not in (
    select concat(classify_type,classify_name,track_date,trade_date)
    from t_sunso_stock_classify_track_day_data
    where 1 > 0
    and classify_type='{{classify_type}}'
    and classify_name='{{classify_name}}'
    and track_date='{{track_date}}'
)
;