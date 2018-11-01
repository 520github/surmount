insert into t_sunso_stock_plate_stock(plate_name,plate_start_date,code,name,industry,area,circulation_amt,join_date)
select '{{plate_name}}','{{plate_start_date}}',code,name,industry,area,round(circulation_amt/10000,6),'{{join_date}}'
from t_sunso_stock_day_trade_statistic_core_data
where trade_date='{{trade_date}}'
and close_amt > 0
and code in ('300492','000671','002261','002556','002570','002699','002845','300041','300279','300440','300469','300582','300690','400492','600052','600079','600155','600208','600280','600297','600300','600318','600337','600346','600373','600400','600438','600496','600535','600633','600699','600804','600867','600986','601218','601388','601555','603001','603011','603018','603167','603501','603808','603979')
and code not in (select code from t_sunso_stock_plate_stock
where plate_name='{{plate_name}}' and plate_start_date='{{plate_start_date}}')
;