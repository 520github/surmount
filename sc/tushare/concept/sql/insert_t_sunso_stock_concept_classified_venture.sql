insert into t_sunso_stock_main_concept_classified(concept_name,code,name,industry,area,totals_stock_amt,join_date)
select '创投',code,name,industry,area,round(totals_stock_amt/10000,6),'{{join_date}}'
from t_sunso_stock_basic
where 1 > 0
and trade_date=(select max(trade_date) from t_sunso_stock_basic)
and code in ('002660','300390','600647','002054','002328','600462','600128','600796','002141','000532','600257','000628','600250','600981','002054','000903','600064','600689','000532','000931','300688','600053','600783','600895','000913','600283','600635','600210','600235','000917')
and code not in (select code from t_sunso_stock_main_concept_classified where concept_name='创投')