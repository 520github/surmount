select
sb.name as a_名称,
sb.code as b_代码,
sb.totals_stock_volume as c_股本,
sb.net_asset_per_share as d_每股净资产,
sb.reserved_amt_per_share as e_每股公积金,
fi.earnings_per_share as f_每股收益,
fi.cash_flow_per_share as g_每股现金流,
sb.time_to_market as h_上市时间,
fi.rise_net_profit_ratio as ha_净利润增长率,
(select group_concat(date)
from t_tushare_stock_limited_sale_reopen lsr
where lsr.code=sb.code and lsr.year>={{year}}) as l_解禁日期,
(select group_concat(count)
from t_tushare_stock_limited_sale_reopen lsr
where lsr.code=sb.code and lsr.year>={{year}}) as m_解禁数量万,
(select group_concat(ratio)
from t_tushare_stock_limited_sale_reopen lsr
where lsr.code=sb.code and lsr.year>={{year}}) as n_解禁数量占比

from t_sunso_stock_basic sb
left join t_sunso_stock_foundation_index fi
on sb.code = fi.code and fi.year = {{year}} and fi.quarter = {{quarter}}
where 1 > 0
and sb.totals_stock_volume <= 2    -- 总股本数
and sb.trade_date='{{trade_date}}'
and sb.net_asset_per_share >=10    -- 每股净资产
and sb.reserved_amt_per_share >=3  -- 每股公积金
and sb.code in (
  select code from t_sunso_stock_foundation_index
  where 1 > 0
  and year=2018
  and quarter =2   -- 中报
  and earnings_per_share > 0.5  -- 每股收益
  and cash_flow_per_share > 0   -- 每股现金流
)
order by sb.totals_stock_volume asc
;