insert into t_sunso_stock_main_concept_classified(concept_name,code,name,industry,area,totals_stock_amt,join_date)
select '独角兽',code,name,industry,area,round(totals_stock_amt/10000,6),'{{join_date}}'
from t_sunso_stock_basic
where 1 > 0
and trade_date=(select max(trade_date) from t_sunso_stock_basic)
and name in ('迈瑞医疗','合肥城建','贤丰控股','麦达数字','华金资本','天华超净','药明康德')
and code not in (select code from t_sunso_stock_main_concept_classified where concept_name='独角兽')