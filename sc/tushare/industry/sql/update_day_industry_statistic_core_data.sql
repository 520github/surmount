update t_sunso_stock_day_industry_statistic_core_data
set
sum_up_limit_count={{sum_up_limit_count}},
sum_down_limit_count={{sum_down_limit_count}},
up_down_limit_count_ratio={{up_down_limit_count_ratio}},
sum_up_count={{sum_up_count}},
sum_down_count={{sum_down_count}},
up_down_count_ratio={{up_down_count_ratio}},
up_top1_name='{{up_top1_name}}',
up_top2_name='{{up_top2_name}}',
up_top3_name='{{up_top3_name}}',
down_top1_name='{{down_top1_name}}',
down_top2_name='{{down_top2_name}}',
down_top3_name='{{down_top3_name}}',
up_avg_close_price_ratio={{up_avg_close_price_ratio}},
down_avg_close_price_ratio={{down_avg_close_price_ratio}},

pre1_totals_stock_amt_ratio={{pre1_totals_stock_amt_ratio}},
pre1_circulation_stock_amt_ratio={{pre1_circulation_stock_amt_ratio}},
pre1_totals_stock_volume_ratio={{pre1_totals_stock_volume_ratio}},
pre1_circulation_stock_volume_ratio={{pre1_circulation_stock_volume_ratio}},

pre3_totals_stock_amt_ratio={{pre3_totals_stock_amt_ratio}},
pre3_circulation_stock_amt_ratio={{pre3_circulation_stock_amt_ratio}},
pre3_totals_stock_volume_ratio={{pre3_totals_stock_volume_ratio}},
pre3_circulation_stock_volume_ratio={{pre3_circulation_stock_volume_ratio}},
pre3_sum_close_price_ratio={{pre3_sum_close_price_ratio}},
pre3_avg_close_price_ratio={{pre3_avg_close_price_ratio}},
pre3_avg_trade_amt={{pre3_avg_trade_amt}},
pre3_avg_trade_volume={{pre3_avg_trade_volume}},
pre3_avg_trade_count={{pre3_avg_trade_count}},

pre5_totals_stock_amt_ratio={{pre5_totals_stock_amt_ratio}},
pre5_circulation_stock_amt_ratio={{pre5_circulation_stock_amt_ratio}},
pre5_totals_stock_volume_ratio={{pre5_totals_stock_volume_ratio}},
pre5_circulation_stock_volume_ratio={{pre5_circulation_stock_volume_ratio}},
pre5_sum_close_price_ratio={{pre5_sum_close_price_ratio}},
pre5_avg_close_price_ratio={{pre5_avg_close_price_ratio}},
pre5_avg_trade_amt={{pre5_avg_trade_amt}},
pre5_avg_trade_volume={{pre5_avg_trade_volume}},
pre5_avg_trade_count={{pre5_avg_trade_count}},

pre10_totals_stock_amt_ratio={{pre10_totals_stock_amt_ratio}},
pre10_circulation_stock_amt_ratio={{pre10_circulation_stock_amt_ratio}},
pre10_totals_stock_volume_ratio={{pre10_totals_stock_volume_ratio}},
pre10_circulation_stock_volume_ratio={{pre10_circulation_stock_volume_ratio}},
pre10_sum_close_price_ratio={{pre10_sum_close_price_ratio}},
pre10_avg_close_price_ratio={{pre10_avg_close_price_ratio}},
pre10_avg_trade_amt={{pre10_avg_trade_amt}},
pre10_avg_trade_volume={{pre10_avg_trade_volume}},
pre10_avg_trade_count={{pre10_avg_trade_count}},

pre20_totals_stock_amt_ratio={{pre20_totals_stock_amt_ratio}},
pre20_circulation_stock_amt_ratio={{pre20_circulation_stock_amt_ratio}},
pre20_totals_stock_volume_ratio={{pre20_totals_stock_volume_ratio}},
pre20_circulation_stock_volume_ratio={{pre20_circulation_stock_volume_ratio}},
pre20_sum_close_price_ratio={{pre20_sum_close_price_ratio}},
pre20_avg_close_price_ratio={{pre20_avg_close_price_ratio}},
pre20_avg_trade_amt={{pre20_avg_trade_amt}},
pre20_avg_trade_volume={{pre20_avg_trade_volume}},
pre20_avg_trade_count={{pre20_avg_trade_count}},

pre30_totals_stock_amt_ratio={{pre30_totals_stock_amt_ratio}},
pre30_circulation_stock_amt_ratio={{pre30_circulation_stock_amt_ratio}},
pre30_totals_stock_volume_ratio={{pre30_totals_stock_volume_ratio}},
pre30_circulation_stock_volume_ratio={{pre30_circulation_stock_volume_ratio}},
pre30_sum_close_price_ratio={{pre30_sum_close_price_ratio}},
pre30_avg_close_price_ratio={{pre30_avg_close_price_ratio}},
pre30_avg_trade_amt={{pre30_avg_trade_amt}},
pre30_avg_trade_volume={{pre30_avg_trade_volume}},
pre30_avg_trade_count={{pre30_avg_trade_count}},

pre60_totals_stock_amt_ratio={{pre60_totals_stock_amt_ratio}},
pre60_circulation_stock_amt_ratio={{pre60_circulation_stock_amt_ratio}},
pre60_totals_stock_volume_ratio={{pre60_totals_stock_volume_ratio}},
pre60_circulation_stock_volume_ratio={{pre60_circulation_stock_volume_ratio}},
pre60_sum_close_price_ratio={{pre60_sum_close_price_ratio}},
pre60_avg_close_price_ratio={{pre60_avg_close_price_ratio}},
pre60_avg_trade_amt={{pre60_avg_trade_amt}},
pre60_avg_trade_volume={{pre60_avg_trade_volume}},
pre60_avg_trade_count={{pre60_avg_trade_count}},

pre90_totals_stock_amt_ratio={{pre90_totals_stock_amt_ratio}},
pre90_circulation_stock_amt_ratio={{pre90_circulation_stock_amt_ratio}},
pre90_totals_stock_volume_ratio={{pre90_totals_stock_volume_ratio}},
pre90_circulation_stock_volume_ratio={{pre90_circulation_stock_volume_ratio}},
pre90_sum_close_price_ratio={{pre90_sum_close_price_ratio}},
pre90_avg_close_price_ratio={{pre90_avg_close_price_ratio}},
pre90_avg_trade_amt={{pre90_avg_trade_amt}},
pre90_avg_trade_volume={{pre90_avg_trade_volume}},
pre90_avg_trade_count={{pre90_avg_trade_count}},

pre120_totals_stock_amt_ratio={{pre120_totals_stock_amt_ratio}},
pre120_circulation_stock_amt_ratio={{pre120_circulation_stock_amt_ratio}},
pre120_totals_stock_volume_ratio={{pre120_totals_stock_volume_ratio}},
pre120_circulation_stock_volume_ratio={{pre120_circulation_stock_volume_ratio}},
pre120_sum_close_price_ratio={{pre120_sum_close_price_ratio}},
pre120_avg_close_price_ratio={{pre120_avg_close_price_ratio}},
pre120_avg_trade_amt={{pre120_avg_trade_amt}},
pre120_avg_trade_volume={{pre120_avg_trade_volume}},
pre120_avg_trade_count={{pre120_avg_trade_count}}

where 1>0
and trade_date='{{trade_date}}'
and industry = '{{industry}}'
