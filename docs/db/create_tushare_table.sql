
CREATE TABLE `t_tushare_stock_newly_quotes_data_hist` (
  `index` bigint(20) DEFAULT NULL,
  `code` varchar(32) DEFAULT NULL,
  `name` text,
  `changepercent` double DEFAULT NULL,
  `trade` double DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `settlement` double DEFAULT NULL,
  `volume` bigint(20) DEFAULT NULL,
  `turnoverratio` double DEFAULT NULL,
  `amount` bigint(20) DEFAULT NULL,
  `per` double DEFAULT NULL,
  `pb` double DEFAULT NULL,
  `mktcap` double DEFAULT NULL,
  `nmc` double DEFAULT NULL,
  `date` varchar(32) DEFAULT NULL,
  KEY `ix_t_tushare_stock_newly_quotes_data_index` (`index`),
  KEY `unique_date_code` (`date`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

