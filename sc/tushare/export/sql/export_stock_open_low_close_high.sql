 select
 '{{trade_date}}' as a_统计日期,
 {{limit}} as b_数据周期,
 t.code as code,
 t.name as coa_名称,
 (select round((t.open_amt-cd.close_amt)/cd.close_amt*100,2) from t_sunso_stock_day_trade_statistic_core_data t
where t.code=cd.code and t.trade_date > '{{trade_date}}'
order by t.trade_date asc limit 1
) as coaa_第二日开盘幅度,

(select round((t.low_amt-cd.close_amt)/cd.close_amt*100,2) from t_sunso_stock_day_trade_statistic_core_data t
where t.code=cd.code and t.trade_date > '{{trade_date}}'
order by t.trade_date asc limit 1
) as cob_第二日最低幅度,

(select round((t.high_amt-cd.close_amt)/cd.close_amt*100,2) from t_sunso_stock_day_trade_statistic_core_data t
where t.code=cd.code and t.trade_date > '{{trade_date}}'
order by t.trade_date asc limit 1
) as coc_第二日最高幅度,

(select round((t.low_amt - t.high_amt)/t.high_amt*100,2) from t_sunso_stock_day_trade_statistic_core_data t
where t.code=cd.code and t.trade_date > '{{trade_date}}'
order by t.trade_date asc limit 1
) as cod_第二日低高幅度,

(select round((t.close_amt-cd.close_amt)/cd.close_amt*100,2) from t_sunso_stock_day_trade_statistic_core_data t
where t.code=cd.code and t.trade_date > '{{trade_date}}'
order by t.trade_date asc limit 1
) as coe_第二日收盘幅度,
 0 as cof_今日开盘价,
 concat("=(D",cast(((@rowNum:=@rowNum+1)+1) as SIGNED INTEGER),"-",cd.close_amt,")/",cd.close_amt,"*100") as cog_开盘价涨幅,
 -- cast(((@rowNum:=@rowNum+1)+1) as SIGNED INTEGER) as ce_序号,
 t.lh as da_平均低高幅度,
 t.open as db_平均开盘幅度,
 t.close as dc_平均收盘幅度,
 t.low as dd_平均最低幅度,
 t.high as de_平均最高幅度,
 t.pre5_ratio as df_平均前5日价格幅度,
 dtd.nearly5_day_sale_top3_count as dl_前3营业部数,
 dtd.nearly5_day_sale_top1_count as dm_前1营业部数,
 dtd.nearly5_day_sale_only_count as dn_独立营业数,
 dtd.nearly5_day_sale_only_buy_count as do_纯买独立营业数,
 dtd.nearly5_day_sale_only_sell_count as dp_纯卖独立营业数,
 dtd.today_buy_amt_ratio as dq_当日龙虎榜买入占比,
 dtd.today_sell_amt_ratio as dr_当日龙虎榜卖出占比,
 dtd.nearly5_day_buy_amt as ds_近5日龙虎榜买入金额,
 dtd.nearly5_day_sell_amt as dt_近5日龙虎榜卖出金额,
 cd.close_amt as ea_统计日收盘价,
 cd.low_high_diff_amt_ratio as eb_统计日高低幅度,
 cd.open_pre_close_diff_amt_ratio as ec_统计日开盘幅度,
 cd.close_pre_close_diff_amt_ratio as ed_统计收盘低幅度,
 cd.low_pre_close_diff_amt_ratio as ee_统计日最低幅度,
 cd.high_pre_close_diff_amt_ratio as ef_统计日最高幅度,
 cd.pre5_close_price_ratio as eg_统计日前5日幅度

 from (
     select code,name,
     avg(low_high_diff_amt_ratio) as lh,
     avg(open_pre_close_diff_amt_ratio) as open,
     avg(low_pre_close_diff_amt_ratio) as low,
     avg(high_pre_close_diff_amt_ratio) as high,
     avg(close_pre_close_diff_amt_ratio) as close,
     avg(pre5_close_price_ratio) as pre5_ratio
     from t_sunso_stock_day_trade_statistic_core_data
     where 1 > 0
     and trade_date <='{{trade_date}}'
     and trade_date >=
         (select trade_date from
                 (select distinct trade_date
                 from t_sunso_stock_day_trade_statistic_core_data
                 where trade_date<='{{trade_date}}'
                 order by trade_date desc limit {{limit}}
                 )  as  t
         order by trade_date asc limit 1)
     group by code,name
 )  as t
 left join t_sunso_stock_day_trade_statistic_core_data cd
 on t.code = cd.code and cd.trade_date = '{{trade_date}}'
 left join t_sunso_stock_dragon_tiger_day_total_data dtd
 on t.code = dtd.code and dtd.trade_date = '{{trade_date}}'
 ,(Select (@rowNum :=0) ) b
 where 1 > 0
 and t.lh >=5        -- 平均低高差大于5哥点
 and t.low<=-3       -- 平均最低点小于-3
 and t.high>=3       -- 平均最高点大于3
 and t.open < 0      -- 平均开盘点小于0
 and t.open*1.5>low  -- 开盘点*1.5要大于最低点
 and t.close > t.open  -- 平均收盘点大于开盘点
 order by t.low asc
 ;
