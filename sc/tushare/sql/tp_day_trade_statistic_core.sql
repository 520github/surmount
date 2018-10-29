insert into t_sunso_stock_day_trade_statistic_core_data(
    code,
    name,
    open_amt,
    close_amt,
    low_amt,
    high_amt,
    avg_amt,
    pre_close_amt,
    close_pre_close_diff_amt_ratio,
    open_pre_close_diff_amt_ratio,
    low_pre_close_diff_amt_ratio,
    high_pre_close_diff_amt_ratio,
    low_high_diff_amt_ratio,
    turnover_rate,
    trade_volume,
    trade_amt,
    trade_count,
    trade_per_avg_volume,
    trade_net_amt,
    market_cap_amt,
    circulation_amt,
    pre_avg1_trade_price_ratio,
    pre_avg1_trade_amt_ratio,
    pre_avg1_trade_net_amt_ratio,
    pre_avg1_trade_volume_ratio,
    pre_avg1_trade_count_ratio,
    pre_avg1_trade_per_avg_volume_ratio,
    inside_dish_sum_amt_ratio,
    outside_dish_sum_amt_ratio,
    midside_dish_sum_amt_ratio,
    small_sum_trade_amt_ratio,
    small_buy_trade_amt_ratio,
    small_sell_trade_amt_ratio,
    large_above_sum_trade_amt_ratio,
    large_above_buy_trade_amt_ratio,
    large_above_sell_trade_amt_ratio,
    large_above_bs_trade_amt_ratio,
    dragon_tiger_today_reason,
    dragon_tiger_all_today_amt_ratio,
    dragon_tiger_total_reason,
    dragon_tiger_all_total_amt_ratio,
    dragon_tiger_all_5day_count,
    dragon_tiger_all_5day_bs_amt_percent,
    pre_avg3_trade_price_ratio,
    pre_avg3_trade_amt_ratio,
    pre_avg3_trade_net_amt_ratio,
    pre_avg3_trade_volume_ratio,
    pre_avg3_trade_count_ratio,
    pre_avg3_trade_per_avg_volume_ratio,
    pre_avg5_trade_price_ratio,
    pre_avg10_trade_price_ratio,
    pre_avg20_trade_price_ratio,
    pre_avg30_trade_price_ratio,
    pre_avg60_trade_price_ratio,
    pre_avg90_trade_price_ratio,
    pre_avg120_trade_price_ratio,
    pre_avg250_trade_price_ratio,
    pre_avg365_trade_price_ratio,
    pre_avg5_trade_amt_ratio,
    pre_avg10_trade_amt_ratio,
    pre_avg20_trade_amt_ratio,
    pre_avg30_trade_amt_ratio,
    pre_avg60_trade_amt_ratio,
    pre_avg90_trade_amt_ratio,
    pre_avg120_trade_amt_ratio,
    pre_avg250_trade_amt_ratio,
    pre_avg365_trade_amt_ratio,
    pre_avg5_trade_net_amt_ratio,
    pre_avg10_trade_net_amt_ratio,
    pre_avg20_trade_net_amt_ratio,
    pre_avg30_trade_net_amt_ratio,
    pre_avg60_trade_net_amt_ratio,
    pre_avg90_trade_net_amt_ratio,
    pre_avg120_trade_net_amt_ratio,
    pre_avg250_trade_net_amt_ratio,
    pre_avg365_trade_net_amt_ratio,
    pre_avg5_trade_volume_ratio,
    pre_avg10_trade_volume_ratio,
    pre_avg20_trade_volume_ratio,
    pre_avg30_trade_volume_ratio,
    pre_avg60_trade_volume_ratio,
    pre_avg90_trade_volume_ratio,
    pre_avg120_trade_volume_ratio,
    pre_avg250_trade_volume_ratio,
    pre_avg365_trade_volume_ratio,
    pre_avg5_trade_count_ratio,
    pre_avg10_trade_count_ratio,
    pre_avg20_trade_count_ratio,
    pre_avg30_trade_count_ratio,
    pre_avg60_trade_count_ratio,
    pre_avg90_trade_count_ratio,
    pre_avg120_trade_count_ratio,
    pre_avg250_trade_count_ratio,
    pre_avg365_trade_count_ratio,
    pre_avg5_trade_per_avg_volume_ratio,
    pre_avg10_trade_per_avg_volume_ratio,
    pre_avg20_trade_per_avg_volume_ratio,
    pre_avg30_trade_per_avg_volume_ratio,
    pre_avg60_trade_per_avg_volume_ratio,
    pre_avg90_trade_per_avg_volume_ratio,
    pre_avg120_trade_per_avg_volume_ratio,
    pre_avg250_trade_per_avg_volume_ratio,
    pre_avg365_trade_per_avg_volume_ratio,
    dragon_tiger_today_is,
    dragon_tiger_all_today_amt,
    dragon_tiger_all_today_buy_amt_ratio,
    dragon_tiger_all_today_sell_amt_ratio,
    dragon_tiger_organ_today_buy_amt_ratio,
    dragon_tiger_organ_today_sell_amt_ratio,
    dragon_tiger_sale_today_buy_amt_ratio,
    dragon_tiger_sale_today_sell_amt_ratio,
    dragon_tiger_total_is,
    dragon_tiger_all_total_amt,
    dragon_tiger_all_total_buy_amt_ratio,
    dragon_tiger_all_total_sell_amt_ratio,
    dragon_tiger_organ_total_buy_amt_ratio,
    dragon_tiger_organ_total_sell_amt_ratio,
    dragon_tiger_sale_total_buy_amt_ratio,
    dragon_tiger_sale_total_sell_amt_ratio,
    dragon_tiger_all_5day_bs_count_percent,
    dragon_tiger_all_5day_bs_diff_amt,
    dragon_tiger_organ_5day_bs_amt_percent,
    dragon_tiger_organ_5day_bs_count_percent,
    dragon_tiger_organ_5day_bs_diff_amt,
    dragon_tiger_sale_5day_name,
    medium_sum_trade_amt_ratio,
    large_sum_trade_amt_ratio,
    super_sum_trade_amt_ratio,
    small_inside_sum_trade_amt_ratio,
    small_outside_sum_trade_amt_ratio,
    medium_inside_sum_trade_amt_ratio,
    medium_outside_sum_trade_amt_ratio,
    large_inside_sum_trade_amt_ratio,
    large_outside_sum_trade_amt_ratio,
    super_inside_sum_trade_amt_ratio,
    super_outside_sum_trade_amt_ratio,
    trade_date
)
value(
    '{{code}}',
    '{{name}}',
    {{open_amt}},
    {{close_amt}},
    {{low_amt}},
    {{high_amt}},
    {{avg_amt}},
    {{pre_close_amt}},
    {{close_pre_close_diff_amt_ratio}},
    {{open_pre_close_diff_amt_ratio}},
    {{low_pre_close_diff_amt_ratio}},
    {{high_pre_close_diff_amt_ratio}},
    {{low_high_diff_amt_ratio}},
    {{turnover_rate}},
    {{trade_volume}},
    {{trade_amt}},
    {{trade_count}},
    {{trade_per_avg_volume}},
    {{trade_net_amt}},
    {{market_cap_amt}},
    {{circulation_amt}},
    {{pre_avg1_trade_price_ratio}},
    {{pre_avg1_trade_amt_ratio}},
    {{pre_avg1_trade_net_amt_ratio}},
    {{pre_avg1_trade_volume_ratio}},
    {{pre_avg1_trade_count_ratio}},
    {{pre_avg1_trade_per_avg_volume_ratio}},
    {{inside_dish_sum_amt_ratio}},
    {{outside_dish_sum_amt_ratio}},
    {{midside_dish_sum_amt_ratio}},
    {{small_sum_trade_amt_ratio}},
    {{small_buy_trade_amt_ratio}},
    {{small_sell_trade_amt_ratio}},
    {{large_above_sum_trade_amt_ratio}},
    {{large_above_buy_trade_amt_ratio}},
    {{large_above_sell_trade_amt_ratio}},
    {{large_above_bs_trade_amt_ratio}},
    '{{dragon_tiger_today_reason}}',
    {{dragon_tiger_all_today_amt_ratio}},
    '{{dragon_tiger_total_reason}}',
    {{dragon_tiger_all_total_amt_ratio}},
    {{dragon_tiger_all_5day_count}},
    {{dragon_tiger_all_5day_bs_amt_percent}},
    {{pre_avg3_trade_price_ratio}},
    {{pre_avg3_trade_amt_ratio}},
    {{pre_avg3_trade_net_amt_ratio}},
    {{pre_avg3_trade_volume_ratio}},
    {{pre_avg3_trade_count_ratio}},
    {{pre_avg3_trade_per_avg_volume_ratio}},
    {{pre_avg5_trade_price_ratio}},
    {{pre_avg10_trade_price_ratio}},
    {{pre_avg20_trade_price_ratio}},
    {{pre_avg30_trade_price_ratio}},
    {{pre_avg60_trade_price_ratio}},
    {{pre_avg90_trade_price_ratio}},
    {{pre_avg120_trade_price_ratio}},
    {{pre_avg250_trade_price_ratio}},
    {{pre_avg365_trade_price_ratio}},
    {{pre_avg5_trade_amt_ratio}},
    {{pre_avg10_trade_amt_ratio}},
    {{pre_avg20_trade_amt_ratio}},
    {{pre_avg30_trade_amt_ratio}},
    {{pre_avg60_trade_amt_ratio}},
    {{pre_avg90_trade_amt_ratio}},
    {{pre_avg120_trade_amt_ratio}},
    {{pre_avg250_trade_amt_ratio}},
    {{pre_avg365_trade_amt_ratio}},
    {{pre_avg5_trade_net_amt_ratio}},
    {{pre_avg10_trade_net_amt_ratio}},
    {{pre_avg20_trade_net_amt_ratio}},
    {{pre_avg30_trade_net_amt_ratio}},
    {{pre_avg60_trade_net_amt_ratio}},
    {{pre_avg90_trade_net_amt_ratio}},
    {{pre_avg120_trade_net_amt_ratio}},
    {{pre_avg250_trade_net_amt_ratio}},
    {{pre_avg365_trade_net_amt_ratio}},
    {{pre_avg5_trade_volume_ratio}},
    {{pre_avg10_trade_volume_ratio}},
    {{pre_avg20_trade_volume_ratio}},
    {{pre_avg30_trade_volume_ratio}},
    {{pre_avg60_trade_volume_ratio}},
    {{pre_avg90_trade_volume_ratio}},
    {{pre_avg120_trade_volume_ratio}},
    {{pre_avg250_trade_volume_ratio}},
    {{pre_avg365_trade_volume_ratio}},
    {{pre_avg5_trade_count_ratio}},
    {{pre_avg10_trade_count_ratio}},
    {{pre_avg20_trade_count_ratio}},
    {{pre_avg30_trade_count_ratio}},
    {{pre_avg60_trade_count_ratio}},
    {{pre_avg90_trade_count_ratio}},
    {{pre_avg120_trade_count_ratio}},
    {{pre_avg250_trade_count_ratio}},
    {{pre_avg365_trade_count_ratio}},
    {{pre_avg5_trade_per_avg_volume_ratio}},
    {{pre_avg10_trade_per_avg_volume_ratio}},
    {{pre_avg20_trade_per_avg_volume_ratio}},
    {{pre_avg30_trade_per_avg_volume_ratio}},
    {{pre_avg60_trade_per_avg_volume_ratio}},
    {{pre_avg90_trade_per_avg_volume_ratio}},
    {{pre_avg120_trade_per_avg_volume_ratio}},
    {{pre_avg250_trade_per_avg_volume_ratio}},
    {{pre_avg365_trade_per_avg_volume_ratio}},
    {{dragon_tiger_today_is}},
    {{dragon_tiger_all_today_amt}},
    {{dragon_tiger_all_today_buy_amt_ratio}},
    {{dragon_tiger_all_today_sell_amt_ratio}},
    {{dragon_tiger_organ_today_buy_amt_ratio}},
    {{dragon_tiger_organ_today_sell_amt_ratio}},
    {{dragon_tiger_sale_today_buy_amt_ratio}},
    {{dragon_tiger_sale_today_sell_amt_ratio}},
    {{dragon_tiger_total_is}},
    {{dragon_tiger_all_total_amt}},
    {{dragon_tiger_all_total_buy_amt_ratio}},
    {{dragon_tiger_all_total_sell_amt_ratio}},
    {{dragon_tiger_organ_total_buy_amt_ratio}},
    {{dragon_tiger_organ_total_sell_amt_ratio}},
    {{dragon_tiger_sale_total_buy_amt_ratio}},
    {{dragon_tiger_sale_total_sell_amt_ratio}},
    {{dragon_tiger_all_5day_bs_count_percent}},
    {{dragon_tiger_all_5day_bs_diff_amt}},
    {{dragon_tiger_organ_5day_bs_amt_percent}},
    {{dragon_tiger_organ_5day_bs_count_percent}},
    {{dragon_tiger_organ_5day_bs_diff_amt}},
    '{{dragon_tiger_sale_5day_name}}',
    {{medium_sum_trade_amt_ratio}},
    {{large_sum_trade_amt_ratio}},
    {{super_sum_trade_amt_ratio}},
    {{small_inside_sum_trade_amt_ratio}},
    {{small_outside_sum_trade_amt_ratio}},
    {{medium_inside_sum_trade_amt_ratio}},
    {{medium_outside_sum_trade_amt_ratio}},
    {{large_inside_sum_trade_amt_ratio}},
    {{large_outside_sum_trade_amt_ratio}},
    {{super_inside_sum_trade_amt_ratio}},
    {{super_outside_sum_trade_amt_ratio}},
    '{{trade_date}}'
);