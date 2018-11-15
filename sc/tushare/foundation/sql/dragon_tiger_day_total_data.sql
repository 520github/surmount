insert into t_sunso_stock_dragon_tiger_day_total_data(
    code,name,trade_date,trade_amt,circulation_amt,turnover_rate,close_amt,
    nearly5_day_sale_only_count,nearly5_day_sale_only_buy_count,nearly5_day_sale_only_sell_count,
    nearly5_day_sale_top1_count,nearly5_day_sale_top3_count,
    nearly5_day_sale_top1_names,nearly5_day_sale_top3_names,nearly5_day_sale_only_names,

    nearly5_day_sale_only_buy_amt,nearly5_day_sale_only_sell_amt,

    nearly5_day_buy_amt,nearly5_day_sell_amt,nearly5_day_net_amt,
    nearly5_day_buy_count,nearly5_day_sell_count,

    today_all_amt,today_buy_amt,today_sell_amt,
    today_buy_amt_ratio,today_sell_amt_ratio,today_reason,

    today_all_amt_mulit_str,today_buy_amt_mulit_str,today_sell_amt_mulit_str,
    today_buy_amt_ratio_mulit_str,today_sell_amt_ratio_mulit_str,today_reason_mulit_str,

    nearly5_day_organ_buy_amt,nearly5_day_organ_sell_amt,nearly5_day_organ_net_amt,
    nearly5_day_organ_buy_count,nearly5_day_organ_sell_count,

    today_organ_buy_amt,today_organ_sell_amt,today_organ_reason,
    today_organ_buy_amt_mulit_str,today_organ_sell_amt_mulit_str,today_organ_reason_mulit_str
)
select
sc.code,sc.name,sc.trade_date,
round(sc.trade_amt/100000000,6),round(sc.circulation_amt/10000,6),
sc.turnover_rate,sc.close_amt,
(select count(*) from t_tushare_stock_dragon_tiger_sale_total_data d where  d.date = nt.date and d.top3 = nt.name ),
(select count(*) from t_tushare_stock_dragon_tiger_sale_total_data d where  d.date = nt.date and d.top3 = nt.name and d.scount<1),
(select count(*) from t_tushare_stock_dragon_tiger_sale_total_data d where  d.date = nt.date and d.top3 = nt.name and d.bcount<1),
(select count(*) from t_tushare_stock_dragon_tiger_sale_total_data d where  d.date = nt.date and d.top3 like concat('',nt.name,'%')),
nt.c,
(select group_concat(broker order by bamount desc) from t_tushare_stock_dragon_tiger_sale_total_data d where  d.date = nt.date and d.top3 = nt.name ),
(select group_concat(broker order by bamount desc) from t_tushare_stock_dragon_tiger_sale_total_data d where  d.date = nt.date and d.top3 like concat('',nt.name,'%') ),
nt.broker,

(select round(sum(bamount)/10000,2) from t_tushare_stock_dragon_tiger_sale_total_data d where  d.date = nt.date and d.top3 = nt.name and d.scount<1),
(select round(sum(samount)/10000,2) from t_tushare_stock_dragon_tiger_sale_total_data d where  d.date = nt.date and d.top3 = nt.name and d.bcount<1),

round(ttd.bamount/10000,6),
round(ttd.samount/10000,6),
round(ttd.net/10000,6),
ttd.bcount,ttd.scount,

round(td.amount/10000,6),round(td.buy/10000,6),round(td.sell/10000,6),
td.bratio,td.sratio,td.reason,
td.amount_mulit,td.buy_mulit,td.sell_mulit,
td.bratio_mulit,td.sratio_mulit,td.reason_mulit,

round(otd.bamount/10000,6),round(otd.samount/10000,6),round(otd.net/10000,6),otd.bcount,otd.scount,

round(od.bamount/10000,6),round(od.samount/10000,6),od.type,
od.bamount_mulit,od.samount_mulit,od.type_mulit
from  (
    select date,name,count(*) as c,group_concat(broker order by bamount desc) as broker from (
        SELECT st.*,
        substring_index(substring_index(st.top3,',',b.help_topic_id+1),',',-1) as name
        FROM tushare.t_tushare_stock_dragon_tiger_sale_total_data st
        inner join mysql.help_topic b
        on b.help_topic_id < (length(st.top3) - length(replace(st.top3,',',''))+1)
        where 1 > 0
        and date='{{trade_date}}'
    ) as t
    where 1 >0
    and length(name) > 0
    group by date,name
    order by c desc
) nt

left join t_tushare_stock_dragon_tiger_total_data ttd
on nt.date = ttd.date and nt.name = ttd.name

left join (
    select t.date,t.code,t.name,
    amount,buy,sell,bratio*100 as bratio,sratio*100 as sratio,reason,
    group_concat(amount) as amount_mulit,
    group_concat(buy) as buy_mulit,
    group_concat(sell) as sell_mulit,
    group_concat(bratio) as bratio_mulit,
    group_concat(bratio) as sratio_mulit,
    group_concat(reason) as reason_mulit
    from t_tushare_stock_dragon_tiger_today_data t
    where t.date ='{{trade_date}}' group by t.code
) td

on nt.date = td.date and nt.name = td.name

left join t_sunso_stock_day_trade_statistic_core_data sc
on nt.date = sc.trade_date and nt.name = sc.name

left join t_tushare_stock_dragon_tiger_organ_total_data otd
on nt.date = otd.date and nt.name = otd.name

left join (
    select
    t.date,t.code,t.name,
    bamount,samount,type,
    group_concat(bamount) as bamount_mulit,
    group_concat(samount) as samount_mulit,
    group_concat(type) as type_mulit
    from t_tushare_stock_dragon_tiger_organ_today_data t
    where t.date='{{trade_date}}' group by t.code
) od
on nt.date = od.date and nt.name = od.name
where 1 > 0
and sc.code is not null
and sc.trade_date = '{{trade_date}}'
;