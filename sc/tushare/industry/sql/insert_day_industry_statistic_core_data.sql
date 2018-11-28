insert into t_sunso_stock_day_industry_statistic_core_data(
    industry,
    trade_date,
    totals_stock_amt,
    circulation_stock_amt,
    totals_stock_volume,
    circulation_stock_volume,
    trade_volume,
    trade_amt,
    trade_count,
    avg_trade_per_volume,
    stock_num,
    avg_close_price,
    sum_close_price_ratio,
    avg_close_price_ratio
)
select
    cd.industry,
    cd.trade_date,
    round(sum(cd.market_cap_amt/10000),6),
    round(sum(cd.circulation_amt/10000),6),
    sum(sb.totals_stock_volume),
    sum(sb.circulation_stock_volume),

    round(sum(trade_volume/100000000),6),
    sum(trade_amt/100000000),
    sum(trade_count),
    round(avg(trade_per_avg_volume),2),
    count(*) as c,
    round(avg(cd.close_amt),2),
    sum(close_pre_close_diff_amt_ratio),
    round(avg(close_pre_close_diff_amt_ratio),2)
from
t_sunso_stock_day_trade_statistic_core_data cd,t_sunso_stock_basic sb
where cd.trade_date='{{trade_date}}'
and cd.code = sb.code
and cd.trade_date = sb.trade_date
group by cd.trade_date,industry