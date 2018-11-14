select
s.name as a_名称,
s.code as b_代码,
s.industry as c_行业,
s.area as d_地区,
s.join_date as f_加入时间

from t_sunso_stock_plate_stock s
where 1> 0
and plate_name = '{{plate_name}}'
and plate_start_date = '{{plate_start_date}}'
order by created_at desc
;