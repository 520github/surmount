drop table t_tushare_stock_fund_holding;

CREATE TABLE `t_tushare_stock_fund_holding` (
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `date` date NOT NULL COMMENT '报告日期',
  `nums` int NOT NULL DEFAULT -1 COMMENT '基金家数',
  `nlast` int NOT NULL DEFAULT -1 COMMENT '与上期相比（增加或减少）',
  `count` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '基金持股数（万股）',
  `clast` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '与上期相比',
  `amount` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '基金持股市值',
  `ratio` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '占流通盘比率',
  `year` int NOT NULL DEFAULT -1 COMMENT '年份',
  `quarter` int NOT NULL DEFAULT -1 COMMENT '季度',
  `handle_date` date NOT NULL COMMENT '处理日期',
  KEY `unique_code_year_quarter` (`code`,`year`,`quarter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE `t_tushare_stock_limited_sale_reopen`;

CREATE TABLE `t_tushare_stock_limited_sale_reopen` (
  `index` bigint(20) DEFAULT NULL,
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `date` date NOT NULL COMMENT '解禁日期',
  `count` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '解禁数量（万股）',
  `ratio` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '占总盘比率',
  `year` int NOT NULL DEFAULT -1 COMMENT '年份',
  `month` int NOT NULL DEFAULT -1 COMMENT '月份',
  `handle_date` date NOT NULL COMMENT '处理日期',
  KEY `ix_t_tushare_stock_limited_sale_reopen_index` (`index`),
  KEY `unique_code_year_month` (`code`,`year`,`month`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table `t_tushare_stock_performance_report`;

CREATE TABLE `t_tushare_stock_performance_report` (
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `eps` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '每股收益',
  `eps_yoy` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '每股收益同比(%)',
  `bvps` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '每股净资产',
  `roe` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '净资产收益率(%)',
  `epcf` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '每股现金流量(元)',
  `net_profits` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '净利润(万元)',
  `profits_yoy` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '净利润同比(%)',
  `distrib` varchar(512) NOT NULL DEFAULT '' COMMENT '分配方案',
  `report_date` varchar(32) NOT NULL DEFAULT ''  COMMENT '发布日期',
  `year` int NOT NULL DEFAULT -1 COMMENT '年份',
  `quarter` int NOT NULL DEFAULT -1 COMMENT '季度',
  `date` date NOT NULL COMMENT '处理日期',
  KEY `unique_code_year_quarter` (`code`,`year`,`quarter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop TABLE `t_tushare_stock_abitity_profit`;
CREATE TABLE `t_tushare_stock_abitity_profit` (
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `roe` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '净资产收益率(%)',
  `net_profit_ratio` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '净利率(%)',
  `gross_profit_rate` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '毛利率(%)',
  `net_profits` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '净利润(万元)',
  `eps` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '每股收益',
  `business_income` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '营业收入(百万元)',
  `bips` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '每股主营业务收入(元)',
  `year` int NOT NULL DEFAULT -1 COMMENT '年份',
  `quarter` int NOT NULL DEFAULT -1 COMMENT '季度',
  `date` date NOT NULL COMMENT '处理日期',
  KEY `unique_code_year_quarter` (`code`,`year`,`quarter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table `t_tushare_stock_ability_operation`;
CREATE TABLE `t_tushare_stock_ability_operation` (
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `arturnover` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '应收账款周转率(次)',
  `arturndays` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '应收账款周转天数(天)',
  `inventory_turnover` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '存货周转率(次)',
  `inventory_days` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '存货周转天数(天)',
  `currentasset_turnover` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '流动资产周转率(次)',
  `currentasset_days` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '流动资产周转天数(天)',
  `year` int NOT NULL DEFAULT -1 COMMENT '年份',
  `quarter` int NOT NULL DEFAULT -1 COMMENT '季度',
  `date` date NOT NULL COMMENT '处理日期',
  KEY `unique_code_year_quarter` (`code`,`year`,`quarter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



drop table `t_tushare_stock_ability_growth`;
CREATE TABLE `t_tushare_stock_ability_growth` (
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `mbrg` decimal(12,4) NOT NULL  DEFAULT -1 COMMENT '主营业务收入增长率(%)',
  `nprg` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '净利润增长率(%)',
  `nav` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '净资产增长率',
  `targ` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '总资产增长率',
  `epsg` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '每股收益增长率',
  `seg` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '股东权益增长率',
  `year` int NOT NULL DEFAULT -1 COMMENT '年份',
  `quarter` int NOT NULL DEFAULT -1 COMMENT '季度',
  `date` date NOT NULL COMMENT '处理日期',
  KEY `unique_code_year_quarter` (`code`,`year`,`quarter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table t_tushare_stock_ability_debt_pay;
CREATE TABLE `t_tushare_stock_ability_debt_pay` (
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `currentratio` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '流动比率',
  `quickratio` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '速动比率',
  `cashratio` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '现金比率',
  `icratio` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '利息支付倍数',
  `sheqratio` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '股东权益比率',
  `adratio` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '股东权益增长率',
  `year` int NOT NULL DEFAULT -1 COMMENT '年份',
  `quarter` int NOT NULL DEFAULT -1 COMMENT '季度',
  `date` date NOT NULL COMMENT '处理日期',
  KEY `unique_code_year_quarter` (`code`,`year`,`quarter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table `t_tushare_stock_ability_cash_flow`;
CREATE TABLE `t_tushare_stock_ability_cash_flow` (
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `cf_sales` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '经营现金净流量对销售收入比率',
  `rateofreturn` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '资产的经营现金流量回报率',
  `cf_nm` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '经营现金净流量与净利润的比率',
  `cf_liabilities` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '经营现金净流量对负债比率',
  `cashflowratio` decimal(12,4) NOT NULL DEFAULT -1 COMMENT '现金流量比率',
  `year` int NOT NULL DEFAULT -1 COMMENT '年份',
  `quarter` int NOT NULL DEFAULT -1 COMMENT '季度',
  `date` date NOT NULL COMMENT '处理日期',
  KEY `unique_code_year_quarter` (`code`,`year`,`quarter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



drop table `t_tushare_stock_basic`;

CREATE TABLE `t_tushare_stock_basic` (
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `industry` varchar(128) NOT NULL DEFAULT '' COMMENT '行业',
  `area` varchar(128) NOT NULL DEFAULT '' COMMENT '地区',
  `pe` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '市盈率',
  `outstanding` decimal(12,3) NOT NULL DEFAULT -1 COMMENT  '流通股本(亿)',
  `totals` decimal(12,3) NOT NULL DEFAULT -1 COMMENT  '总股本(亿)',
  `totalAssets` decimal(18,3) NOT NULL DEFAULT -1 COMMENT  '总资产(万)',
  `liquidAssets` decimal(18,3) NOT NULL DEFAULT -1 COMMENT  '流动资产(万)',
  `fixedAssets` decimal(18,3) NOT NULL DEFAULT -1 COMMENT  '固定资产(万)',
  `reserved` decimal(12,3) NOT NULL DEFAULT -1 COMMENT  '公积金(万)',
  `reservedPerShare` decimal(8,3) NOT NULL DEFAULT -1 COMMENT  '每股公积金(元)',
  `esp` decimal(8,4) NOT NULL DEFAULT -1 COMMENT '每股收益',
  `bvps` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '每股净资产',
  `pb` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '市净率',
  `timeToMarket` bigint(20) NOT NULL DEFAULT -1 COMMENT '上市时间',
  `undp` decimal(12,3) NOT NULL DEFAULT -1 COMMENT  '未分配利润(万)',
  `perundp` decimal(8,3) NOT NULL DEFAULT -1 COMMENT  '每股未分配利润(元)',
  `rev` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '收入同比%',
  `profit` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '利润同比%',
  `gpr` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '毛利率%',
  `npr` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '净利润率%',
  `holders` bigint NOT NULL DEFAULT -1 COMMENT '股东人数',
  `date` date NOT NULL COMMENT '交易日期',
  UNIQUE KEY `unique_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table t_tushare_stock_today_tick_trade_data;
CREATE TABLE `t_tushare_stock_today_tick_trade_data` (
  `index` bigint(20) DEFAULT NULL,
  `time` varchar(64) NOT NULL DEFAULT '' COMMENT '交易时间',
  `price` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '交易价格(元)',
  `pchange` varchar(64) NOT NULL DEFAULT '' COMMENT '涨跌幅',
  `change` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '价格变动(元)',
  `volume` bigint(20) NOT NULL DEFAULT -1 COMMENT '交易手数',
  `amount` bigint(20) NOT NULL DEFAULT -1 COMMENT '交易金额(元)',
  `type` varchar(32) NOT NULL DEFAULT '' COMMENT '交易类型',
  `date` date DEFAULT NULL COMMENT '交易日期',
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  KEY `ix_t_tushare_stock_today_tick_trade_data_index` (`index`),
  KEY `index_code_date` (`code`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table `t_tushare_stock_newly_quotes_data` ;
CREATE TABLE `t_tushare_stock_newly_quotes_data` (
  `index` bigint(20) DEFAULT NULL,
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `changepercent` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '涨跌幅%',
  `trade` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '收盘价(元)',
  `open` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '开盘价(元)',
  `high` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '最高价(元)',
  `low` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '最低价(元)',
  `settlement` decimal(8,3)  NOT NULL DEFAULT -1 COMMENT '昨日收盘价(元)',
  `volume`  bigint NOT NULL DEFAULT -1  COMMENT '成交量(股)',
  `turnoverratio` decimal(8,5) NOT NULL DEFAULT -1 COMMENT '换手率%',
  `amount` decimal(18,0) NOT NULL DEFAULT -1 COMMENT '成交金额(元)' ,
  `per` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '市盈率',
  `pb` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '市净率',
  `mktcap` decimal(16,7) NOT NULL DEFAULT -1 COMMENT '总市值(万)',
  `nmc` decimal(16,7) NOT NULL DEFAULT -1 COMMENT '流通市值(万)',
  `date` date DEFAULT NULL,
  KEY `ix_t_tushare_stock_newly_quotes_data_index` (`index`),
  KEY `unique_code_date` (`code`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table `t_tushare_stock_newly_quotes_data_hist` ;
CREATE TABLE `t_tushare_stock_newly_quotes_data_hist` (
  `index` bigint(20) DEFAULT NULL,
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `changepercent` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '涨跌幅%',
  `trade` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '收盘价(元)',
  `open` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '开盘价(元)',
  `high` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '最高价(元)',
  `low` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '最低价(元)',
  `settlement` decimal(8,3)  NOT NULL DEFAULT -1 COMMENT '昨日收盘价(元)',
  `volume`  bigint NOT NULL DEFAULT -1  COMMENT '成交量(股)',
  `turnoverratio` decimal(8,5) NOT NULL DEFAULT -1 COMMENT '换手率%',
  `amount` decimal(18,0) NOT NULL DEFAULT -1 COMMENT '成交金额(元)' ,
  `per` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '市盈率',
  `pb` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '市净率',
  `mktcap` decimal(16,7) NOT NULL DEFAULT -1 COMMENT '总市值(万)',
  `nmc` decimal(16,7) NOT NULL DEFAULT -1 COMMENT '流通市值(万)',
  `date` date DEFAULT NULL,
  KEY `ix_t_tushare_stock_newly_quotes_data_hist_index` (`index`),
  KEY `unique_code_date` (`code`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table `t_tushare_stock_hist_quotes_data` ;
CREATE TABLE `t_tushare_stock_hist_quotes_data` (
  `date` date DEFAULT NULL COMMENT '交易日期',
  `open` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '开盘价(元)',
  `high` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '最高价(元)',
  `close` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '收盘价(元)',
  `low` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '最低价(元)',
  `volume`  bigint NOT NULL DEFAULT -1  COMMENT '成交量(股)',
  `price_change` decimal(8,5) NOT NULL DEFAULT -1 COMMENT '价格变动(元)',
  `p_change` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '涨跌幅%',
  `ma5` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '5日均价(元)',
  `ma10` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '10日均价(元)',
  `ma20` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '20日均价(元)',
  `v_ma5` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '5日均量(手)',
  `v_ma10` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '10日均量(手)',
  `v_ma20` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '20日均量(手)',
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  UNIQUE KEY `unique_date_code` (`date`,`code`),
  KEY `index` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table `t_tushare_stock_dragon_tiger_total_data` ;
CREATE TABLE `t_tushare_stock_dragon_tiger_total_data` (
  `index` bigint(20) NOT NULL DEFAULT -1,
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `count` bigint(20) NOT NULL DEFAULT -1 COMMENT '上榜次数',
  `bamount` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '累积购买额(万)',
  `samount` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '累积卖出额(万)',
  `net` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '净额(万)',
  `bcount` bigint(20) NOT NULL DEFAULT -1 COMMENT '买入席位数',
  `scount` bigint(20) NOT NULL DEFAULT -1 COMMENT '卖出席位数',
  `days` bigint(20) NOT NULL DEFAULT -1 COMMENT '统计周期,5、10、30和60日，默认为5日',
  `date` date DEFAULT NULL COMMENT '统计日期',
  KEY `ix_t_tushare_stock_dragon_tiger_total_data_index` (`index`),
  UNIQUE KEY `unique_date_days_code` (`date`,`days`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table `t_tushare_stock_dragon_tiger_today_data`;
CREATE TABLE `t_tushare_stock_dragon_tiger_today_data` (
  `index` bigint(20) NOT NULL DEFAULT -1,
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `pchange` decimal(8,5) NOT NULL DEFAULT -1 COMMENT '当日涨跌幅%',
  `amount` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '累积购买额(万)',
  `buy` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '累积购买额(万)',
  `sell` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '累积购买额(万)',
  `reason` varchar(512) NOT NULL DEFAULT '' COMMENT '上榜原因',
  `bratio` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '买入占总成交比例%',
  `sratio` decimal(8,3) NOT NULL DEFAULT -1 COMMENT '卖出占总成交比例%',
  `date` date DEFAULT NULL COMMENT '交易日期',
  KEY `ix_t_tushare_stock_dragon_tiger_today_data_index` (`index`),
  key `index_date_code` (`date`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table `t_tushare_stock_dragon_tiger_organ_total_data`;
CREATE TABLE `t_tushare_stock_dragon_tiger_organ_total_data` (
  `index` bigint(20) NOT NULL DEFAULT -1,
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `bamount` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '累积买入额(万)',
  `bcount` bigint(20) NOT NULL DEFAULT -1 COMMENT '买入次数',
  `samount` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '累积卖出额(万)',
  `scount` bigint(20) NOT NULL DEFAULT -1 COMMENT '卖出次数',
  `net` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '净额(万)',
  `days` bigint(20) NOT NULL DEFAULT -1 COMMENT '统计周期,5、10、30和60日，默认为5日',
  `date` date DEFAULT NULL COMMENT '交易日期',
  KEY `ix_t_tushare_stock_dragon_tiger_organ_total_data_index` (`index`),
  UNIQUE KEY `unique_date_days_code` (`date`,`days`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table `t_tushare_stock_dragon_tiger_organ_today_data` ;
CREATE TABLE `t_tushare_stock_dragon_tiger_organ_today_data` (
  `index` bigint(20) NOT NULL DEFAULT -1,
  `code` varchar(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `date` date DEFAULT NULL COMMENT '交易日期',
  `bamount` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '机构席位买入额(万)',
  `samount` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '机构席位卖出额(万)',
  `type` varchar(512) NOT NULL DEFAULT '' COMMENT '上榜原因',
  `get_date` date DEFAULT NULL COMMENT '获取数据时间日期',
  KEY `ix_t_tushare_stock_dragon_tiger_organ_today_data_index` (`index`),
  key `index_getdate_date_code` (`get_date`,`date`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table `t_tushare_stock_dragon_tiger_sale_total_data` ;
CREATE TABLE `t_tushare_stock_dragon_tiger_sale_total_data` (
  `index` bigint(20) NOT NULL DEFAULT -1,
  `broker` varchar(512) NOT NULL DEFAULT '' COMMENT '营业部名称',
  `count` bigint(20) NOT NULL DEFAULT -1 COMMENT '上榜次数',
  `bamount` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '累积购买额(万)',
  `bcount` bigint(20) NOT NULL DEFAULT -1 COMMENT '买入席位数',
  `samount` decimal(12,3) NOT NULL DEFAULT -1 COMMENT '累积卖出额(万)',
  `scount` bigint(20) NOT NULL DEFAULT -1 COMMENT '卖出席位数',
  `top3` varchar(512) NOT NULL DEFAULT '' COMMENT '买入前三股票',
  `days` bigint(20) NOT NULL DEFAULT -1 COMMENT '统计周期,5、10、30和60日，默认为5日',
  `date` date DEFAULT NULL COMMENT '交易日期',
  KEY `ix_t_tushare_stock_dragon_tiger_sale_total_data_index` (`index`),
  KEY `index_date_days` (`date`,`days`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;