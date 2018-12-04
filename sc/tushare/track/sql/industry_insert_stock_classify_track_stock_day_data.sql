insert into t_sunso_stock_classify_track_stock_day_data(
    classify_type,
    classify_name,
    track_date,
    trade_date,
    track_sum_day,
    code,
    name,
    from_track_date_up_down_ratio,
    track_date_close_amt,
    track_date_close_amt_ratio,
    close_amt,
    close_amt_ratio,
    sum_close_amt_ratio,
    avg_close_amt_ratio
)
select * from (
    select
        '{{classify_type}}' as classify_type,
        '{{classify_name}}' as classify_name,
        '{{track_date}}' as track_date,
        '{{trade_date}}' as trade_date,
        {{track_sum_day}} as track_sum_day,
        '{{code}}' as code,
        '{{name}}' as name,
        {{from_track_date_up_down_ratio}} as from_track_date_up_down_ratio,
        {{track_date_close_amt}} as track_date_close_amt,
        {{track_date_close_amt_ratio}} as track_date_close_amt_ratio,
        {{close_amt}} as close_amt,
        {{close_amt_ratio}} as close_amt_ratio,
        {{sum_close_amt_ratio}} as sum_close_amt_ratio,
        {{avg_close_amt_ratio}} as avg_close_amt_ratio
    from dual
) t
where 1 > 0
and concat(classify_type,classify_name,track_date,trade_date,code) not in (
    select
    concat(classify_type,classify_name,track_date,trade_date,code)
    from t_sunso_stock_classify_track_stock_day_data
    where 1 > 0
    and classify_type='{{classify_type}}'
    and classify_name='{{classify_name}}'
    and track_date='{{track_date}}'
    and trade_date='{{trade_date}}'
)
;