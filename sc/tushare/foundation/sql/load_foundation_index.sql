insert into t_sunso_stock_foundation_index(
code,name,year,quarter,
earnings_per_share,net_asset_per_share,cash_flow_per_share,
main_business_per_share,net_profits,business_income,

net_asset_return_ratio,net_profit_ratio,gross_profit_ratio,
rise_main_business_income_ratio,rise_net_profit_ratio,rise_net_asset_ratio,
rise_total_asset_ratio,rise_eps_ratio,rise_stockholder_equity_ratio,
earnings_per_share_yy_ratio,profits_yy_ratio,

receivable_turnover_frequency,receivable_turnover_days,inventory_turnover_frequency,
inventory_days,current_asset_turnover_frequency,current_asset_days,

current_ratio,quick_ratio,cash_ratio,interest_pay_ratio,stockholder_equity_ratio,

net_cash_flow_and_sale_ratio,cash_flow_return_ratio,
net_cash_flow_and_net_profit_ratio,net_cash_flow_and_debt_ratio,cash_flow_ratio,

report_date,allocation_scheme
)
select
m.code,m.name,m.year,m.quarter,
m.eps,m.bvps,m.epcf,
ap.bips,ap.net_profits,ap.business_income,

ap.roe,ap.net_profit_ratio,ap.gross_profit_rate,
ag.mbrg,ag.nprg,ag.nav,ag.targ,ag.epsg,ag.seg,
m.eps_yoy,m.profits_yoy,

ao.arturnover,ao.arturndays,ao.inventory_turnover,
ao.inventory_days,ao.currentasset_turnover,ao.currentasset_days,

dp.currentratio,dp.quickratio,dp.cashratio,dp.icratio,dp.sheqratio,dp.adratio,

cf.cf_sales,cf.rateofreturn,cf.cf_nm,cf.cf_liabilities,cf.cashflowratio,

m.report_date,m.distrib

from t_tushare_stock_performance_report m

left join t_tushare_stock_abitity_profit ap
on m.code = ap.code and m.year =ap.year and m.quarter = ap.quarter

left join t_tushare_stock_ability_operation ao
on m.code = ao.code and m.year =ao.year and m.quarter = ao.quarter

left join t_tushare_stock_ability_growth ag
on m.code = ag.code and m.year =ag.year and m.quarter = ag.quarter

left join t_tushare_stock_ability_debt_pay dp
on m.code = dp.code and m.year =dp.year and m.quarter = dp.quarter

left join t_tushare_stock_ability_cash_flow cf
on m.code = cf.code and m.year =cf.year and m.quarter = cf.quarter

where 1 > 0
and m.year in {{year}}
and m.quarter in {{quarter}}
concat(m.code,m.year,m.quarter)
not in (select concat(m.code,m.year,m.quarter) from t_sunso_stock_foundation_index)
;

