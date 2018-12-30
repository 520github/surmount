insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,industry,area,circulation_amt,join_date)
select '{{plate_name}}','{{plate_start_date}}',cd.code,cd.name,cd.industry,cd.area,round(cd.circulation_amt/10000,6),'{{join_date}}'
from t_sunso_stock_day_trade_statistic_core_data cd
where 1 >0
-- and code='603922'
and trade_date='{{trade_date}}'
and close_amt > open_amt
and (close_amt-open_amt)/open_amt*100>1
and pre5_close_price_ratio <= -10
and pre10_close_price_ratio < pre5_close_price_ratio
and pre20_close_price_ratio < pre10_close_price_ratio
and pre30_close_price_ratio > pre20_close_price_ratio
;