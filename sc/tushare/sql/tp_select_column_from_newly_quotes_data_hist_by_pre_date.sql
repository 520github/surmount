select {{column}} as c
from (
    select * from t_tushare_stock_newly_quotes_data_hist
    where code='{{code}}' and date<'{{trade_date}}'
    order by date desc limit {{limit}}
) as t
;