## ETF-SCRAPER
### Create mysql database
```CREATE TABLE `bloomberg` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `return_3_months` float DEFAULT NULL,
  `return_ytd` float DEFAULT NULL,
  `return_1_year` float DEFAULT NULL,
  `return_3_year` float DEFAULT NULL,
  `return_5_year` float DEFAULT NULL,
  `inception_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
)```
### Parse to html file per etf
```python parse_html.py```
### Save date to mysql
```python scraper.py```
### Data mining
```select name, return_3_months, return_ytd , return_1_year , return_3_year , return_5_year , inception_date from bloomberg order by return_1_year desc limit 10;```