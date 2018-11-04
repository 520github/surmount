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