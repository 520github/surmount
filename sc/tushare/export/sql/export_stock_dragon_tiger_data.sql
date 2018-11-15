select nt.*, ttd.count,ttd.bamount,ttd.samount,ttd.net,
ttd.bcount,ttd.scount,td.amount,td.buy,td.sell,td.reason
,td.pchange,sc.close_pre_close_diff_amt_ratio,sc.trade_amt,

(select count(*) from t_tushare_stock_dragon_tiger_sale_total_data d where  d.date = nt.date and d.top3 like concat('',nt.name,'%')),
(select count(*) from t_tushare_stock_dragon_tiger_sale_total_data d where  d.date = nt.date and d.top3 = nt.name )

from  (
    select date,name,count(*) as c,group_concat(broker) from (
    SELECT st.*,
    substring_index(substring_index(st.top3,',',b.help_topic_id+1),',',-1) as name
    FROM tushare.t_tushare_stock_dragon_tiger_sale_total_data st
    inner join mysql.help_topic b
    on b.help_topic_id < (length(st.top3) - length(replace(st.top3,',',''))+1)
    where 1 > 0
    -- and top3 like '%江泉实业%'
    -- and broker='中国银河证券股份有限公司杭州庆春路证券营业部'
    and date='2018-11-06'
    and substring_index(substring_index(st.top3,',',b.help_topic_id+1),',',-1) ='奥马电器'
    ) as t
    where 1 >0
    and length(name) > 0
    group by date,name
    order by date asc
) nt
left join t_tushare_stock_dragon_tiger_total_data ttd
on nt.date = ttd.date and nt.name = ttd.name
left join t_tushare_stock_dragon_tiger_today_data td
on nt.date = td.date and nt.name = td.name
left join t_sunso_stock_day_trade_statistic_core_data sc
on nt.date = sc.trade_date and nt.name = sc.name
;