update t_sunso_stock_classify_track_basic
set
trade_date='{{trade_date}}',
stock_num={{stock_num}},
from_track_date_up_down_ratio={{from_track_date_up_down_ratio}}
where 1 > 0
and classify_type='{{classify_type}}'
and classify_name='{{classify_name}}'
and track_date='{{track_date}}'
;