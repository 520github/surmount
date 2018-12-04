select {{column}} as c from t_sunso_stock_day_industry_statistic_core_data
where 1 > 0
and industry='{{industry}}'
and trade_date<='{{trade_date}}'
and trade_date>'{{track_date}}'
;